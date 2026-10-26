# data and relational constraints

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Inputs, schema, queries or transformations interact.

## Reasoning procedure
Model field relations, source provenance, keys, order, null/missing, schema evolution, transformations and dependent values..

## What may be unseen
A well-typed field can still violate relationships; examples are not universal schema proof..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
