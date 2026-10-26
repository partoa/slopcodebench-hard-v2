---
name: audit-tool-operation
description: Audit whether engineering tools are reachable, reproducible and trustworthy in the agent's actual environment, including evidence integrity, state transitions, failure reporting and operational cost.
---

# Audit the operational and evidence contract

A capable analysis that the agent cannot run does not provide its intended value. A passing record validator does not establish the truth of the recorded claim. Inspect both the operational path and the evidence it produces.

Trace prerequisites from invocation through source collection, analysis, artifact generation, downstream interpretation and recovery. Distinguish a legitimate permission or provenance restriction from an unnecessary coupling that blocks read-only analysis. Preserve real access boundaries; do not bypass them by editing identity metadata or weakening guards.

Test the claimed deployment modes and environment assumptions using authorized resources. Record frontend/runtime/tool versions, configuration, source identity, dirty-state handling, supported file types and excluded or failed inputs. If a verified source snapshot can be analyzed without a genuine checkout, label the mode and provenance accurately rather than fabricating a native freeze.

Audit negative and partial outcomes. Malformed input, unsupported constructs, missing prior state, interrupted writes, timeouts and unavailable dependencies should be distinguishable from a checked negative or successful audit. Consider transactional artifact generation, resumable operations and idempotent retries when the workflow requires them. Do not rewrite immutable historical records to make a chain pass.

For evidence claims, follow the bytes and identities rather than trusting labels:

- Do source, tests, commands, runtime and configuration correspond to the state actually analyzed or executed?
- Are referenced artifact contents checked against their recorded digests at the decision boundary?
- Can a later edit invalidate a review without changing an event identifier?
- Are source coverage, relevant dependencies and context changes represented in validity checks?
- Does a claim of independent verification identify a genuinely separate authority or execution, rather than a nonempty field?

Separate record shape, integrity, oracle authority, observed behavior, coverage and independence. Reject false certainty without erasing legitimate scoped local evidence. Empty lists and an inconclusive result can be truthful; a gate should not demand fabricated uncertainty or success.

Measure the tool's time, memory, output volume, maintenance and investigation burden where they matter. Distinguish measured values from estimates. Add explicit bounds or cancellation for subprocesses and captures when required by the operating contract. Inspect whether selection and review budgets remain bounded as records accumulate.

Document assumptions that the tool cannot verify, including information access beyond the repository. A branch-name check is not a memory firewall. Do not output a stronger provenance claim than the mechanism establishes.

Propose changes against concrete failures, preserve old evidence, and validate the repaired workflow end to end. A repaired schema is not by itself proof that the analysis or the engineering decision improved.
