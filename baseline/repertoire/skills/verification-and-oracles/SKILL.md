# verification and oracles

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** An agent writes tests or claims a responsibility is satisfied.

## Reasoning procedure
Derive oracles independently from contracts, add negative controls, contrasting examples, source/environment evidence and scoped closure..

## What may be unseen
Self-authored passing tests are not independent certification..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
