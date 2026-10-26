# numbers units and types

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Computation or serialization involves typed values.

## Reasoning procedure
Define units, coercions, equality, ordering, rounding, overflow, null/NaN, precision and representation..

## What may be unseen
Programming-language defaults are not necessarily domain semantics..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
