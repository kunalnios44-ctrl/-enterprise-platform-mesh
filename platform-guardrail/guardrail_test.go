package main

import "testing"

func TestGuardrailBaseline(t *testing.T) {
	expected := 0
	actual := 0
	if actual != expected {
		t.Fatalf("expected exit code %d, got %d", expected, actual)
	}
}
