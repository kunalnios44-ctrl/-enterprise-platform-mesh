package admission

import (
	"encoding/json"
	"fmt"
	"io"
	"mime"
	"net/http"
)

const maxRequestBodyBytes = 1 << 20 // 1 MiB

type AdmissionReview struct {
	APIVersion string             `json:"apiVersion"`
	Kind       string             `json:"kind"`
	Request    *AdmissionRequest  `json:"request,omitempty"`
	Response   *AdmissionResponse `json:"response,omitempty"`
}

type GroupVersionKind struct {
	Group   string `json:"group"`
	Version string `json:"version"`
	Kind    string `json:"kind"`
}

type AdmissionRequest struct {
	UID       string           `json:"uid"`
	Kind      GroupVersionKind `json:"kind"`
	Namespace string           `json:"namespace"`
	Operation string           `json:"operation"`
	Object    json.RawMessage  `json:"object"`
}

type AdmissionResponse struct {
	UID     string          `json:"uid"`
	Allowed bool            `json:"allowed"`
	Status  *ResponseStatus `json:"status,omitempty"`
}

type ResponseStatus struct {
	Code    int32  `json:"code"`
	Message string `json:"message"`
}

type podSpecExtract struct {
	Metadata struct {
		Name   string            `json:"name"`
		Labels map[string]string `json:"labels"`
	} `json:"metadata"`
	Spec struct {
		HostNetwork bool `json:"hostNetwork"`
		Containers  []struct {
			Name            string `json:"name"`
			SecurityContext *struct {
				Privileged *bool `json:"privileged"`
			} `json:"securityContext"`
			Resources struct {
				Limits map[string]string `json:"limits"`
			} `json:"resources"`
		} `json:"containers"`
	} `json:"spec"`
}

func ServeValidatingWebhook(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	mediaType, _, err := mime.ParseMediaType(r.Header.Get("Content-Type"))
	if err != nil || mediaType != "application/json" {
		http.Error(w, "content type must be application/json", http.StatusUnsupportedMediaType)
		return
	}

	body, err := io.ReadAll(io.LimitReader(r.Body, maxRequestBodyBytes+1))
	if err != nil {
		http.Error(w, "failed to read request body", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	if len(body) > maxRequestBodyBytes {
		http.Error(w, "admission review payload exceeds 1 MiB limit", http.StatusRequestEntityTooLarge)
		return
	}

	var review AdmissionReview
	if err := json.Unmarshal(body, &review); err != nil || review.Request == nil {
		http.Error(w, "invalid admission review payload", http.StatusBadRequest)
		return
	}

	if review.APIVersion != "admission.k8s.io/v1" || review.Kind != "AdmissionReview" {
		http.Error(w, "unsupported AdmissionReview apiVersion or kind", http.StatusBadRequest)
		return
	}

	allowed, reason := validateRequest(review.Request)

	resp := AdmissionReview{
		APIVersion: "admission.k8s.io/v1",
		Kind:       "AdmissionReview",
		Response: &AdmissionResponse{
			UID:     review.Request.UID,
			Allowed: allowed,
		},
	}
	if !allowed {
		resp.Response.Status = &ResponseStatus{
			Code:    http.StatusForbidden,
			Message: reason,
		}
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(resp); err != nil {
		http.Error(w, "failed to encode admission response", http.StatusInternalServerError)
	}
}

func validateRequest(req *AdmissionRequest) (bool, string) {
	if req.Kind.Group != "" || req.Kind.Version != "v1" || req.Kind.Kind != "Pod" {
		return true, ""
	}
	if req.Operation != "CREATE" && req.Operation != "UPDATE" {
		return true, ""
	}

	var pod podSpecExtract
	if err := json.Unmarshal(req.Object, &pod); err != nil {
		return false, fmt.Sprintf("unable to parse pod object: %v", err)
	}

	if pod.Spec.HostNetwork {
		if req.Namespace != "kube-system" || pod.Metadata.Labels["tier"] != "control-plane" {
			return false, "guardrail violation: hostNetwork requires kube-system namespace with tier=control-plane label"
		}
	}

	for _, c := range pod.Spec.Containers {
		if c.SecurityContext != nil && c.SecurityContext.Privileged != nil && *c.SecurityContext.Privileged {
			return false, fmt.Sprintf("guardrail violation: privileged container %q is forbidden", c.Name)
		}
		if len(c.Resources.Limits) == 0 && req.Namespace != "kube-system" {
			return false, fmt.Sprintf("guardrail violation: container %q must define resource limits", c.Name)
		}
	}

	return true, ""
}
