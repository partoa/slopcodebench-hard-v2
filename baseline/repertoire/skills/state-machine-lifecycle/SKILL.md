# state machine lifecycle

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Behavior depends on process state, persistence or time.

## Reasoning procedure
List states, transitions, preconditions, invariants, cleanup, restart, retries and partial failure..

## What may be unseen
Single-call tests do not close lifecycle obligations..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
