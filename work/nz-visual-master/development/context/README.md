# Context Folder — README

Status: DEV / SOURCE  
Audience: System architect, developer  
Scope: Context-of-use classification and interpretation  
Not for runtime use

---

## Purpose

The `context/` folder contains **context-of-use definitions** for Visual Master.

Context files describe **what kind of visual work is being performed**
and what professional expectations apply to it.

They help the system:
- interpret intent correctly,
- select appropriate quality criteria,
- avoid category errors (e.g. treating branding as illustration).

Context files do **not** define behavior.
They define **interpretation and evaluation frames**.

---

## What Belongs Here

Files in this folder may define:

- types of visual production,
- production domains and professional contexts,
- narrative vs non-narrative classification,
- platform or medium expectations,
- output intent categories.

Examples:
- `context_of_use_visual_types.md`
- future: `context_of_use_platforms.md`

---

## What Does NOT Belong Here

Forbidden in `context/`:

- executable logic,
- constraints that change system behavior,
- embeddings or embedding candidates,
- prompt rules,
- generation instructions,
- QC algorithms,
- runtime-loadable files.

If a file affects **how the system behaves**,
it does NOT belong here.

---

## Context vs Contextual Modules (Critical Distinction)

### Context-of-Use (`context/`)

- describes *what this task is*
- affects interpretation and QC
- never constrains execution logic
- never activates or overrides behavior

Context answers:
> “What professional domain am I operating in?”

---

### Contextual Modules (`contextual_modules/`)

- extend or constrain behavior
- may enforce or block decisions
- may become embeddings
- interact directly with execution logic

Modules answer:
> “How must the system behave in this domain?”

Confusing these two is an architectural violation.

---

## Relationship to Runtime

- Context files are DEV-only
- They must never be loaded into runtime
- Their logic is assumed to be **compiled indirectly**
  into the Execution Core and QC reasoning

Runtime does not know about `context/` explicitly.

---

## Change Discipline

When adding or modifying context files:

1. Ensure the file is purely classificatory
2. Verify it does not introduce behavior
3. Confirm it cannot be interpreted as an embedding
4. Keep language descriptive, not prescriptive

If rules or enforcement appear → move the file elsewhere.

---

## Final Rule

If a file explains **what kind of work this is** — it belongs here.  
If a file explains **how the system must act** — it does not.

---

End of Context README
