# architecture and temporal debt

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Repeated changes increase structural cost.

## Reasoning procedure
Trace structure, dependencies, invariants, obligation propagation and affordances; compare justified designs and change cost..

## What may be unseen
A complexity metric or favored pattern is not itself an obligation..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
