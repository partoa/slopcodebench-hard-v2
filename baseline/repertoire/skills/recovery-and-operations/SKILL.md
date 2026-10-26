# recovery and operations

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Service must run reliably outside development.

## Reasoning procedure
Map packaging, configuration, logging, environment, restart, backup, health and operator recovery..

## What may be unseen
Green local tests do not demonstrate field operability..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
