# SlopCodeBench Hard v2 — spec-only Arm C experiment

**New uncontaminated implementation run.** No checkpoint implementation, public evaluator test source, prior test results, or prior experiment solution is included here. The reusable engineering repertoire and generic tool unit tests are distinct from benchmark evaluator tests.

## Strict benchmark firewall

Implement solely from one released public `checkpoint_N.md` and that problem's `config.yaml` metadata, never `tests/`, `solutions/`, benchmark evaluation harness code, prior implementations, prior evidence, branch/history of benchmark runs, or hidden feedback. **Do not clone or browse the public benchmark repository recursively.** Retrieve exact allowed files only. Do not browse `partoa/slopcodebench-hard`; it contains contaminated application work and evaluator tests.

At every checkpoint, independently derive tests from explicit requirements. All authored tests and test expectations must originate in the released specification, not prior public tests or recollections. Record the test oracle provenance. A true held-out evaluator must be run by a *different* evaluator after implementation freeze, never exposed to implementing agents or this experiment's active chat.

One checkpoint at a time; freeze code, raw authored test evidence, requirements fulfillment, method crosswalk, sensors, techniques and knowledge changes before releasing the next checkpoint. Keep external results outside agent-visible artifacts. Fakes prove only their modeled boundaries.

## Run order

Fresh `recli` 8 checkpoints, then `meshctl` 8; `test_translator` 8; `sheeteval` 7; `sith` 6; `eve_industry` 6; `rejector` 5; `metric_transform_lang` 5; `dynamic_buffer` 4; `eve_market_tools` 4; `dag_execution` 3. Total **64 checkpoints across 11 Hard problem runs**.

Benchmark spec pin: `gabeorlanski/scb-problems@9cd9ca3a51c3d3e2a99d2488a25baf73a2204451`. This repository is a spec-only implementation workspace; no benchmark test fixtures or evaluator material should ever be copied into it.

## Skills and tooling

Use `baseline/repertoire/skills/` (generic historical skills) plus `skills/obligation-method-crosswalk/` and `skills/explicit-requirement-fulfillment/`. `baseline/tooling/tests/` and `tooling/tests/` test generic analysis tools only; they are not SlopCodeBench evaluator tests. Archive older tools as versioned code, and validate their actual scope before assuming semantic coverage.

Never claim complete correctness from passing authored tests. Document unsupported conditions and distinguish engineering-complete from experimental freeze. Historical `recli` experience means this reset is **not provably blind** if the implementing agent can recall it; a new session with no imported conversational memory, no old branches, and a hard repository access allowlist is required.
