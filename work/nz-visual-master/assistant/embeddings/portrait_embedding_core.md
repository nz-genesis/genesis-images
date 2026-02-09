# PORTRAIT / IDENTITY EMBEDDING — CORE (FROZEN)

**Status:** FROZEN  
**Role:** Contextual Embedding (Runtime)  
**Domain:** Human identity and recognizability


## Embedding Role

This embedding enforces **identity preservation constraints** for portrait-oriented visual tasks.

When active, it restricts the system from altering, stylizing, or reconstructing a person’s identity
beyond acceptable natural variation.

This embedding does not define intent, reasoning order, or generation strategy.
It only constrains the allowable output space.

---

## Identity Integrity Rules

When this embedding is active, the system must:

- preserve facial structure, proportions, and recognizable identity features;
- prevent identity replacement, face swapping, or composite identities;
- avoid exaggerated stylization that alters recognizability;
- maintain continuity of identity across temporal or stylistic variation.

Identity preservation has priority over:
- stylistic interpretation,
- aesthetic enhancement,
- artistic abstraction.

---

## Acceptable Variation

The following variations are allowed **only if recognizability is preserved**:

- natural aging or de-aging within plausible bounds;
- changes in expression, pose, lighting, or environment;
- non-destructive stylistic rendering that does not distort identity;
- period-accurate appearance adjustments.

---

## Explicit Exclusions

When this embedding is active, the system must not:

- replace one identity with another;
- merge or blend multiple identities;
- generate fictional or anonymized faces in place of a real subject;
- apply caricature, extreme stylization, or abstraction that compromises identity.

---

## Conflict Resolution

If a conflict arises between identity preservation and other constraints:

1. Identity preservation takes precedence.
2. Style and aesthetic goals must yield.
3. If preservation cannot be guaranteed, the system must request clarification or decline.

---

**End of Portrait / Identity Embedding (FROZEN)**

