package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/google/uuid"
)

// =============================================================================
// CONSTANTS & REJECTION CODES
// =============================================================================

const (
	// Version
	Version = "1.0.0"

	// State Machine States
	StateRequestReceived   = "REQUEST_RECEIVED"
	StateValidation        = "VALIDATION"
	StateRejected          = "REJECTED"
	StateSandboxCreated    = "SANDBOX_CREATED"
	StateExecution         = "EXECUTION"
	StateSandboxDestroyed  = "SANDBOX_DESTROYED"
	StateResponse          = "RESPONSE"

	// Sandbox Profiles
	ProfileDefault     = "default"
	ProfileRestricted  = "restricted"
	ProfilePrivileged  = "privileged"

	// Network Modes
	NetworkDisabled   = "disabled"
	NetworkRestricted = "restricted"
)

// Rejection Codes - DENIAL_MATRIX
const (
	// R-CTX - Context Violations
	RCTX001 = "R-CTX-001" // Missing tenant_id
	RCTX002 = "R-CTX-002" // Missing subject_id
	RCTX003 = "R-CTX-003" // Missing trace_id
	RCTX004 = "R-CTX-004" // Workspace mismatch

	// R-INTENT - Intent Reference Violations
	RINTENT001 = "R-INTENT-001" // Missing intent_id
	RINTENT002 = "R-INTENT-002" // Unknown intent_id
	RINTENT003 = "R-INTENT-003" // Intent version mismatch
	RINTENT004 = "R-INTENT-004" // Intent already closed

	// R-SCHEMA - Schema Violations
	RSCHEMA001 = "R-SCHEMA-001" // Payload not matching schema
	RSCHEMA002 = "R-SCHEMA-002" // Unknown fields present
	RSCHEMA003 = "R-SCHEMA-003" // Missing mandatory fields

	// R-SEC - Security Violations
	RSEC001 = "R-SEC-001" // Network access requested but forbidden
	RSEC002 = "R-SEC-002" // Privileged sandbox requested without approval
	RSEC003 = "R-SEC-003" // Attempt to access secrets

	// R-SBX - Sandbox Violations
	RSBX001 = "R-SBX-001" // Invalid sandbox profile
	RSBX002 = "R-SBX-002" // Sandbox profile escalation

	// R-RES - Resource Violations
	RRES001 = "R-RES-001" // CPU limit missing
	RRES002 = "R-RES-002" // Memory limit missing
	RRES003 = "R-RES-003" // Timeout missing
	RRES004 = "R-RES-004" // Resource limits exceed policy

	// R-STATE - Lifecycle Violations
	RSTATE001 = "R-STATE-001" // Execution request already consumed
	RSTATE002 = "R-STATE-002" // Replay attempt detected
	RSTATE003 = "R-STATE-003" // Mutation detected
	RSTATE004 = "R-STATE-004" // Chained execution attempt
)

// =============================================================================
// DATA STRUCTURES
// =============================================================================

// ExecutionRequest represents the canonical execution request
type ExecutionRequest struct {
	ExecutionRequestID     string              `json:"execution_request_id"`
	ExecutionRequestVersion string             `json:"execution_request_version"`
	IntentRef              IntentRef           `json:"intent_ref"`
	ExecutionSpec          ExecutionSpec       `json:"execution_spec"`
	Context                Context             `json:"context"`
	Sandbox                Sandbox             `json:"sandbox"`
	Resources              Resources           `json:"resources"`
	Artifacts              Artifacts           `json:"artifacts"`
	Audit                  Audit               `json:"audit"`
}

type IntentRef struct {
	IntentID       string `json:"intent_id"`
	IntentVersion string `json:"intent_version"`
	TraceID       string `json:"trace_id"`
}

type ExecutionSpec struct {
	Executor    string                 `json:"executor"`
	Target      string                 `json:"target"`
	Parameters  map[string]interface{}  `json:"parameters"`
}

type Context struct {
	TenantID     string `json:"tenant_id"`
	SubjectID    string `json:"subject_id"`
	WorkspaceID  string `json:"workspace_id,omitempty"`
	TraceID      string `json:"trace_id"`
}

type Sandbox struct {
	ID        string     `json:"id"`
	Profile    string     `json:"profile"`
	Network    string     `json:"network"`
	Filesystem string     `json:"filesystem"`
	Cmd        *exec.Cmd  `json:"-"`
	Finished  bool       `json:"finished"`
}

type Resources struct {
	CPU      string `json:"cpu"`
	Memory   string `json:"memory"`
	Timeout  int    `json:"timeout_ms"`
}

type Artifacts struct {
	CaptureStdout   bool     `json:"capture_stdout"`
	CaptureStderr   bool     `json:"capture_stderr"`
	OutputFiles    []string `json:"output_files"`
	Persist        bool     `json:"persist"`
}

type Audit struct {
	ExecutionTraceID string `json:"execution_trace_id"`
	ParentTraceID    string `json:"parent_trace_id"`
	RequestedBy      string `json:"requested_by"`
	Timestamp        string `json:"timestamp"`
}

// RejectionResponse represents the rejection response
type RejectionResponse struct {
	ExecutionRequestID string `json:"execution_request_id"`
	Status             string `json:"status"`
	RejectionCode      string `json:"rejection_code"`
	Reason             string `json:"reason"`
	TraceID            string `json:"trace_id"`
	Timestamp          string `json:"timestamp"`
}

// SuccessResponse represents the success response
type SuccessResponse struct {
	ExecutionRequestID string   `json:"execution_request_id"`
	Status             string   `json:"status"`
	ExitCode           int      `json:"exit_code"`
	Stdout             string   `json:"stdout,omitempty"`
	Stderr             string   `json:"stderr,omitempty"`
	Artifacts          []string `json:"artifacts,omitempty"`
	StartedAt          string   `json:"started_at"`
	FinishedAt         string   `json:"finished_at"`
}

// ExecutionState tracks the current state of execution
type ExecutionState struct {
	CurrentState        string
	Request             *ExecutionRequest
	RejectionCode       string
	RejectionReason     string
	ExitCode            int
	Stdout              string
	Stderr              string
	StartedAt           time.Time
	FinishedAt          time.Time
}

// =============================================================================
// STATE MACHINE
// =============================================================================

func NewExecutionState(req *ExecutionRequest) *ExecutionState {
	return &ExecutionState{
		CurrentState: StateRequestReceived,
		Request:      req,
		StartedAt:    time.Now().UTC(),
	}
}

func (s *ExecutionState) Transition(newState string) {
	s.CurrentState = newState
}

func (s *ExecutionState) TransitionToValidation() {
	s.Transition(StateValidation)
}

func (s *ExecutionState) TransitionToRejected(code, reason string) {
	s.RejectionCode = code
	s.RejectionReason = reason
	s.Transition(StateRejected)
	s.FinishedAt = time.Now().UTC()
}

func (s *ExecutionState) TransitionToSandboxCreated() {
	s.Transition(StateSandboxCreated)
}

func (s *ExecutionState) TransitionToExecution() {
	s.Transition(StateExecution)
}

func (s *ExecutionState) TransitionToSandboxDestroyed() {
	s.Transition(StateSandboxDestroyed)
}

func (s *ExecutionState) TransitionToResponse() {
	s.Transition(StateResponse)
	s.FinishedAt = time.Now().UTC()
}

// =============================================================================
// VALIDATION PIPELINE
// =============================================================================

type ValidationResult struct {
	Rejected      bool
	RejectionCode string
	RejectionReason string
}

func (state *ExecutionState) Validate() *ValidationResult {
	// Fixed order: Schema → Context → Intent → Security → Sandbox → Resources → State
	
	// 1. Schema Validation
	if result := state.validateSchema(); result.Rejected {
		return result
	}
	
	// 2. Context Validation (R-CTX-XXX)
	if result := state.validateContext(); result.Rejected {
		return result
	}
	
	// 3. Intent Validation (R-INTENT-XXX)
	if result := state.validateIntent(); result.Rejected {
		return result
	}
	
	// 4. Security Validation (R-SEC-XXX)
	if result := state.validateSecurity(); result.Rejected {
		return result
	}
	
	// 5. Sandbox Validation (R-SBX-XXX)
	if result := state.validateSandbox(); result.Rejected {
		return result
	}
	
	// 6. Resources Validation (R-RES-XXX)
	if result := state.validateResources(); result.Rejected {
		return result
	}
	
	// 7. State Validation (R-STATE-XXX)
	if result := state.validateState(); result.Rejected {
		return result
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateSchema() *ValidationResult {
	req := state.Request
	
	// Check required fields presence
	if req.ExecutionRequestID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: execution_request_id"}
	}
	if req.IntentRef.IntentID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: intent_ref.intent_id"}
	}
	if req.IntentRef.IntentVersion == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: intent_ref.intent_version"}
	}
	if req.ExecutionSpec.Executor == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: execution_spec.executor"}
	}
	if req.ExecutionSpec.Target == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: execution_spec.target"}
	}
	if req.Context.TenantID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: context.tenant_id"}
	}
	if req.Context.SubjectID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: context.subject_id"}
	}
	if req.Context.TraceID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: context.trace_id"}
	}
	if req.Sandbox.Profile == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: sandbox.profile"}
	}
	if req.Resources.CPU == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: resources.cpu"}
	}
	if req.Resources.Memory == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: resources.memory"}
	}
	if req.Resources.Timeout == 0 {
		return &ValidationResult{Rejected: true, RejectionCode: RSCHEMA003, RejectionReason: "Missing mandatory field: resources.timeout_ms"}
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateContext() *ValidationResult {
	req := state.Request
	
	if req.Context.TenantID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RCTX001, RejectionReason: "Missing tenant_id"}
	}
	if req.Context.SubjectID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RCTX002, RejectionReason: "Missing subject_id"}
	}
	if req.Context.TraceID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RCTX003, RejectionReason: "Missing trace_id"}
	}
	
	// Validate UUID format
	if !isValidUUID(req.Context.TenantID) {
		return &ValidationResult{Rejected: true, RejectionCode: RCTX001, RejectionReason: "Invalid tenant_id format"}
	}
	if !isValidUUID(req.Context.SubjectID) {
		return &ValidationResult{Rejected: true, RejectionCode: RCTX002, RejectionReason: "Invalid subject_id format"}
	}
	if !isValidUUID(req.Context.TraceID) {
		return &ValidationResult{Rejected: true, RejectionCode: RCTX003, RejectionReason: "Invalid trace_id format"}
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateIntent() *ValidationResult {
	req := state.Request
	
	if req.IntentRef.IntentID == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RINTENT001, RejectionReason: "Missing intent_id"}
	}
	if !isValidUUID(req.IntentRef.IntentID) {
		return &ValidationResult{Rejected: true, RejectionCode: RINTENT001, RejectionReason: "Invalid intent_id format"}
	}
	
	// Validate intent version format (e.g., "1.0")
	if !isValidVersion(req.IntentRef.IntentVersion) {
		return &ValidationResult{Rejected: true, RejectionCode: RINTENT003, RejectionReason: "Invalid intent_version format"}
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateSecurity() *ValidationResult {
	req := state.Request
	
	// R-SEC-001: Network access requested but forbidden
	if req.Sandbox.Network != "" && req.Sandbox.Network != NetworkDisabled {
		return &ValidationResult{Rejected: true, RejectionCode: RSEC001, RejectionReason: "Network access requested but forbidden by policy"}
	}
	
	// R-SEC-002: Privileged sandbox requested without approval
	if req.Sandbox.Profile == ProfilePrivileged {
		return &ValidationResult{Rejected: true, RejectionCode: RSEC002, RejectionReason: "Privileged sandbox requested without approval"}
	}
	
	// R-SEC-003: Attempt to access secrets
	// Check parameters for secret-like patterns
	paramsJSON, _ := json.Marshal(req.ExecutionSpec.Parameters)
	paramsStr := string(paramsJSON)
	if containsSecretsPatterns(paramsStr) {
		return &ValidationResult{Rejected: true, RejectionCode: RSEC003, RejectionReason: "Attempt to access secrets detected"}
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateSandbox() *ValidationResult {
	req := state.Request
	
	// R-SBX-001: Invalid sandbox profile
	validProfiles := map[string]bool{
		ProfileDefault: true,
		ProfileRestricted: true,
		ProfilePrivileged: false, // Handled in security validation
	}
	
	if !validProfiles[req.Sandbox.Profile] {
		return &ValidationResult{Rejected: true, RejectionCode: RSBX001, RejectionReason: fmt.Sprintf("Invalid sandbox profile: %s", req.Sandbox.Profile)}
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateResources() *ValidationResult {
	req := state.Request
	
	// R-RES-001: CPU limit missing
	if req.Resources.CPU == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RRES001, RejectionReason: "Missing CPU limit"}
	}
	
	// R-RES-002: Memory limit missing
	if req.Resources.Memory == "" {
		return &ValidationResult{Rejected: true, RejectionCode: RRES002, RejectionReason: "Missing memory limit"}
	}
	
	// R-RES-003: Timeout missing
	if req.Resources.Timeout == 0 {
		return &ValidationResult{Rejected: true, RejectionCode: RRES003, RejectionReason: "Missing timeout"}
	}
	
	// R-RES-004: Resource limits exceed policy
	if !isWithinPolicyLimits(req.Resources.CPU, req.Resources.Memory, req.Resources.Timeout) {
		return &ValidationResult{Rejected: true, RejectionCode: RRES004, RejectionReason: "Resource limits exceed policy"}
	}
	
	return &ValidationResult{Rejected: false}
}

func (state *ExecutionState) validateState() *ValidationResult {
	req := state.Request
	
	// R-STATE-002: Replay attempt detection
	// Check if execution_request_id was already used (in-memory cache for demo)
	if usedRequests.Contains(req.ExecutionRequestID) {
		return &ValidationResult{Rejected: true, RejectionCode: RSTATE002, RejectionReason: "Replay attempt detected"}
	}
	
	// R-STATE-004: Chained execution attempt
	// Verify intent_ref.trace_id matches context.trace_id
	if req.IntentRef.TraceID != req.Context.TraceID {
		return &ValidationResult{Rejected: true, RejectionCode: RSTATE004, RejectionReason: "Chained execution attempt detected"}
	}
	
	return &ValidationResult{Rejected: false}
}

// =============================================================================
// SANDBOX LIFECYCLE
// =============================================================================

func createSandbox(profile string, spec ExecutionSpec, resources Resources) (*Sandbox, error) {
	sandbox := &Sandbox{
		ID:      uuid.New().String(),
		Profile: profile,
	}
	
	// Build command based on executor and target
	// This is a simplified implementation - real implementation would use
	// containerization (Docker/LXC) or gVisor for full sandbox isolation
	
	var cmd *exec.Cmd
	
	switch spec.Executor {
	case "execution":
		// Execute target as command
		// Parameters may contain command arguments
		args := []string{"-c", spec.Target}
		if paramsArgs, ok := spec.Parameters["args"].([]interface{}); ok {
			for _, a := range paramsArgs {
				if arg, ok := a.(string); ok {
					args = append(args, arg)
				}
			}
		}
		cmd = exec.Command("/bin/sh", args...)
	default:
		// Generic executor - use shell to interpret
		cmd = exec.Command("/bin/sh", "-c", spec.Target)
	}
	
	// Apply sandbox restrictions
	if profile == ProfileRestricted {
		// Apply restrictions via shell commands
		cmd.Env = append(os.Environ(),
			"PATH=/usr/bin:/bin",
			"HOME=/tmp",
			"USER=nobody",
		)
	} else {
		// Default profile - minimal restrictions
		cmd.Env = append(os.Environ(),
			"HOME=/tmp",
		)
	}
	
	// Set working directory to ephemeral location
	cmd.Dir = "/tmp"
	
	sandbox.Cmd = cmd
	return sandbox, nil
}

func (s *Sandbox) Execute() (int, string, string, error) {
	// Execute the command with resource limits applied via system calls
	// In a real implementation, this would use cgroups, namespaces, etc.
	
	stdout, err := s.Cmd.Output()
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			return exitErr.ExitCode(), "", string(exitErr.Stderr), nil
		}
		return -1, "", "", err
	}
	
	return 0, string(stdout), "", nil
}

func (s *Sandbox) Destroy() error {
	// Clean up sandbox resources
	// In a real implementation, this would destroy containers/namespaces
	s.Finished = true
	return nil
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

func isValidUUID(s string) bool {
	_, err := uuid.Parse(s)
	return err == nil
}

func isValidVersion(v string) bool {
	parts := strings.Split(v, ".")
	if len(parts) != 2 {
		return false
	}
	for _, p := range parts {
		for _, c := range p {
			if c < '0' || c > '9' {
				return false
			}
		}
	}
	return true
}

func isWithinPolicyLimits(cpu, memory string, timeout int) bool {
	// Policy limits - can be made configurable
	maxCPU := "2000m"      // 2 CPU cores
	maxMemory := "512Mi"   // 512 MB
	maxTimeout := 300000   // 5 minutes in ms
	
	// Simple string comparison for demo
	// Real implementation would parse and compare properly
	if cpu != "" && cpu > maxCPU {
		return false
	}
	if memory != "" && memory > maxMemory {
		return false
	}
	if timeout > maxTimeout {
		return false
	}
	
	return true
}

func containsSecretsPatterns(s string) bool {
	patterns := []string{
		"password",
		"secret",
		"api_key",
		"private_key",
		"credential",
	}
	
	lower := strings.ToLower(s)
	for _, pattern := range patterns {
		if strings.Contains(lower, pattern) {
			return true
		}
	}
	return false
}

// UsedRequests tracks consumed request IDs for replay detection
var usedRequests = &RequestCache{
	requests: make(map[string]time.Time),
}

// RequestCache provides simple replay detection
type RequestCache struct {
	requests map[string]time.Time
}

func (c *RequestCache) Contains(id string) bool {
	_, ok := c.requests[id]
	return ok
}

func (c *RequestCache) Add(id string) {
	c.requests[id] = time.Now()
}

func (c *RequestCache) RemoveExpired() {
	// Cleanup expired entries (older than 24 hours)
	cutoff := time.Now().Add(-24 * time.Hour)
	for id, t := range c.requests {
		if t.Before(cutoff) {
			delete(c.requests, id)
		}
	}
}

// =============================================================================
// AUDIT LOGGING
// =============================================================================

type AuditEntry struct {
	ExecutionRequestID string `json:"execution_request_id"`
	IntentID           string `json:"intent_id"`
	TenantID           string `json:"tenant_id"`
	SubjectID          string `json:"subject_id"`
	TraceID            string `json:"trace_id"`
	SandboxProfile     string `json:"sandbox_profile"`
	RejectionCode      string `json:"rejection_code,omitempty"`
	ExitCode           int    `json:"exit_code,omitempty"`
	StartedAt          string `json:"started_at"`
	FinishedAt         string `json:"finished_at"`
}

func (state *ExecutionState) ToAuditEntry() *AuditEntry {
	entry := &AuditEntry{
		ExecutionRequestID: state.Request.ExecutionRequestID,
		IntentID:           state.Request.IntentRef.IntentID,
		TenantID:           state.Request.Context.TenantID,
		SubjectID:          state.Request.Context.SubjectID,
		TraceID:            state.Request.Context.TraceID,
		SandboxProfile:     state.Request.Sandbox.Profile,
		StartedAt:          state.StartedAt.Format(time.RFC3339),
		FinishedAt:         state.FinishedAt.Format(time.RFC3339),
	}
	
	if state.RejectionCode != "" {
		entry.RejectionCode = state.RejectionCode
	}
	
	entry.ExitCode = state.ExitCode
	
	return entry
}

func logAudit(entry *AuditEntry) {
	// Audit-only logging - NO payload dumping
	// In production, this would write to a secure audit log
	auditJSON, _ := json.Marshal(entry)
	fmt.Fprintf(os.Stderr, "[AUDIT] %s\n", string(auditJSON))
}

// =============================================================================
// HTTP HANDLERS
// =============================================================================

func handleExecute(w http.ResponseWriter, r *http.Request) {
	requestID := uuid.New().String()
	
	// Read request body
	var req ExecutionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		sendRejection(w, requestID, RSCHEMA001, "Invalid JSON payload")
		return
	}
	
	// Initialize state machine
	state := NewExecutionState(&req)
	state.TransitionToValidation()
	
	// Run validation pipeline (fixed order)
	result := state.Validate()
	if result.Rejected {
		state.TransitionToRejected(result.RejectionCode, result.RejectionReason)
		logAudit(state.ToAuditEntry())
		sendRejection(w, state.Request.ExecutionRequestID, state.RejectionCode, state.RejectionReason)
		return
	}
	
	// Mark request as used (replay protection)
	usedRequests.Add(req.ExecutionRequestID)
	
	// Create sandbox
	state.TransitionToSandboxCreated()
	sandbox, err := createSandbox(req.Sandbox.Profile, req.ExecutionSpec, req.Resources)
	if err != nil {
		state.TransitionToRejected("R-SBX-001", fmt.Sprintf("Failed to create sandbox: %v", err))
		logAudit(state.ToAuditEntry())
		sendRejection(w, state.Request.ExecutionRequestID, state.RejectionCode, state.RejectionReason)
		return
	}
	
	// Execute
	state.TransitionToExecution()
	exitCode, stdout, stderr, err := sandbox.Execute()
	state.ExitCode = exitCode
	state.Stdout = stdout
	state.Stderr = stderr
	
	// Destroy sandbox
	state.TransitionToSandboxDestroyed()
	sandbox.Destroy()
	
	// Response
	state.TransitionToResponse()
	logAudit(state.ToAuditEntry())
	sendSuccess(w, state)
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status": "healthy"}`))
}

func sendRejection(w http.ResponseWriter, requestID, code, reason string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusForbidden)
	
	response := RejectionResponse{
		ExecutionRequestID: requestID,
		Status:             "rejected",
		RejectionCode:      code,
		Reason:             reason,
		TraceID:            uuid.New().String(),
		Timestamp:         time.Now().UTC().Format(time.RFC3339),
	}
	
	json.NewEncoder(w).Encode(response)
}

func sendSuccess(w http.ResponseWriter, state *ExecutionState) {
	w.Header().Set("Content-Type", "application/json")
	
	var status string
	if state.ExitCode == 0 {
		status = "success"
	} else {
		status = "error"
	}
	
	response := SuccessResponse{
		ExecutionRequestID: state.Request.ExecutionRequestID,
		Status:             status,
		ExitCode:           state.ExitCode,
		StartedAt:          state.StartedAt.Format(time.RFC3339),
		FinishedAt:         state.FinishedAt.Format(time.RFC3339),
	}
	
	if state.Request.Artifacts.CaptureStdout {
		response.Stdout = state.Stdout
	}
	if state.Request.Artifacts.CaptureStderr {
		response.Stderr = state.Stderr
	}
	
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// =============================================================================
// MAIN
// =============================================================================

func main() {
	// Start cleanup goroutine for expired requests (ONLY for state cleanup)
	// Note: This is the ONLY allowed goroutine - for maintenance, not execution
	go func() {
		ticker := time.NewTicker(1 * time.Hour)
		defer ticker.Stop()
		for range ticker.C {
			usedRequests.RemoveExpired()
		}
	}()
	
	// Register handlers
	http.HandleFunc("/execute", handleExecute)
	http.HandleFunc("/health", handleHealth)
	
	// Start server
	fmt.Println("nz-execution-gateway starting on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Fprintf(os.Stderr, "Server error: %v\n", err)
		os.Exit(1)
	}
}
