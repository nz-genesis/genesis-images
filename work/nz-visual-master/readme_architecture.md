# Visual Master — Architecture Overview

**Status:** Canonical
**Audience:** Human operator / system architect
**Scope:** Project architecture, not AI execution

---

## Purpose

This document defines the **operational architecture** of Visual Master.
It exists to prevent role confusion, architectural drift, and unsafe modifications.

This file is **not** part of the runtime context and must **never** be loaded into an AI session.

---

## Core Principle

Visual Master is built as a **two-contour system**:

- **Development contour** — where thinking, validation, and evolution happen
- **Runtime contour** — where execution happens

These contours must never be merged.

---

## Contour 1: Development (SOURCE)

### Role

Development is the **single source of truth** for:
- methodology
- reasoning
- constraints derivation
- quality logic

It is allowed to be:
- verbose
- exploratory
- redundant
- iterative

### What belongs here

- Canonical method descriptions
- QC matrices
- Contracts and guides
- Governance rules
- Notes, history, discarded ideas
- **Embedding cores (SOURCE versions)**

### What does NOT belong here

- Frozen runtime artifacts
- Executable-only files without context

### Key rule

> **All changes originate in Development.**

Runtime is never edited directly.

---

## Contour 2: Runtime (FROZEN)

### Role

Runtime contains **only executable artifacts** required for AI operation.

It must be:
- minimal
- stable
- deterministic
- free of explanations

### What belongs here

- `01_system_prompt_execution_core.md`
- Exactly **one active embedding core** per task context

### What does NOT belong here

- Canonical texts
- QC documents
- Guides or contracts
- Governance or philosophy
- Examples or validation material

### Key rule

> **Runtime files are read-only.**

Any modification requires republishing from Development.

---

## Embedding Lifecycle

Embedding cores are the **primary product** of development work.

### SOURCE (Development)

- Editable
- May contain comments or TODOs
- Used for discussion and refinement

### FROZEN (Runtime)

- Exact copy of SOURCE at publish time
- No comments or explanations
- Versioned
- Treated as immutable

> **SOURCE → compile → FROZEN**

---

## System Prompt Lifecycle

The system prompt follows the same rule:

- Edited and discussed in Development
- Published as a frozen artifact in Runtime

The system prompt acts as:
- execution dispatcher
- module selector
- arbitration layer

It does **not** contain methodology details.

---

## Context Management Rule

Visual Master does **not** rely on large contextual memory.

At any time, work can continue using only:
- the system prompt
- the relevant embedding SOURCE or FROZEN

All other documents are optional and may be detached from active sessions.

---

## Deletion & Memory Safety

Documents may be removed from AI context if:
- their logic is already compiled into an embedding
- a version has been fixed

Embedding cores act as **state checkpoints**.

---

## Change Discipline

Forbidden actions:
- editing runtime files directly
- adding explanatory documents to runtime
- using examples as execution rules

Required actions:
- modify SOURCE
- recompile embedding
- republish runtime

---

## Final Statement

Visual Master is designed as an **AI operating system**, not a prompt collection.

Architecture exists to:
- reduce cognitive load
- prevent degradation over time
- enable safe scaling

This document defines **how the system is maintained**, not how it thinks.

---

**End of Architecture Overview**

