# temporal order and causality

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Several operations compose or order matters.

## Reasoning procedure
Track preconditions, effects, intermediate state, idempotence, interference, order and alternative causal explanations..

## What may be unseen
Isolated operation correctness does not prove composed correctness..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
