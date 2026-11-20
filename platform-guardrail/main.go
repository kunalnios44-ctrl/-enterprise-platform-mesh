
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

const maxConfigBytes int64 = 1 << 20

type rawPlatformConfig struct {
	Env            *string `json:"env"`
	Region         *string `json:"region"`
	Replicas       *int    `json:"replicas"`
	LeastPrivilege *bool   `json:"least_privilege"`
	DRVerified     *bool   `json:"dr_verified"`
}

type PlatformConfig struct {
	Env            string
	Region         string
	Replicas       int
	LeastPrivilege bool
	DRVerified     bool
}

func readBoundedFileWithContext(ctx context.Context, path string, maxBytes int64) ([]byte, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	if maxBytes <= 0 {
		return nil, errors.New("maximum file size must be positive")
	}

	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	info, err := f.Stat()
	if err != nil {
		return nil, err
	}
	if !info.Mode().IsRegular() {
		return nil, errors.New("config path is not a regular file")
	}
	if info.Size() > maxBytes {
		return nil, fmt.Errorf("config file exceeds maximum allowed size of %d bytes", maxBytes)
	}

	data, err := io.ReadAll(io.LimitReader(f, maxBytes+1))
	if err != nil {
		return nil, err
	}
	if int64(len(data)) > maxBytes {
		return nil, fmt.Errorf("config file exceeds maximum allowed size of %d bytes", maxBytes)
	}
	if err := ctx.Err(); err != nil {
		return nil, err
	}

	return data, nil
}

func parseStrictConfig(data []byte) (PlatformConfig, error) {
	if len(bytes.TrimSpace(data)) == 0 {
		return PlatformConfig{}, errors.New("configuration file is empty")
	}

	var raw rawPlatformConfig
	dec := json.NewDecoder(bytes.NewReader(data))
	dec.DisallowUnknownFields()

	if err := dec.Decode(&raw); err != nil {
		return PlatformConfig{}, err
	}

	var extra any
	if err := dec.Decode(&extra); err != io.EOF {
		if err == nil {
			return PlatformConfig{}, errors.New("unexpected trailing JSON data")
		}
		return PlatformConfig{}, fmt.Errorf("invalid trailing JSON data: %w", err)
	}

	if raw.Env == nil || raw.Region == nil ||
		raw.Replicas == nil || raw.LeastPrivilege == nil ||
		raw.DRVerified == nil {
		return PlatformConfig{}, errors.New("all required fields must be present and non-null")
	}

	return PlatformConfig{
		Env:            *raw.Env,
		Region:         *raw.Region,
		Replicas:       *raw.Replicas,
		LeastPrivilege: *raw.LeastPrivilege,
		DRVerified:     *raw.DRVerified,
	}, nil
}

func evaluateGuardrails(cfg PlatformConfig) []string {
	var violations []string

	env := strings.TrimSpace(cfg.Env)
	region := strings.TrimSpace(cfg.Region)

	switch env {
	case "dev", "staging", "prod":
	default:
		violations = append(violations, "env must be one of: dev, staging, prod")
	}

	if region == "" {
		violations = append(violations, "region must not be empty or whitespace")
	}
	if cfg.Replicas < 0 {
		violations = append(violations, "replicas must not be negative")
	}
	if !cfg.LeastPrivilege {
		violations = append(violations, "least_privilege must be true")
	}

	if env == "prod" {
		if cfg.Replicas < 2 {
			violations = append(violations, "prod replicas must be >= 2 for high availability")
		}
		if !cfg.DRVerified {
			violations = append(violations, "prod dr_verified must be true")
		}
	}

	return violations
}

func validateConfig(ctx context.Context, path string) ([]string, error) {
	data, err := readBoundedFileWithContext(ctx, path, maxConfigBytes)
	if err != nil {
		return nil, err
	}

	cfg, err := parseStrictConfig(data)
	if err != nil {
		return nil, err
	}

	if err := ctx.Err(); err != nil {
		return nil, err
	}

	return evaluateGuardrails(cfg), nil
}

func run(ctx context.Context, configPath string) int {
	violations, err := validateConfig(ctx, configPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "RUNTIME ERROR: %v\n", err)
		return 2
	}

	if len(violations) > 0 {
		fmt.Fprintln(os.Stderr, "GUARDRAIL VIOLATIONS:")
		for _, v := range violations {
			fmt.Fprintf(os.Stderr, " - %s\n", v)
		}
		return 1
	}

	fmt.Println("GUARDRAIL PASSED: configuration meets production standards")
	return 0
}

func main() {
	configPath := "config.json"
	if len(os.Args) > 1 {
		configPath = os.Args[1]
	}

	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	os.Exit(run(ctx, configPath))
}
