---
name: architectural-decomposition
description: Reconsider responsibility boundaries when evolving code accumulates interacting policies, repeated preparation, compatibility branches, or costly changes; justify decomposition through behavior, ownership and concrete change scenarios rather than metric targets.
---

# Decompose by responsibility, evidence and reason for change

Use this skill when new requirements concentrate decisions, spread one responsibility across several places, or create repeated work and growing context. A high-complexity function is an investigation cue, not an obligation to refactor. A small dispatcher or a cohesive parser may legitimately contain many branches.

## Find the actual structural pressure

Choose a current change or a plausible next change supported by the task's direction. Trace the responsibilities, dependencies and invariants that must be understood or modified. Identify what changes together and what should vary independently. Distinguish essential domain complexity from complexity caused by representation, wiring, repeated work or accumulated compatibility decisions.

Describe each candidate responsibility by its inputs, outputs, authority, owned state, invariants and failure behavior. A boundary is useful when a caller can rely on that contract without understanding the callee's implementation. Extracting a contiguous block or reducing a function's branch count does not by itself create such a boundary.

## Separate work by what it depends on

Distinguish structural validation, semantic relationship checks, normalization, binding/resolution, execution and external presentation where their authorities or dependencies differ. Do not require separate classes or passes for every distinction; use the simplest structure that makes the relevant dependencies clear.

For each repeated operation, identify its actual inputs, configuration, environmental observations and mutations. Distinguish stable preparation from context-dependent checks and effects. A syntax tree may depend on source and grammar, while a resolved program also depends on definitions and scope, and its result depends on runtime state. Reuse only within the conditions that keep the relevant dependencies valid.

Consider retaining a prepared representation when the system repeatedly reconstructs information required for execution. Keep provenance, binding context and diagnostic meaning intact. Do not add caching or an intermediate representation merely because it is a familiar pattern. Establish a useful responsibility boundary and a measured or otherwise demonstrated reason first.

## Compare boundaries and ownership

Check whether one function owns unrelated policies or whether one policy is implemented inconsistently across several functions. Seek boundaries that localize reasons for change, preserve coherent invariants and reduce the context a maintainer must hold at once.

Keep execution ownership explicit: who may mutate data, who constructs new values, and where copying is required. Keep internal computation results distinct from public response envelopes when recursive components should not depend on presentation details. Use named representations when positional tuples or output parameters obscure important roles; do not replace a clear simple tuple with a framework by default.

Treat compatibility as an owned responsibility. If parallel old/new paths remain necessary, specify which inputs and semantics each supports, where they meet, and how they are tested. Investigate whether a common representation or narrower adapter can preserve the promise with less policy duplication. Do not delete the old path merely to reduce lines.

## Challenge the proposed change

Compare retaining the design, a local extraction, a shared representation or helper, and a broader reorganization as appropriate. Evaluate the concrete change scenario: responsibilities touched, dependencies introduced, invariants simplified or dispersed, behavior preserved, runtime work and maintenance burden. Prefer a smaller justified change over a speculative architecture.

Before changing code, establish the relevant behavioral and integration checks. Afterwards verify both the old obligations and the structural purpose of the change. For performance claims, measure meaningful workloads; for maintainability claims, record a concrete improvement in navigation, change localization, rework or defect prevention and identify subjective judgments honestly.

Metrics can corroborate the assessment but cannot substitute for it. Do not lower a ratio by adding trivial helpers, fragmenting coherent logic or moving complexity behind indirection. A better boundary should remain useful when the metric is hidden.

Retain the successful method with its activation cues, limits, costs and counterexamples. Test later unaided use on a new authorized change before claiming a transferable architectural improvement. Preserving a functioning design is a legitimate outcome when the evidence does not justify a refactor.
