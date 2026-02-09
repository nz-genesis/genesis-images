# PROD MINIMAL PACK — Visual Master

Status: CANONICAL  
Scope: Production Runtime Contents  
Disclosure: NONE

---

## Definition

The PROD Minimal Pack defines the **complete and exclusive set of artifacts**
that constitute the production runtime of Visual Master.

No other files, documents, references, or logic are considered part of PROD.

---

## Included in PROD

The production runtime consists of **only the following**:

assistant/
├─ core/
│ └─ 01_system_prompt_execution_core.md
│
├─ embeddings/
│ ├─ portrait_embedding_core.md
│ ├─ advertising_branding_embedding_core.md
│ ├─ layout_composition_embedding_core.md
│ ├─ style_embedding_core.md
│ └─ mvm_embedding_core.md
│
├─ runtime_profile.md

yaml
Копировать код

These files define all executable behavior, constraints, and interaction characteristics.

---

## Explicit Exclusions

The following are **not part of PROD** under any circumstances:

- development files or folders
- context descriptions
- reference examples
- QC matrices
- operational protocols
- philosophy or design rationale
- comments, notes, or explanations
- test, draft, or experimental artifacts

---

## Runtime Independence

If all non-PROD artifacts are removed,
the PROD runtime must remain:

- fully functional,
- behaviorally complete,
- professionally reliable,
- secure and non-disclosive.

Any dependency on excluded artifacts
is considered an architectural violation.

---

## Change Policy

Changes to PROD artifacts require:

- explicit version increment,
- formal review,
- re-freeze of the affected files.

No hotfixes, patches, or implicit changes are permitted.

---

End of PROD Minimal Pack