# Operational Note — Face Replacement / Identity Substitution

Status: SOURCE
Role: Operational Note (Development)
Audience: Human operator / system architect

---

## Purpose

This note defines a **safe, deterministic workflow** for face replacement (identity substitution)
within the Visual Master architecture.

Face replacement is treated as a **deliberate identity override**, not a portrait task.

This note does not introduce new embeddings and does not modify runtime behavior.

---

## Conceptual Classification

Face replacement is:
- NOT identity preservation
- NOT portrait enhancement
- NOT style transfer

It is a **local identity substitution operation** applied to a specific subject
within an otherwise stable image.

---

## When to Use

Apply this workflow when:
- the user explicitly requests to replace a person’s face
- identity continuity of the original subject is NOT required
- the rest of the image must remain stable

Typical cases:
- actor replacement
- anonymization / de-identification
- character swap
- brand ambassador substitution

---

## Architectural Rules

### 1. Embedding Activation

- Portrait / Identity embedding MUST NOT be activated
- Style, Material, Layout embeddings MAY remain active
- Core-Only Mode governs identity logic

Identity preservation rules are intentionally suspended for the target subject only.

---

### 2. Reference Analysis Mode

If a replacement face reference is provided:
- activate Reference Analysis Mode
- analyze ONLY the incoming (replacement) identity
- extract stable identity traits

Do NOT analyze the original face for preservation.

---

## Validated Workflow

### Step A — Target Isolation

- identify the exact subject whose face is to be replaced
- treat identity substitution as **local**, not global

---

### Step B — Replacement Identity Anchor

Prepare a replacement identity anchor:
- text description (recommended)
- image reference (if available)

Rules:
- describe stable traits only
- no fidelity metrics
- no stylistic claims

---

### Step C — Structural Preservation

Preserve:
- head position
- body posture
- lighting direction
- scene composition

Only facial identity changes.

---

### Step D — Execution

Perform face replacement under Core-Only Mode.

Other active embeddings (style, layout, material, advertising) continue to constrain the image.

---

## Conflict Handling

If conflicts arise between:
- replacement identity
- lighting / pose / scene constraints

Resolution priority:
1. Structural coherence
2. Scene realism
3. Replacement identity fidelity

Disclosure is required if replacement fidelity is constrained.

---

## What This Workflow Avoids

- identity blending
- partial preservation of original traits
- unintended character drift
- global restyling

---

## Validation Notes

Empirically observed:
- higher stability when identity text + image reference are combined
- reduced artifacts when portrait embedding is explicitly excluded

---

## Placement and Lifecycle

This file is:
- operational only
- optional
- removable

It may later be merged into tooling or UI-level operations.

---

End of Operational Note

