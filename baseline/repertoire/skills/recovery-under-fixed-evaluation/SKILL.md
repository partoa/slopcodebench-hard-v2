# Recover without contaminating the independent evaluator

**Trigger:** A failed self-authored test, observable regression, inconsistent domain model, contradictory assumption, missing obligation, or unexpectedly costly method creates a justified need to repair or revise behavior.

**Method:** Diagnose from the released specification, same-arm source, authorized runtime observations, own executable checks, and genuine input/output contracts. Revisit prior assumptions and the repercussions of the failure; if appropriate, reverse, perturb, instrument, compare alternatives, or try to break the proposed repair. Modify code only when the correct behavior and need for change are supported. Rerun own earlier tests plus new checks against the current revision, not just the failing example.

**Recovery states:** ATTEMPTED (with test and result), NOT_NEEDED (explain why), DEFERRED (why an attempt was unwarranted or unavailable), BLOCKED (technical constraint). A failing check should ordinarily trigger a recovery attempt while development is allowed.

**Benchmark limit:** Use the official SlopCodeBench evaluator unmodified and only after the normal submission boundary, under the same pass policy, hidden tests, timeout and resource constraints as comparators. Do not feed official hidden test names, arguments, traces, fail counts, messages or summaries back to agents for learning. The benchmark's prescribed early stopping remains in force. No post-evaluation repair of a frozen submission or extra retries granted because of a bad hidden score. If that feedback/retry scenario is studied, it must be a distinctly labeled nonstandard experiment.

**Learning:** Retain the raw authorized result (including command, exit code, stdout, stderr, test-file hashes and code SHA) and a separate review explaining why the new observation matters. Update a skill only if the lesson is plausibly reusable, with scope and counterexamples. A self-authored pass is not independent certification.
