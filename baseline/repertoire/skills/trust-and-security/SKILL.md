# trust and security

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Untrusted input, secrets, permission or privileged action.

## Reasoning procedure
Map trust/authority boundaries, attack surfaces, least privilege, misuse cases and data flows; verify protections..

## What may be unseen
Do not assume all consumers are benevolent or trusted..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
