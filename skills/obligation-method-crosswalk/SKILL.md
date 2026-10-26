---
name: obligation-method-crosswalk
description: Check reasoning-method applicability for every accepted engineering obligation and revisit affected mappings on requirements, changes, failures and freezes; connect justified obligations to actual method use, operational behavior and evidence without treating skill names as fulfillment.
---

# Crosswalk obligations to methods and fulfillment

Use this skill when establishing or revising an obligation inventory or reviewing a consequential engineering event. Its subject is whether the agent has identified and applied the reasoning an obligation needs. It does not require every available skill to run for every obligation.

## Establish the available repertoire

Record the skill/tool versions actually available to this agent. Distinguish unavailable, available, retrieved, applied and evaluated. A skill in another branch, coordinator archive or global package is not automatically part of this agent's treatment. Do not load sibling skills wholesale; retrieve the selected method when needed. Standalone use can apply the core questions below even if named companion skills are unavailable; report that capability limit.

## Crosswalk every accepted obligation

Establish the released specification's explicit requirements first, with individual acceptance criteria, implementation paths and evidence. Verify the clean setup, actual entrypoint and ordinary documented execution paths, then check the explicit requirements at the boundaries where they apply. Inferred responsibilities and structural improvements supplement this baseline; they do not replace missing requested behavior. An explicit requirement that is unimplemented, violated or unsupported must remain visibly incomplete. Experimental freeze and engineering acceptance are separate dispositions.

For each obligation, assess every axis in the core crosswalk. Assign `APPLIES`, `DOES_NOT_APPLY` or `UNRESOLVED` with a reason tied to this obligation. Applicability is separate from availability, actual application and verification. Most accepted obligations will need several methods; one skill is not an exclusive category.

Route additional methods using problem classes, dependencies and the conditional cues in the reference. Account for relevant interacting classes, not just the most obvious symptom. Introduce a new class or method when necessary and explain its basis. Do not infer inapplicability from absence of a tool, test or implementation. A missing capability can leave an applicable method unexecuted.

Trace:

**Obligation and authority → reasoning need → selected method → justified decision → operational realization → observable fulfillment → evidence and disposition.**

Identify the required outcome, intended parties/resources/context and commitments to preserve. Trace whether resolved information and decisions govern the eventual effects. For stateful operations, consider relevant intermediate and terminal states and derive the required failure behavior from the contract. Avoid imposing atomicity, rollback, caching, abstraction or a particular architecture without authority.

For each selected method, retain the question it answered, actual work or artifact, what that evidence establishes and what remains unsupported. Listing a skill as used does not satisfy an obligation. A method may be applied competently yet reveal that the implementation violates the contract.

## Revisit affected mappings on each event

Trigger review for each new requirement, consequential change, changed assumption, failed or contradictory observation, and freeze. Find affected obligations through their dependencies and responsible boundaries; include relevant unbound assumptions/questions. Review each item individually, including inherited commitments. A shared event may support several reviews, but each needs its own applicability decision and disposition.

Reuse unchanged, version-valid records by reference. State why they remain valid; do not silently copy a previous pass into a new scope. Mark genuinely unaffected items with a defensible scope decision rather than rewriting every ledger. Keep unresolved applicability visible with its next distinguishing question.

## Require evidence at the right boundary

Develop observable checks from justified contracts independently of the implementation. Test complete relevant paths, required effects and forbidden effects, using contrasting conditions and failure injection where warranted. Local checks, controlled adapters, real dependencies and independent evaluators establish different scopes. State their limits. Agent-authored tests can provide valid local evidence when their oracles are independently justified.

At review or freeze, separate method application, implementation presence, local verification, independent acceptance and fulfillment claims. Check contradicted assumptions and invalidated evidence before closing an obligation. Preserve uncertainty and justified decisions to make no code change.

Use the record template with the existing obligation ledger or equivalent links. It is a recording aid, not a second mandatory ledger or a validator of reasoning truth. Evaluate this procedure by better decisions, fewer missed obligations and useful evidence at acceptable cost. When it fails, distinguish discovery, selection, application, tooling, evidence and contract-authority gaps before inventing another skill.
