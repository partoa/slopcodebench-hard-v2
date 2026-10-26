# Try to break: risk-calibrated challenge and defense

**Purpose:** Attempt to falsify a consequential claim, design, input contract, selected skill or operating assumption when there is a **grounded reason** to suspect a failure. This is not a mandate to red-team everything.

## Applicability gate — before attacking

1. Derive the **ordinary behavior** expected from the current specification, relevant consumers and domain conventions. Begin with normal successful and expected-invalid cases.
2. Name the actual target and boundary: trusted internal state, uncontrolled dependency, external request, adversarial input, operational deployment, or skill/assumption.
3. Identify a plausible failure, exposure, impact or evidence gap; classify it as contract validation, reliability/fault tolerance, security/abuse, or exploratory uncertainty.
4. **Skip adversarial red-teaming** if the only rationale is that the skill exists. Internal fixed values may need no extra testing; OOM/crash/restart can be more appropriate internal challenges. External inputs warrant natural contract validation, with adversarial escalation only when trust and impact justify it.
5. Set an attack budget and an independently justified oracle. Don't silently transform speculative behavior into a requirement.

## Challenge styles (choose, combine or invent)

- Ordinary counterexample: valid shape but broken input relationship, boundary value, wrong lifecycle transition or inconsistent output.
- Fault injection: process crash, allocation/timeout exhaustion, partial failure, unavailable service, restart, adverse scheduling.
- Red team: malicious or deliberately misleading input across an exposed trust boundary, authority confusion, unintended side effects.
- Epistemic challenge: reverse a premise, vary a consumer, question an apparently obvious contract interpretation, change representation or run a negative control.

## Blue-team pairing

For each **credible security or resilience threat found**, determine proportionate response: **prevent, detect, contain, recover**, or explicitly limit responsibility and accept/defer residual risk with justification. Test both the failure and the authorized behavior to avoid defenses that break the promised interface. Treat blue team as a complementary **engineering response**, not a compulsory feature build.

## Evidence and learning

Record selection rationale, contract/domain authority, target/boundary, expected outcome, negative controls, observations, diagnostics, defensive outcome, source revision, resource budget and residual uncertainties. A red-team failure to break something does not prove it is safe. A failed method can still teach an applicable technique, but only scoped evidence supports promoting it.

Use `repertoire/CHALLENGE_TEMPLATE.json` for a record. An agent can choose a different operation or invent a new one if that better addresses the actual problem.
