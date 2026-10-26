# recli checkpoint 2 — implementation and verification record

Released benchmark: `gabeorlanski/scb-problems@9cd9ca3a51c3d3e2a99d2488a25baf73a2204451/recli/checkpoint_2.md`; blob `039f63d133fa6d1a5d323bd49e3a2b346871624a`.
Authorized reads this checkpoint: existing implementation and generic protocol, checkpoint-2 specification only. No benchmark tests or future checkpoint material accessed.

## Requirement accounting
| ID | Contract | Boundary | Evidence/status |
|---|---|---|---|
| C2-01 | CLI > nearest project > global > defaults | configuration.load_configuration, CLI.run | Original test written; NOT_RUN |
| C2-02 | Project upward search; local file priority; first directory wins | project_config_path | Original test written; NOT_RUN |
| C2-03 | Global config path env/root fallback; auto-create locale/installer_version | global_config_path/load_configuration | Original test written; NOT_RUN |
| C2-04 | YAML inheritance and replacement/append semantics | read_yaml/merge_config | Original test written; NOT_RUN |
| C2-05 | Global recognized parameters; runtime-only and file-only applicability | GLOBAL_DEFAULTS/RUNTIME_PARAMS, CLI.run | INCOMPLETE: partial checks only, NOT_RUN |
| C2-06 | Deprecated warning and hidden globals | CLI.deprecated_globals/hidden_globals | INCOMPLETE: API hooks only; no metadata registry or original tests |
| C2-07 | Disabled commands blocked | CLI.run | Original test written; NOT_RUN |
| C2-08 | Alias validation, runtime overrides, local path resolution | read_yaml/load_configuration | Original tests written; NOT_RUN |
| C2-09 | Alias invocation, @all ordering, groups, invalid members, duplicate suppression | expand_alias, CLI.run | Original tests written; NOT_RUN |
| C2-10 | Unknown alias and edit suggestions | expand_alias | Original test written; NOT_RUN |
| C2-11 | Remote SSH execution, pre-command, error 255 | execute_remote, CLI.run | NOT_RUN: needs controlled SSH transport verification |
| C2-12 | Packages directory resolution | packages_directory | Original test written; NOT_RUN |

## Architecture and method crosswalk
- Explicit requirements to independent original test oracles: APPLIES, test sources committed; execution NOT_RUN.
- Integration and state/side effects: APPLIES; global YAML auto-write and remote subprocess need failure-injection tests.
- Source of truth: YAML merge and environment overrides centralized in configuration.py; dispatch remains in CLI.
- Open obligation: inherited checkpoint-1 strict-flag and determinism coverage remains INCONCLUSIVE. CP2 global strict handling is coded but not verified.
- Possible negative transfer: configuration loaded inside run may introduce filesystem side effects for a previously pure dispatcher; not yet evaluated.
- Skills/tools: existing requirement and crosswalk skills consulted; no claimed improvement; no new sensor validations.

## Raw execution
Checkpoint-2 unit and integration test commands: **NOT_RUN**.
The earlier checkpoint-1 suite was executed in a local workspace before checkpoint-2 code changes (6 passed); **this does not validate the current revision**.
GitHub Actions intentionally not configured. External evaluator NOT_RUN.
No baseline/current-commit correctness claim is made.

## Experimental freeze
**INCOMPLETE** — implementation and original tests published but unverified; no engineering-complete claim. The checkpoint 2 implementation should not be trusted until the committed tests and inherited regressions run, and the incomplete requirements receive evidence. Future stage must not be released until this record is published and verified.
