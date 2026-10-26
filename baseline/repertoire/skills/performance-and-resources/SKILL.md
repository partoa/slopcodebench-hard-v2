# performance and resources

**Seed status:** generic candidate skill; not independently validated.

**When applicable:** Latency, scale, budget or resource consumption matters.

## Reasoning procedure
Tie measurable budgets to consumer needs; test representative, peak, tail and failure workloads..

## What may be unseen
Proxy metric improvement without a user-facing consequence is not enough..

## Falsification and evidence
Specify a contrary case or independent negative control; justify the required behavior from the contract or domain rather than current code. Test at the affected boundary and retain inconclusive results.

## Domain adaptation
Create a new, arm-local, versioned skill if the encountered problem reveals domain-specific assumptions, consumers, externalities or exceptions. Record what was observed, what could not be observed, known unknowns and systematic unknown-unknown probes. Never report all unknowns covered.
