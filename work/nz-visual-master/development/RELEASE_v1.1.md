# Visual Master — Release v1.1

## Release Status

This release finalizes the **core production architecture** of Visual Master.

Execution Core, embeddings, and runtime profiles are considered
**architecturally complete and frozen**.

Further development must not modify production behavior
without a new version and explicit freeze.

---

## Scope of This Release

Release v1.1 includes:

- Finalized Execution Core
- Synchronized constraint-only embeddings
- Frozen runtime profiles
- Formal separation of DEV and PROD
- Completed QC matrices

No experimental, provisional, or implicit behavior remains.

---

## Execution Core

- Single authority for reasoning and decision order
- Fully self-sufficient at runtime
- No dependency on DEV artifacts
- Explicit handling of:
  - uncertainty,
  - unknown tools,
  - language behavior,
  - copy-paste–ready prompt formatting,
  - security and integrity

Version: **Execution Core v1.1 (FROZEN)**

---

## Embeddings

All embeddings are **constraint-only** and synchronized with Core v1.1.

Active embeddings:

- portrait_embedding_core.md
- advertising_branding_embedding_core.md
- layout_composition_embedding_core.md
- style_embedding_core.md
- mvm_embedding_core.md

Embeddings:
- do not introduce intent,
- do not control reasoning,
- do not override Core.

---

## Runtime Profiles

Runtime profiles are frozen and limited strictly to interaction control.

Profiles:

- LITE — minimal verbosity, no explanations
- PRO — structured, explanatory interaction

Runtime profiles:
- do not affect reasoning depth,
- do not affect quality,
- do not affect constraints.

---

## Development vs Production

### Development (DEV)

DEV contains:
- context-of-use descriptions,
- reference examples,
- operational protocols,
- QC matrices,
- analytical and explanatory materials.

DEV artifacts are used exclusively to **compile behavior**.

They are never loaded or referenced at runtime.

### Production (PROD)

PROD contains only:
- Execution Core,
- Embeddings,
- Runtime profiles.

If all DEV artifacts are removed,
PROD remains fully functional.

---

## Quality Control

QC matrices validate:

- authority separation,
- constraint purity,
- identity preservation,
- branding clarity,
- material plausibility,
- language hygiene,
- security and injection resistance.

All mandatory QC checks pass for this release.

---

## Change Policy

After this release:

- Execution Core changes require a new version.
- Embedding changes must not conflict with Core.
- Runtime profile changes must not affect logic.
- DEV artifacts may evolve freely.

No hotfixes or runtime patches are permitted.

---

## Architectural Closure

Release v1.1 marks the point at which:

- system behavior is fully specified,
- architectural responsibilities are closed,
- further changes are deliberate, not accidental.

This release serves as a **stable baseline** for all future work.

---

End of Release v1.1
