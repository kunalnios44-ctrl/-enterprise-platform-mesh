// SPDX-License-Identifier: GPL-2.0
#include <linux/bpf.h>
#include <linux/pkt_cls.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define IP_OFFSET 0x1FFF

struct chaos_policy {
    __u32 drop_percent;
    __u32 protect_ctrl_flags;
    __u32 enabled;
};

struct chaos_stats {
    __u64 total_packets;
    __u64 dropped_packets;
    __u64 bypassed_packets;
};

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 256);
    __type(key, __u16);
    __type(value, struct chaos_policy);
} policy_map SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct chaos_stats);
} stats_map SEC(".maps");

SEC("tc")
int chaos_tc_egress(struct __sk_buff *skb)
{
    void *data = (void *)(long)skb->data;
    void *data_end = (void *)(long)skb->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return TC_ACT_OK;

    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return TC_ACT_OK;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end)
        return TC_ACT_OK;

    __u32 ip_hdr_len = ip->ihl * 4;
    if (ip_hdr_len < sizeof(*ip))
        return TC_ACT_OK;

    if ((void *)ip + ip_hdr_len > data_end)
        return TC_ACT_OK;

    if (ip->protocol != IPPROTO_TCP)
        return TC_ACT_OK;

    __u16 frag_off = bpf_ntohs(ip->frag_off);
    if (frag_off & IP_OFFSET)
        return TC_ACT_OK;

    struct tcphdr *tcp = (void *)ip + ip_hdr_len;
    if ((void *)(tcp + 1) > data_end)
        return TC_ACT_OK;

    __u32 tcp_hdr_len = tcp->doff * 4;
    if (tcp_hdr_len < sizeof(*tcp))
        return TC_ACT_OK;

    if ((void *)tcp + tcp_hdr_len > data_end)
        return TC_ACT_OK;

    __u16 dport = bpf_ntohs(tcp->dest);

    struct chaos_policy *policy =
        bpf_map_lookup_elem(&policy_map, &dport);

    if (!policy || !policy->enabled)
        return TC_ACT_OK;

    __u32 key = 0;
    struct chaos_stats *stats =
        bpf_map_lookup_elem(&stats_map, &key);

    if (stats)
        stats->total_packets++;

    if (policy->protect_ctrl_flags &&
        (tcp->syn || tcp->fin || tcp->rst)) {
        if (stats)
            stats->bypassed_packets++;

        return TC_ACT_OK;
    }

    if (policy->drop_percent >= 100) {
        if (stats)
            stats->dropped_packets++;

        return TC_ACT_SHOT;
    }

    if (policy->drop_percent > 0) {
        __u64 random = bpf_get_prandom_u32();
        __u32 scaled = (__u32)((random * 100) >> 32);

        if (scaled < policy->drop_percent) {
            if (stats)
                stats->dropped_packets++;

            return TC_ACT_SHOT;
        }
    }

    return TC_ACT_OK;
}

char _license[] SEC("license") = "GPL";
