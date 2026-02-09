# Development Contour — README

Status: DEV / SOURCE  
Audience: System architect, developer  
Scope: Development-only architecture, reasoning, and evolution  
Not for runtime use

---

## Purpose

The Development contour is the **single source of truth** for how Visual Master is designed,
reasoned, validated, and evolved.

Nothing in this contour is intended for direct AI runtime execution.

Development exists to:
- derive constraints and behavior,
- reason about visual logic,
- validate architectural decisions,
- compile executable artifacts for Runtime,
- prevent long-term system drift.

---

## Two-Contour Architecture (Critical)

Visual Master is split into two strictly separated contours:

### 1. Development (DEV)

- exploratory
- explanatory
- iterative
- editable

This is where:
- rules are reasoned,
- constraints are derived,
- embeddings are designed,
- quality logic is validated.

### 2. Runtime (PROD)

- minimal
- deterministic
- executable
- immutable

Runtime contains **only compiled artifacts** and must never include:
- philosophy,
- explanations,
- guides,
- examples,
- SOURCE files.

> Any change in Runtime must originate in Development.

---

## Folder Responsibilities

### `core/`

Contains SOURCE versions of:
- system prompt,
- execution logic,
- canonical reasoning structures.

These files:
- may be verbose,
- may include explanations,
- are compiled into frozen runtime artifacts.

---

### `context/`

Contains **context-of-use classification**.

Purpose:
- define professional production contexts,
- describe expectations of different visual domains,
- guide intent interpretation and QC.

Key properties:
- NOT executable
- NOT embeddings
- NOT loadable at runtime
- do not add or modify behavior

Example:
- `context_of_use_visual_types.md`

---

### `contextual_modules/`

Contains **contextual logic extensions**.

Purpose:
- extend or constrain execution behavior,
- formalize domain-specific logic,
- serve as candidates for embeddings.

Properties:
- may affect reasoning and constraints,
- loaded only when relevant,
- never override Execution Core.

Examples:
- portrait
- advertising
- material-volume-method

---

### `governance/`

Contains rules that protect system integrity.

Includes:
- change discipline,
- disclosure rules,
- safety constraints.

These files define what is allowed or forbidden
when modifying the system.

---

## What Is NOT Allowed in Development

Forbidden:
- editing runtime files directly,
- placing executable logic outside `core/` or `contextual_modules/`,
- turning classifications into embeddings,
- loading DEV files into runtime contexts.

If in doubt:
- keep the file in Development,
- do not simulate runtime behavior.

---

## Embeddings vs Context (Non-Negotiable)

**Context-of-use**:
- describes *what kind of visual work this is*,
- affects interpretation and QC,
- never changes execution logic.

**Contextual modules / embeddings**:
- constrain *how the system behaves*,
- may override stylistic freedom,
- may block or enforce decisions.

Confusing these two leads to architectural failure.

---

## Change Discipline

All changes follow this path:

1. Modify or add SOURCE files in Development
2. Reason and validate changes conceptually
3. Update embedding SOURCE if behavior changes
4. Compile executable artifacts
5. Publish frozen artifacts to Runtime

Direct Runtime edits are forbidden.

---

## Design Philosophy (Compact)

- Meaning precedes form
- Observability over abstraction
- One dominant idea per visual
- Professional human standards over novelty
- Stability over expressiveness when in conflict

---

## Final Rule

Development is allowed to be:
- verbose,
- redundant,
- exploratory.

Runtime is not.

If a file explains **why** — it belongs here.  
If a file enforces **how** — it may become runtime.

---

End of Development README
