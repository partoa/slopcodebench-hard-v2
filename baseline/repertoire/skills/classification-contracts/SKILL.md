---
name: classification-contracts
description: Establish and validate category membership for statuses, outcomes, policies, routing, permissions, or diagnostics when choosing the wrong class changes externally observable behavior.
---

# Classify by justified decision boundaries

Category names are vocabulary, not definitions. Knowing every available label does not establish which label owns a case. Determine the classification contract before wiring cases to outputs.

## Establish the classification problem

Identify the entity being classified, the relevant conditions and context, the consumer of the classification, and the decisions or effects that depend on it. Distinguish independent dimensions: an outcome can have a cause, a severity, a retry policy and an audience without those being the same taxonomy.

For each category, identify its authoritative definition and distinguishing predicate. Do not assume that a familiar label carries the same meaning across domains. If definitions are incomplete, enumerate plausible alternatives and mark the unresolved boundary.

## Construct a decision model

Use a compact table or equivalent predicates:

| Case conditions | Candidate class | Defining rule and authority | Consequence | Uncertainty |
| --- | --- | --- | --- | --- |
| Relevant facts and context | Proposed category | Why the case belongs here | What the consumer does differently | Any unsettled distinction |

Distinguish malformed representation, out-of-range or prohibited value, inconsistent relationship, absent prerequisite, unauthorized action, and operational failure only to the extent the contract distinguishes them. Do not impose a universal mapping from these concepts to particular labels.

For neighboring classes, find cases that differ in the defining condition while holding irrelevant facts constant. Identify overlaps and gaps. Establish priority when several rules apply, including specific exceptions to general defaults. Some classifications legitimately allow several labels or an unknown result; do not force exclusivity or completeness unless required.

## Validate the mapping and its realization

Check a representative member, a nearby nonmember, and consequential boundary or ambiguous cases for important categories. Verify that irrelevant changes do not change the class, while changing a defining condition does. Such checks require a justified oracle; they do not independently settle a disputed definition.

Inspect how the decision reaches the public output or effect. Defaults in helper functions, exception wrapping, lookup fallbacks, dispatch order and later translation can replace a correctly reasoned classification. Verify the observed boundary rather than merely the presence of the correct constants.

Separate an incorrect decision rule from an incorrect implementation of the rule. If the mapping is inconsistent, repair the rule or realization indicated by the evidence. Do not blindly swap labels to match known examples. When the public contract underdetermines the taxonomy, retain the mismatch and ambiguity separately instead of inventing a uniquely correct rationale after evaluation.

A reusable lesson should retain the predicates, applicability, authority and counterexamples. Preserve exact category names only when their particular contract is relevant to future use.
