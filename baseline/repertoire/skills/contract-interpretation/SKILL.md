# contract interpretation

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Requirements admit multiple externally visible meanings.

## Reasoning procedure
Enumerate candidate interpretations, authority, validation timing, precedence and consequences; generate discriminating examples and independent test oracles..

## What may be unseen
Do not resolve ambiguous contracts by copying implementation behavior..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
