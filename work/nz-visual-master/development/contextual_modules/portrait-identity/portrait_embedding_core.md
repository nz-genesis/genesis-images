# PORTRAIT / IDENTITY EMBEDDING — CORE

**Status:** SOURCE  
**Role:** Contextual Embedding (Development)  
**Domain:** Human identity and recognizability

---

## Purpose

This embedding governs **identity-critical visual tasks** involving human subjects.

Its purpose is to:
- preserve recognizability of a specific person,
- prevent identity drift,
- distinguish identity from style, pose, or context,
- define when identity logic must apply — and when it must not.

This embedding does **not** describe how to draw faces.
It constrains **how identity is treated** during execution.

---

## Activation Conditions

Activate this embedding **only if**:
- a specific person is implied or referenced,
- recognizability matters across variations,
- the subject functions as an identity anchor (brand face, character, known individual).

Do **not** activate this embedding if:
- the subject is generic or anonymous,
- the task is face replacement or substitution,
- humans are background elements only,
- Core-Only Mode is explicitly required.

---

## Identity Scope

Identity is defined as the **stable recognizability of a person**.

Identity includes:
- core facial structure and proportions,
- stable traits (hairline pattern, eye color, skin tone),
- age range as a qualitative attribute,
- psychological presence (calm, tense, reserved, expressive).

Identity explicitly excludes:
- clothing and accessories,
- pose and body posture,
- hairstyle variations,
- lighting conditions,
- camera angle or lens choice,
- emotional state as narrative abstraction.

These elements may vary freely without breaking identity.

---

## Semantic Identity Anchor

When identity matters, establish a **semantic identity anchor**:
- compact textual description of stable traits,
- optional visual reference (image),
- no numerical or geometric precision.

Rules:
- describe traits qualitatively,
- avoid aesthetic judgments,
- avoid idealization or stylization,
- prefer human realism over perfection.

The anchor defines *who the person is*, not *how they are rendered*.

---

## Identity Preservation Mode (Default)

When active, this embedding enforces:
- consistency of facial identity across images,
- resistance to stylistic distortion,
- prioritization of recognizability over aesthetics.

If conflicts arise:
1. Identity preservation prevails
2. Style and mood adjust
3. Composition adapts if necessary

Loss of recognizability is a failure condition.

---

## Temporal Variation

The same identity may appear across different times or contexts.

Permitted variations:
- slightly younger or older appearance (qualitative only),
- grooming changes,
- contextual fatigue or vitality,
- situational expression.

Forbidden:
- extreme aging or de-aging,
- symbolic or metaphorical identity shifts,
- transformation into a different person.

Temporal change must never break recognizability.

---

## Identity Substitution (Exclusion Rule)

This embedding MUST NOT be active during **face replacement or identity substitution** tasks.

In such cases:
- original identity preservation is suspended,
- replacement identity is treated as local override,
- Core-Only Mode governs execution.

Activating this embedding during face replacement is a violation.

---

## Reference Analysis Interaction

If a visual reference is provided:
- analyze for stable identity traits only,
- ignore stylistic, lighting, or contextual artifacts,
- reconcile with semantic identity anchor.

The goal is alignment, not replication.

---

## Failure Modes (Prevented)

This embedding exists to prevent:
- identity drift across generations,
- merging multiple faces into an archetype,
- loss of character through style dominance,
- unintended idealization.

---

## Quality Check

Before output, verify:
- recognizability relative to anchor,
- coherence under variation,
- absence of identity-style conflation.

If verification fails, revision is mandatory.

---

## Authority

When active, this embedding overrides:
- stylistic exaggeration,
- aesthetic optimization,
- expressive distortion.

It does not override:
- execution core logic,
- material realism requirements,
- compositional hierarchy.

---

**End of Portrait / Identity Embedding (SOURCE)**