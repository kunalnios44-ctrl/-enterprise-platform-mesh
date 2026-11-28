package main

import (
	"context"
	"crypto/tls"
	"encoding/json"
	"errors"
	"flag"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/kunalnios44-ctrl/enterprise-platform-mesh/internal/admission"
	"github.com/kunalnios44-ctrl/enterprise-platform-mesh/internal/kernel"
)

func main() {
	var (
		ifaceName  = flag.String("iface", "eth0", "network interface for eBPF TC egress attachment")
		bpfObjPath = flag.String("bpf-obj", "/opt/chaos/chaos_tc.o", "path to compiled eBPF ELF object")
		listenAddr = flag.String("listen", ":8443", "HTTPS listen address for admission webhook")
		tlsCert    = flag.String("tls-cert", "/certs/tls.crt", "path to TLS certificate")
		tlsKey     = flag.String("tls-key", "/certs/tls.key", "path to TLS private key")
	)
	flag.Parse()

	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

	ctrl, err := kernel.LoadAndAttach(*bpfObjPath, *ifaceName)
	if err != nil {
		logger.Error("failed to initialize eBPF controller", "error", err)
		os.Exit(1)
	}

	defer func() {
		if closeErr := ctrl.Close(); closeErr != nil {
			logger.Error("failed to detach eBPF resources cleanly", "error", closeErr)
		}
	}()

	mux := http.NewServeMux()

	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}

		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte("ok"))
	})

	mux.HandleFunc("/validate", admission.ServeValidatingWebhook)

	mux.HandleFunc("/stats", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}

		stats, err := ctrl.ReadAggregatedStats()
		if err != nil {
			http.Error(w, "failed to read kernel stats", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")

		if err := json.NewEncoder(w).Encode(stats); err != nil {
			logger.Error("failed to encode kernel stats", "error", err)
		}
	})

	srv := &http.Server{
		Addr:              *listenAddr,
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       60 * time.Second,
		TLSConfig: &tls.Config{
			MinVersion: tls.VersionTLS13,
		},
	}

	ctx, stop := signal.NotifyContext(
		context.Background(),
		os.Interrupt,
		syscall.SIGTERM,
	)
	defer stop()

	go func() {
		logger.Info(
			"starting chaos-resilience agent",
			"addr", *listenAddr,
			"iface", *ifaceName,
		)

		if err := srv.ListenAndServeTLS(*tlsCert, *tlsKey); err != nil &&
			!errors.Is(err, http.ErrServerClosed) {
			logger.Error("https server failed", "error", err)
			stop()
		}
	}()

	<-ctx.Done()

	logger.Info("shutdown signal received, cleaning up")

	shutdownCtx, cancel := context.WithTimeout(
		context.Background(),
		10*time.Second,
	)
	defer cancel()

	if err := srv.Shutdown(shutdownCtx); err != nil {
		logger.Error("http server graceful shutdown error", "error", err)
	}
}
