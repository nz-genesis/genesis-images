# Operational Note — Temporal Identity Consistency

Status: SOURCE
Role: Operational Note (Development)
Audience: Human operator / system architect

---

## Purpose

This note defines a **safe operational framework** for maintaining identity consistency
across time, context, and narrative progression.

It applies when the **same character appears in multiple moments**, scenes, or versions
without becoming a new identity.

This note introduces no new embeddings and does not modify runtime behavior.

---

## Conceptual Scope

Temporal identity consistency concerns:
- the same person across different times
- aging or de-aging within a controlled range
- emotional or situational change without identity loss
- continuity across campaigns, scenes, or series

It explicitly excludes:
- reincarnation or alternate identities
- symbolic or metaphorical identity shifts
- multiverse or role-swapping scenarios

---

## Identity Invariants (Must Persist)

Across time, the following must remain coherent:
- core facial structure
- stable traits (hairline, eye color, baseline proportions)
- psychological presence
- recognizability as the same individual

These invariants anchor the identity.

---

## Permitted Temporal Variations

The following may change without breaking identity:
- age (within a plausible range)
- hairstyle and grooming
- clothing and accessories
- pose and body posture
- lighting and environment
- emotional state (calm, focused, serious, reflective)

Temporal variation must never collapse recognizability.

---

## Operational Workflow

### Step A — Identity Anchor

Use an existing semantic identity anchor:
- text description
- optional visual reference

Do not rewrite the anchor per time state.

---

### Step B — Temporal Modifier

Apply a lightweight modifier describing time shift:
- "earlier"
- "later"
- "slightly older"
- "more mature"

Avoid numerical ages.

---

### Step C — Scene Execution

Execute under the active task embedding (ad, portrait, scene).

Portrait embedding remains active.
Temporal change does not disable identity preservation.

---

## Conflict Resolution

If temporal variation conflicts with recognizability:

Resolution priority:
1. Identity recognizability
2. Narrative plausibility
3. Temporal accuracy

Disclosure is required if temporal intent is constrained.

---

## Common Failure Modes (Avoid)

- treating time shift as a new character
- excessive aging or de-aging
- identity dilution through style or lighting
- overuse of symbolic aging cues

---

## Validation Notes

Observed stability improves when:
- the same identity anchor is reused verbatim
- temporal modifiers are qualitative, not quantitative

---

## Placement and Lifecycle

This file is:
- operational only
- optional
- removable

It may later be merged into higher-level narrative tooling.

---

End of Operational Note