---
name: contract-grounding
description: Derive and validate observable engineering obligations when interface behavior, domain semantics, or consumer expectations could otherwise be decided by assumptions or implementation preference.
---

# Ground observable obligations

An external obligation is a commitment at a boundary, not a matter of implementation taste. Determine what is owed and why, then establish fulfillment through appropriate observations. Do not mistake the ability to measure a behavior for authority to require that behavior.

Use this skill for consequential behavioral decisions, disputed conformance, or discovery of implicit responsibilities. Routine internal formatting choices do not require a contract investigation unless an accepted constraint makes them consequential.

## Establish the responsibility

Identify the consumer or affected party, the boundary, the intended outcome, and conditions under which the system makes a commitment. Include existing consumers and commitments, not only the immediate caller. Trace internal responsibilities to the external commitments or accepted internal constraints they support.

Collect relevant authority: explicit requirements, interface definitions, current accepted instructions, authoritative standards where applicable, established compatible behavior, and domain relationships. Check version and scope. Name a conflict rather than silently selecting the source most convenient for the implementation. Existing behavior can be a defect; an example may illustrate a rule without defining its entire extent.

## Derive instead of assuming

For each proposed obligation:

- State the externally meaningful condition without referring to the chosen implementation.
- Identify the evidence and reasoning that make it required or defensible.
- Distinguish explicit requirements, necessary implications, justified inferences, provisional policy choices, and unresolved questions.
- Ask whether a materially different behavior could still fulfill the legitimate expectation. If so, do not present your preferred behavior as uniquely required without further authority.
- Consider who depends on the distinction and what goes wrong if it is lost. Convenience alone does not establish a responsibility.

Read [the contract inventory](references/contract-inventory.md) when discovering relevant dimensions. Activate only entries justified by the actual boundary. It is a search aid, not a set of universal requirements.

## Make fulfillment observable

Define the target, conditions, expected relationship or output, allowed variation, and observable boundary. The criterion must be justified independently of the current code's output. Use exact equality only where the contract makes that exact representation significant; otherwise check the relevant semantic relationship. Conversely, do not replace required exact behavior with a looser notion of similarity.

Choose a check that can distinguish a plausible violation: examples, properties, contrasting cases, state transitions, structural inspection, integration observations, or justified formal analysis. Match the depth of the evidence to the responsibility. State what a proxy or local check does not establish. A measurable operational limit can require workload, population, duration and tolerance definitions rather than one deterministic test.

Keep three claims separate:

1. **Observed fact:** what the system did under stated conditions.
2. **Normative claim:** what it owed, justified by authority and reasoning.
3. **Conformance judgment:** whether the observation fulfills that scoped obligation.

Passing an evaluator objectively establishes agreement with its assertions. It does not by itself resolve a disagreement between those assertions and the public contract. Self-authored checks can provide meaningful evidence when their oracle is justified; independent execution and exhaustive coverage are additional questions.

## Resolve or bound uncertainty

If available evidence determines the behavior, implement and verify it consistently. If several interpretations remain defensible, record a provisional choice, its authority, and the consequence of choosing differently. Seek clarification when the ambiguity materially blocks authorized work; otherwise make a proportionate reversible choice and disclose the limit.

Do not downgrade an explicit requirement to taste because compliance is inconvenient. Do not promote an inferred preference to a mandatory contract because a hidden test favors it. Design choices can become commitments once exposed and relied upon; revisit their compatibility implications before changing them.

For significant decisions, retain a concise chain: **expectation → authority → deduction or choice → fulfillment condition → implementation/integration → observation → scoped assessment**. Revisit it when the contract, implementation, environment or assumptions change.
