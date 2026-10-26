# migration and compatibility

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** An existing consumer or representation survives change.

## Reasoning procedure
Preserve old commitments, version negotiation, migration, rollback, mixed-version interactions and data continuity..

## What may be unseen
Refactoring does not authorize changes to observable contracts..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
