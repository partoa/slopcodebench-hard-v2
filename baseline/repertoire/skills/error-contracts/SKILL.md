# error contracts

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Invalid input or operational faults require public diagnostics.

## Reasoning procedure
Map failure families to externally specified error categories, paths, statuses, precedence and actionable recovery..

## What may be unseen
Do not extend special-case errors because their names sound plausible..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
