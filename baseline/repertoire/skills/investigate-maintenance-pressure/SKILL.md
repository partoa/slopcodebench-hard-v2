---
name: investigate-maintenance-pressure
description: Investigate growing complexity, scattered changes, repeated work or architectural erosion using function histories and concrete maintenance tasks; distinguish necessary complexity from demonstrated change difficulty before proposing a refactor.
---

# Investigate maintenance pressure

Treat a structural reading as an observation requiring interpretation. A high branch count can express a coherent domain; a low count can conceal indirection, duplicated policy or a difficult dependency. Do not turn a threshold into an architectural contract.

## Choose evidence for the question

- **Concentrated decisions:** inspect function size, branch sources, nesting and their history. Identify whether decisions belong to one policy or independently changing responsibilities.
- **Scattered policy:** trace one externally justified change across its owners, callers, representations and duplicated rules. Count semantic sites needing coordinated edits, not just files or lines.
- **Repeated work:** retain call sites and input/context provenance, then observe execution counts on a relevant workload. Lexically equal expressions do not establish equal inputs, purity, repeated execution or safe reuse.
- **Hidden coupling:** inspect the information and invariants a caller must know, mutable state ownership and the dependencies through which a change can propagate. A lexical call graph does not establish data flow or aliasing.
- **Change difficulty:** record an actual task's behavior checks, affected responsibilities, attempts, rework, regressions and resources. Separate coding time from tool waits; control task size, model and budget when comparing treatments.
- **Lost visibility:** inspect parse failures, excluded files, unresolved calls and identity-matching uncertainty before interpreting an apparent improvement.

For a local Python structural baseline and before/after comparison, use `tooling/maintenance_sensor.py` and `tooling/change_impact.py` in the versioned toolkit. Read its output limitations. It does not measure maintenance effort, prove a defect, implement scb-check's exact formula, or resolve data flow.

## Establish an engineering consequence

Start with a requirement available to the agent, not a hidden evaluator outcome. Trace the smallest coherent change and ask which decisions and invariants must be understood together. Locate avoidable coordination, redundant preparation, conflicting ownership or accidental representation constraints. Describe necessary domain work separately.

Record observation → candidate explanation → distinguishing check → engineering consequence → decision. Keep evidence states separate: structural signal; investigated hypothesis; demonstrated burden; proposed remedy; verified effect. A threshold crossing may remain a signal indefinitely if no harmful consequence is established.

Compare preserving the design with a proportionate alternative. Test contrary cases: a large cohesive dispatcher, a small but scattered policy, a wrapper-heavy refactor, an operation that must be recomputed after state changes. Check whether the proposed boundary reduces the context needed for the concrete task without increasing coupling or invalidating an obligation.

## Verify the intervention and retain its limits

Preserve behavioral obligations, then repeat the distinguishing check. For a changeability claim, show what coordination or rework was reduced on a named task; for runtime claims, measure representative execution. Report adverse effects, introduced dependencies and residual uncertainty. Absolute complexity, function distribution and added indirection should accompany ratios so dilution cannot masquerade as improvement.

Choose preservation, observation, instrumentation, local repair or decomposition according to the evidence. Store the method with activation cues, useful counterexamples and cost. Establish transfer on a later independent task before claiming general improvement.

In a controlled experiment, register new skills, tools and feedback prospectively. Retrospective sensing of frozen code does not establish that agents detected or acted on its signals during implementation.

## Change impact tracking

At each meaningful source revision, compare *matching explicitly scoped* structural snapshots, then ask whether a named requirement forced coordinated semantic edits, rework or additional context. Track tool/analysis cost as part of the result. Enter only observed measurements; when no task evidence exists, record `NOT_MEASURED`, never a positive maintainability verdict. Use `tooling/templates/change-trial.example.json` as a data shape, not as evidence of a completed trial. Reconsider and remove low-value records; Git history is the retirement log.
