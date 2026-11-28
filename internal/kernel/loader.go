package kernel

import (
	"errors"
	"fmt"
	"net"

	"github.com/cilium/ebpf"
	"github.com/cilium/ebpf/link"
)

var ErrControllerClosed = errors.New("ebpf controller is nil or closed")

type ChaosPolicy struct {
	DropPercent      uint32
	ProtectCtrlFlags uint32
	Enabled          uint32
}

type ChaosStats struct {
	TotalPackets    uint64
	DroppedPackets  uint64
	BypassedPackets uint64
}

type bpfObjects struct {
	ChaosTcEgress *ebpf.Program `ebpf:"chaos_tc_egress"`
	PolicyMap     *ebpf.Map     `ebpf:"policy_map"`
	StatsMap      *ebpf.Map     `ebpf:"stats_map"`
}

func (o *bpfObjects) Close() error {
	var errs []error

	if o.ChaosTcEgress != nil {
		errs = append(errs, o.ChaosTcEgress.Close())
	}
	if o.PolicyMap != nil {
		errs = append(errs, o.PolicyMap.Close())
	}
	if o.StatsMap != nil {
		errs = append(errs, o.StatsMap.Close())
	}

	return errors.Join(errs...)
}

type Controller struct {
	objs   bpfObjects
	tcLink link.Link
}

func LoadAndAttach(objPath, ifaceName string) (*Controller, error) {
	if objPath == "" {
		return nil, errors.New("object path is required")
	}
	if ifaceName == "" {
		return nil, errors.New("interface name is required")
	}

	iface, err := net.InterfaceByName(ifaceName)
	if err != nil {
		return nil, fmt.Errorf("find interface %q: %w", ifaceName, err)
	}

	spec, err := ebpf.LoadCollectionSpec(objPath)
	if err != nil {
		return nil, fmt.Errorf("load eBPF object %q: %w", objPath, err)
	}

	var objs bpfObjects
	if err := spec.LoadAndAssign(&objs, nil); err != nil {
		return nil, fmt.Errorf("load eBPF objects: %w", err)
	}

	tcLink, err := link.AttachTCX(link.TCXOptions{
		Interface: iface.Index,
		Program:   objs.ChaosTcEgress,
		Attach:    ebpf.AttachTCXEgress,
	})
	if err != nil {
		_ = objs.Close()
		return nil, fmt.Errorf("attach TCX egress to %q: %w", ifaceName, err)
	}

	return &Controller{
		objs:   objs,
		tcLink: tcLink,
	}, nil
}

func (c *Controller) SetPortPolicy(
	dport uint16,
	dropPercent uint32,
	protectCtrl bool,
	enabled bool,
) error {
	if c == nil || c.objs.PolicyMap == nil {
		return ErrControllerClosed
	}

	if dport == 0 {
		return errors.New("destination port must be greater than 0")
	}

	if dropPercent > 100 {
		return fmt.Errorf("drop_percent %d must be between 0 and 100", dropPercent)
	}

	var protect, active uint32

	if protectCtrl {
		protect = 1
	}
	if enabled {
		active = 1
	}

	policy := ChaosPolicy{
		DropPercent:      dropPercent,
		ProtectCtrlFlags: protect,
		Enabled:          active,
	}

	if err := c.objs.PolicyMap.Put(dport, policy); err != nil {
		return fmt.Errorf("update policy for port %d: %w", dport, err)
	}

	return nil
}

func (c *Controller) RemovePortPolicy(dport uint16) error {
	if c == nil || c.objs.PolicyMap == nil {
		return ErrControllerClosed
	}

	if err := c.objs.PolicyMap.Delete(dport); err != nil &&
		!errors.Is(err, ebpf.ErrKeyNotExist) {
		return fmt.Errorf("remove policy for port %d: %w", dport, err)
	}

	return nil
}

func (c *Controller) ReadAggregatedStats() (ChaosStats, error) {
	if c == nil || c.objs.StatsMap == nil {
		return ChaosStats{}, ErrControllerClosed
	}

	var statsKey uint32
	var perCPUStats []ChaosStats

	if err := c.objs.StatsMap.Lookup(statsKey, &perCPUStats); err != nil {
		return ChaosStats{}, fmt.Errorf("read per-CPU stats: %w", err)
	}

	var total ChaosStats

	for _, stats := range perCPUStats {
		total.TotalPackets += stats.TotalPackets
		total.DroppedPackets += stats.DroppedPackets
		total.BypassedPackets += stats.BypassedPackets
	}

	return total, nil
}

func (c *Controller) Close() error {
	if c == nil {
		return nil
	}

	var errs []error

	if c.tcLink != nil {
		errs = append(errs, c.tcLink.Close())
		c.tcLink = nil
	}

	errs = append(errs, c.objs.Close())

	return errors.Join(errs...)
}
