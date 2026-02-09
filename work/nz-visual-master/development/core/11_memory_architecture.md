# MEMORY ARCHITECTURE — VISUAL MASTER (AI-NATIVE)

This document defines how Visual Master memory is structured, loaded, and preserved.
Memory architecture ensures continuity, stability, and scalability across sessions.

---

## CORE PRINCIPLE

Not all knowledge is equal.
Memory is layered by mutability, scope, and purpose.

---

## MEMORY LAYERS

### 1. SYSTEM PROMPT (EXECUTION CORE)

File:
- 01_system_prompt_execution_core.md

Properties:
- always loaded
- immutable
- defines execution behavior

---

### 2. IMMUTABLE CORE MEMORY

Files:
- 02_core_philosophy.md
- 03_pipeline_8_steps.md
- 04_core_modules.md
- 05_storytelling_visual_dramaturgy.md
- 06_conflict_tension_grammar.md
- 07_non_mechanical_creativity.md
- 08_professional_qc.md
- 09_reference_tool_intelligence.md

Properties:
- always loaded
- immutable
- define reasoning, rules, and evaluation

---

### 3. ADAPTIVE MEMORY

Files:
- 10_adaptive_intelligence.md

Stored content:
- user preferences
- successful pattern tendencies
- session-level adjustments

Properties:
- persists across sessions (if supported)
- bounded by immutable core

---

### 4. CONTEXTUAL MODULE MEMORY

Examples:
- portrait_module.md
- advertising_module.md
- video_module.md
- 3d_module.md

Properties:
- loaded only when relevant
- extend, never override, core rules

---

### 5. TEMPORARY SESSION MEMORY

Content:
- current task state
- intermediate decisions
- unresolved branches

Properties:
- cleared after session
- never persisted

---

## MEMORY LOADING ORDER

1. System Prompt
2. Immutable Core Memory
3. Adaptive Memory
4. Contextual Modules (if any)
5. Session Memory

Lower layers may not override higher layers.

---

## CONTINUITY RULE

To continue work in a new session:
- reload System Prompt
- reload Immutable Core Memory
- reload Adaptive Memory (if available)

Do not rely on session memory persistence.

---

## MEMORY SAFEGUARDS

Forbidden:
- modifying immutable files
- loading conflicting modules
- adapting rules instead of preferences

Violation requires rollback to last stable state.

---

This document is immutable.
All memory handling must comply with this architecture.
