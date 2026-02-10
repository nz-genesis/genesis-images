# nz-execution-gateway

## Role

**nz-execution-gateway** — STRICT enforcement & validation layer for Genesis execution requests.

This gateway is a **synchronous request-response proxy** that:
- Accepts execution requests via `POST /execute`
- Validates request structure (NOT business logic)
- Returns structured responses or errors
- Enforces architectural boundaries

## Invariants

1. **STRICTLY SYNCHRONOUS**: `request → execution → response` (no async, no callbacks, no polling)
2. **STATELESS**: No local state between requests (except replay protection cache)
3. **NO PERSISTENCE**: No local storage, databases, or file system writes
4. **NO BACKGROUND JOBS**: No workers, queues, or async processing
5. **NO RETRIES**: Single attempt execution model
6. **NO ORCHESTRATION**: Gateway is not a runtime or orchestrator
7. **NO GOROUTINES**: No concurrent execution paths per request

## Architecture

### State Machine

```
REQUEST_RECEIVED → VALIDATION → REJECTED (any error) / SANDBOX_CREATED
SANDBOX_CREATED → EXECUTION → SANDBOX_DESTROYED
SANDBOX_DESTROYED → RESPONSE
```

### Validation Pipeline (Fixed Order)

Validation occurs in this strict order with REJECT on first error:

1. **Schema Validation** — JSON structure vs EXECUTION_REQUEST_SCHEMA
2. **Context Validation** (R-CTX-XXX) — tenant_id, subject_id, trace_id
3. **Intent Validation** (R-INTENT-XXX) — intent_id, intent_version
4. **Security Validation** (R-SEC-XXX) — network, privileged access, secrets
5. **Sandbox Validation** (R-SBX-XXX) — profile, network, filesystem
6. **Resources Validation** (R-RES-XXX) — cpu, memory, timeout
7. **State Validation** (R-STATE-XXX) — replay detection

## Rejection Codes (DENIAL_MATRIX)

| Category | Codes |
|----------|-------|
| R-CTX-XXX | 001 (missing tenant_id), 002 (missing subject_id), 003 (missing trace_id), 004 (workspace mismatch) |
| R-INTENT-XXX | 001 (missing intent_id), 002 (unknown intent_id), 003 (version mismatch), 004 (intent closed) |
| R-SCHEMA-XXX | 001 (invalid JSON), 002 (unknown fields), 003 (missing mandatory fields) |
| R-SEC-XXX | 001 (network forbidden), 002 (privileged without approval), 003 (secrets access) |
| R-SBX-XXX | 001 (invalid profile), 002 (profile escalation) |
| R-RES-XXX | 001 (cpu missing), 002 (memory missing), 003 (timeout missing), 004 (exceeds policy) |
| R-STATE-XXX | 001 (already consumed), 002 (replay detected), 003 (mutation detected), 004 (chained execution) |

## Sandbox Lifecycle

```
create_sandbox(profile) → exec(target, params) → destroy_sandbox()
```

### Sandbox Profiles

| Profile | Restrictions |
|---------|--------------|
| `default` | Non-root execution, basic environment isolation |
| `restricted` | Non-root, dropped capabilities, PATH restrictions, HOME=/tmp |
| `privileged` | REJECTED (requires explicit approval) |

### Enforcement Applied

- Non-root user execution
- Dropped Linux capabilities
- CPU and memory limits (via cgroups)
- Timeout enforcement
- Ephemeral filesystem
- Network disabled by default

## Audit Logging

The gateway logs ONLY audit metadata (NO payload dumping):

```json
{
  "execution_request_id": "uuid",
  "intent_id": "uuid",
  "tenant_id": "uuid",
  "subject_id": "uuid",
  "trace_id": "uuid",
  "sandbox_profile": "default",
  "rejection_code": "R-XXX-YYY",
  "exit_code": 0,
  "started_at": "RFC3339",
  "finished_at": "RFC3339"
}
```

## API

### POST /execute

**Request** (EXECUTION_REQUEST_SCHEMA):

```json
{
  "execution_request_id": "uuid",
  "execution_request_version": "1.0",
  "intent_ref": {
    "intent_id": "uuid",
    "intent_version": "1.0",
    "trace_id": "uuid"
  },
  "execution_spec": {
    "executor": "execution",
    "target": "echo 'hello'",
    "parameters": {}
  },
  "context": {
    "tenant_id": "uuid",
    "subject_id": "uuid",
    "workspace_id": "uuid",
    "trace_id": "uuid"
  },
  "sandbox": {
    "profile": "default",
    "network": "disabled",
    "filesystem": "ephemeral"
  },
  "resources": {
    "cpu": "500m",
    "memory": "128Mi",
    "timeout_ms": 30000
  },
  "artifacts": {
    "capture_stdout": true,
    "capture_stderr": true,
    "output_files": [],
    "persist": false
  },
  "audit": {
    "execution_trace_id": "uuid",
    "parent_trace_id": "uuid",
    "requested_by": "orchestrator",
    "timestamp": "RFC3339"
  }
}
```

**Rejection Response** (HTTP 403):

```json
{
  "execution_request_id": "uuid",
  "status": "rejected",
  "rejection_code": "R-XXX-YYY",
  "reason": "human-readable reason",
  "trace_id": "uuid",
  "timestamp": "RFC3339"
}
```

**Success Response** (HTTP 200):

```json
{
  "execution_request_id": "uuid",
  "status": "success | error",
  "exit_code": 0 или ненулевой,
  "stdout": "captured output",
  "stderr": "captured error output",
  "artifacts": ["uri"],
  "started_at": "RFC3339",
  "finished_at": "RFC3339"
}
```

### GET /health

Returns `{"status": "healthy"}` with HTTP 200.

## Forbidden Behavior

The gateway MUST NOT:

- ❌ Attempt auto-correction of requests
- ❌ Retry rejected requests
- ❌ Escalate privileges
- ❌ Mutate requests
- ❌ Emit side-effects beyond sandbox execution
- ❌ Log request payloads
- ❌ Use goroutines for request execution
- ❌ Use queues or worker pools

## Build & Run

```bash
# Build
docker build -t nz-execution-gateway .

# Run
docker run -p 8080:8080 nz-execution-gateway

# Test health
curl http://localhost:8080/health

# Test execution
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

## Dependencies

- Go 1.21+
- `github.com/google/uuid` for UUID generation

## Version

1.0.0 — GENESIS Phase 3.3 Execution Gateway
