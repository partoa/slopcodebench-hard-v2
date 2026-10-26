# Blue team: defensive design and resilience response

**Trigger:** a concrete security challenge, misuse case or operational fault threatens a justified boundary obligation, or an existing mitigation is being evaluated.

**Do not apply by default** to every internal data value. Start from what authorized consumers must accomplish under the supplied specification.

1. **Prevent:** reject invalid/untrusted actions where appropriate, enforce authority, avoid unsafe state transitions or remove the cause.
2. **Detect:** provide usable evidence of attempted misuse, impending overload, invalid state or failing dependency.
3. **Contain:** isolate effects, limit resources, avoid corrupted output or unauthorized propagation.
4. **Recover:** retry safely if allowed, restore state, report irrecoverable failure and support an authorized operator response.

Which items apply depends on stated guarantees, externalities, cost and risk. Some may be out of scope. A justified **no additional defense** is a legitimate result.

**Test a pair**: the challenging/fault condition and a benign/authorized negative control. Define pass/fail from domain contract and failure budget, not from the preferred implementation. Record impact of the defense, known residual risks, evidence, version and cost. If the challenge reveals a missing external obligation, add it as a candidate until independently justified.
