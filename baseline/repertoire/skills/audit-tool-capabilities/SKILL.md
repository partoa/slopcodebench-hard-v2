---
name: audit-tool-capabilities
description: Determine whether an engineering analysis tool can answer the actual question it is being used for, by inspecting its implementation, coverage, assumptions and discriminating capability probes.
---

# Audit the capability before trusting its output

A tool name, graph representation or successful command does not establish the capability an engineering decision requires. Audit the inference the tool actually performs, not the inference a reader wishes it performed.

## Define the required observation

Start with an actual engineering uncertainty or consumer obligation. State the question, the distinguishing observation, the target language/environment and the required scope. Separate candidate discovery from established findings and verified transformations. A heuristic may be useful without being sound or complete, but its limits must be visible.

Map the tool's claimed inputs and outputs to its actual implementation. Follow a small case from source collection through parsing, representation, query/analysis, finding and presentation. Identify unsupported constructs, skipped input, unresolved relationships and defaults. Include module initialization, nested scopes, generated code and supported language versions when relevant to the claim.

Distinguish names from bindings, object identity, member accesses and runtime values. Distinguish syntax from control flow, call resolution, data dependencies, effects and execution cost. A list of function names is not a resolved call graph; a repeated identifier is not evidence of shared state; a similar function body is not the same as duplicate computation.

## Probe the claim, not merely the parser

Construct small authorized cases with independently understandable behavior:

- A genuine positive case and a nearby legitimate counterexample.
- A surface change that preserves the relevant relationship, such as renaming bound variables.
- A relationship change that preserves surface similarity, such as unrelated locals with the same spelling.
- Supported boundary constructs and explicit unsupported or malformed input.

Observe whether the output includes enough coverage information to interpret silence. No finding, unsupported input, unresolved analysis, failed analysis and a checked negative are different results. State the actual soundness or completeness limits instead of claiming universal detection from a few probes.

For repeated work, identify operation identity, input provenance, call-site multiplicity, relevant context, mutations, side effects and dependency changes. Repetition may be required for fresh observations or contextual validation. Measure a controlled example before proposing reuse. A safe optimization requires stronger evidence than a candidate detector.

## Produce an actionable capability assessment

Classify each gap as an implementation defect, unsupported capability, fragile integration, misleading claim, or unvalidated hypothesis. Cite the exact tool version, source boundary, probe and observed result. State the decision it prevents or misleads, and define an acceptance check for an improvement. Preserve uncertainty where a suspected gap was not exercised.

Choose a proportionate response: use a narrower claim, select a different observation method, add a targeted capability, or defer the inquiry. Do not demand an expensive graph engine where a smaller analysis or runtime trace can supply the required evidence.

Keep audit fixtures and hidden evaluation material outside unauthorized implementation contexts. Findings are prospective development inputs; they do not retroactively establish that an earlier tool had the missing capability.
