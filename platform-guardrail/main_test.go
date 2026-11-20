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

type PlatformConfig struct {
	Env            string `json:"env"`
	Region         string `json:"region"`
	Replicas       int    `json:"replicas"`
	LeastPrivilege bool   `json:"least_privilege"`
	DRVerified     bool   `json:"dr_verified"`
}

func readFileWithContext(ctx context.Context, path string) ([]byte, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}

	type readResult struct {
		data []byte
		err  error
	}

	ch := make(chan readResult, 1)
	go func() {
		f, err := os.Open(path)
		if err != nil {
			ch <- readResult{err: err}
			return
		}
		defer f.Close()

		data, err := io.ReadAll(f)
		ch <- readResult{data: data, err: err}
	}()

	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	case res := <-ch:
		if err := ctx.Err(); err != nil {
			return nil, err
		}
		return res.data, res.err
	}
}

func parseStrictJSON(data []byte) (PlatformConfig, error) {
	var cfg PlatformConfig
	dec := json.NewDecoder(bytes.NewReader(data))
	dec.DisallowUnknownFields()

	if err := dec.Decode(&cfg); err != nil {
		return PlatformConfig{}, err
  }
  
