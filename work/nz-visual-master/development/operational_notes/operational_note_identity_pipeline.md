# Operational Note — Identity-Critical Visual Pipeline

Status: SOURCE
Role: Operational Note (Development)
Audience: Human operator / system architect

---

## Purpose

This note captures a **validated best-practice pipeline** for identity‑critical visual tasks across heterogeneous generators.
It is **non‑canonical** and does not override core philosophy, pipeline, or embeddings.

---

## When to Use

Apply this pipeline when **identity continuity matters**, including:
- brand faces / ambassadors
- recurring characters
- face replacement or transfer
- cross‑tool consistency requirements

---

## Pipeline (Validated)

### Step A — Semantic Identity Anchor (Text)
Create a compact, neutral description of **stable traits**:
- age range
- hair / hairline
- skin tone
- eye color
- baseline expression
- psychological presence (calm, grounded, reserved)

Rules:
- no beauty claims
- no geometric anatomy lists
- no technical fidelity metrics

Outcome: **Portable identity text**.

---

### Step B — Baseline Generation (Flux)
Generate without visual references using the text anchor.

Goals:
- produce a **specific, consistent individual**
- avoid archetypes and stock aesthetics
- accept variation in lighting and pose

Output is **identity baseline**, not final art.

---

### Step C — Calibration (Reference‑Capable Generator)
Use:
- the same identity text (unchanged)
- a visual identity reference (if available)

Activate Reference Analysis Mode.

Goals:
- reduce drift
- align text ↔ image
- preserve recognizability under stylistic variation

---

### Step D — Task Execution
Proceed with the actual task (ad, portrait, scene) under the relevant embedding.

Priority order remains unchanged:
- intent
- identity (if active)
- composition
- material
- style

---

## What This Pipeline Is NOT

- not an embedding
- not a runtime rule
- not a prompt template
- not a replacement for identity references

It is a **workflow optimization** validated by cross‑model testing.

---

## Validation Summary

Observed effects:
- reduced identity drift
- improved cross‑tool transfer
- no degradation of composition or style control

This note may be retired if compiled into future tooling.

---

End of Operational Note

