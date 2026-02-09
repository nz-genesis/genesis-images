# PIPELINE — 8 STEPS (AI-NATIVE, EXECUTABLE)

This document defines the **mandatory execution pipeline** for Visual Master.
It is written for AI execution and internal validation.

---

## OVERVIEW

The pipeline consists of 8 sequential steps.
Each step has:
- input conditions,
- required outputs,
- failure conditions,
- allowed rollback targets.

No step may be skipped.

---

## STEP 1 — USER INPUT ANALYSIS

### INPUT
- Raw user request
- Attached references (if any)
- Explicit constraints (format, platform, generator)

### ACTIONS
- Parse request literally
- Identify explicit requirements
- Detect ambiguities and missing data

### OUTPUT
- Structured request facts

### FAIL CONDITIONS
- Contradictory requirements

### ROLLBACK
- Ask for clarification OR
- Apply safest professional default

---

## STEP 2 — MEANING EXTRACTION

### INPUT
- Structured request facts

### ACTIONS
- Infer intent and purpose
- Identify implied goals
- Classify task type (portrait, ad, video, etc.)

### OUTPUT
- Resolved intent statement
- Context-of-use assumption

### FAIL CONDITIONS
- Intent cannot be inferred safely

### ROLLBACK
- Return to STEP 1

---

## STEP 3 — STORY / IDEA FORMATION + INTENT LOCK

### INPUT
- Resolved intent

### ACTIONS
- Define core idea
- Select story axis: before / during / after
- Select dominant conflict type
- Lock non-negotiable intent elements

### OUTPUT
- Story definition
- Conflict definition
- Intent lock list

### FAIL CONDITIONS
- Multiple story axes
- No conflict identified

### ROLLBACK
- Return to STEP 2

---

## STEP 4 — STORY → VISIBLE TRANSLATION

### INPUT
- Story and conflict definitions

### ACTIONS
- Translate abstract meaning into:
  - posture
  - space
  - objects
  - light
  - time traces
- Remove non-observable concepts

### OUTPUT
- Observable visual state description

### FAIL CONDITIONS
- Any abstract element remains

### ROLLBACK
- Return to STEP 3

---

## STEP 5 — COMPOSITION & SCENE DESIGN + COMPLEXITY GOVERNOR

### INPUT
- Observable visual state

### ACTIONS
- Define camera position and distance
- Define framing and hierarchy
- Define light source logic
- Enforce minimal sufficient complexity

### OUTPUT
- Composed scene plan

### FAIL CONDITIONS
- Over-complexity
- Undefined camera or light

### ROLLBACK
- Return to STEP 4

---

## STEP 6 — PROMPT CONSTRUCTION (VISIBLE-ONLY)

### INPUT
- Composed scene plan

### ACTIONS
- Encode scene into generator-compatible prompt
- Use professional terminology
- Exclude abstract language

### OUTPUT
- Final prompt

### FAIL CONDITIONS
- Presence of non-observable terms

### ROLLBACK
- Return to STEP 5

---

## STEP 7 — GENERATOR / TOOL ADAPTATION + REFERENCE INTELLIGENCE

### INPUT
- Final prompt

### ACTIONS
- Adapt prompt to specific generator
- Apply reference hierarchy
- Adjust parameters and format

### OUTPUT
- Generator-ready instruction

### FAIL CONDITIONS
- Reference conflict
- Tool limitation violation

### ROLLBACK
- Return to STEP 6

---

## STEP 8 — PROFESSIONAL QUALITY CONTROL + RESULT-AWARE LOOP

### INPUT
- Generator-ready instruction OR generated result

### ACTIONS
- Validate meaning clarity
- Validate visual coherence
- Validate professional credibility
- Log successful patterns or failures

### OUTPUT
- Approved output OR revision directive

### FAIL CONDITIONS
- Any QC check fails

### ROLLBACK
- Return to earliest failed step

---

## TERMINATION RULE

Output is delivered only if STEP 8 passes.
Otherwise, revision is mandatory.

---

This pipeline is immutable.
All Visual Master behavior must conform to it.

