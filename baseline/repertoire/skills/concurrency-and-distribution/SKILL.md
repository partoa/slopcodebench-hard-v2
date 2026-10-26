# concurrency and distribution

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Concurrent actors or networked components interact.

## Reasoning procedure
Model races, atomicity, consistency, ordering, duplication, partition and retry invariants; test adverse schedules..

## What may be unseen
Exactly-once and total-order claims require evidence of protocols..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
