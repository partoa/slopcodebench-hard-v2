# integration realization

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Code crosses multiple boundaries or deployment conditions.

## Reasoning procedure
Trace obligation -> implementation -> composition -> entrypoint -> deployment -> operational outcome; test at the owed boundary..

## What may be unseen
Code presence or unit checks are not operational fulfillment..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
