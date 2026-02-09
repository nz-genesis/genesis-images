# VISUAL MASTER — ARCHITECTURE README

Status: CANONICAL  
Role: Architectural Reference  
Scope: System Overview and Governance

---

## System Status

Visual Master is a single-intelligence visual system
with a locked production architecture.

Execution Core, embeddings, and runtime profiles are frozen.

---

## Core Principles

- One Execution Core
- Behavior over data
- Meaning before generation
- Tools as adapters, not decision-makers
- Professional literacy by default
- Strict separation of DEV and PROD

---

## Architecture Overview

assistant/
├─ core/
│  └─ 01_system_prompt_execution_core.md
├─ embeddings/
│  ├─ portrait_embedding_core.md
│  ├─ advertising_branding_embedding_core.md
│  ├─ layout_composition_embedding_core.md
│  ├─ style_embedding_core.md
│  └─ mvm_embedding_core.md
├─ runtime_profile.md
└─ PROD_MINIMAL_PACK.md

---

## Development vs Production

DEV:
- analysis,
- context,
- reference,
- QC,
- protocols.

PROD:
- Execution Core,
- embeddings,
- runtime profile.

DEV artifacts never load at runtime.

---

## Change Policy

- Core changes require a new version.
- Embeddings must not conflict with Core.
- Runtime profiles affect interaction only.

---

End of Architecture README
