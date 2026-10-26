# recli checkpoint 2 — recovery verification and freeze

Implementation branch: `recli-cp2-recovery`, based on checkpoint-2 publication `db82491980b3a240fdeff71b84d5de472c5f4097`. This deliberately excludes unfinished checkpoint-3 changes already present on `main`.

## Released authority and isolation
Only `recli/config.yaml`, `recli/checkpoint_1.md`, and `recli/checkpoint_2.md` at pinned revision `9cd9ca3a51c3d3e2a99d2488a25baf73a2204451`. No benchmark tests, reference solutions or future checkpoint reads used in the recovery.

## Recovery
- Resolved a real `@all`/group defect found by a new original boundary test: group arrays were converted to dictionaries instead of expanded.
- Added recursive group expansion, invalid-member errors, cycle detection and first-appearance handling within groups. `@all` processes registered aliases in case-insensitive sorted order, including explicitly defined groups.
- Moved first-run global configuration initialization before no-argument help.
- Corrected global `--no-color` and related negated runtime switch recognition.

## Contract tracing
| Requirement family | Verification |
|---|---|
| Upward discovery, local/project precedence, global config resolution | VERIFIED_LOCAL by original tests |
| Global config default creation and packages path | VERIFIED_LOCAL |
| YAML inheritance, merge/append, cycle failure | VERIFIED_LOCAL |
| Recognized globals, runtime-only/file-only, strict mode, explicit override | VERIFIED_LOCAL for sample variants; full combinations not exhaustively tested |
| Deprecated global remains functional with warning | VERIFIED_LOCAL through configured deprecated flag |
| Hidden global omitted from help | INCONCLUSIVE: help does not enumerate globals; no explicit metadata/visibility test |
| Disabled commands prevent handler invocation | VERIFIED_LOCAL |
| Alias file and runtime resolution, local path, unknown/misspelled name | VERIFIED_LOCAL |
| Groups, duplicate suppression, invalid references, cycles, @all ordering | VERIFIED_LOCAL |
| Remote shell pre-command, transport-exit 255/error propagation | VERIFIED_LOCAL using controlled mocked subprocess; real SSH endpoint NOT_RUN |
| Unwritable config reports error | VERIFIED_LOCAL for directory-as-config failure |

## Runs and sensor evidence
See `raw_cp2_recovery.json`. The original six checkpoint-1 regression tests and six checkpoint-2 tests pass alongside eleven new boundary checks: **23 passed**, exit 0. Syntax compilation passes. An earlier authored boundary test failed, prompting a code correction; failure is preserved, not erased.

### Important evidence limitations
The local checkpoint-2 recovery source was reconstructed from the published checkpoint-2 commit. The CLI source blob is byte-identical to the recovered GitHub CLI; the local configuration module and test source were semantically reconstructed but not byte-identical to the published files. Consequently **the exact committed branch tree has not been executed**. Local verification cannot be rebranded as verification of the GitHub branch. The remote SSH check used a controlled fake, not a real endpoint. The held-out benchmark evaluator has not been accessed.

## Architecture/method crosswalk
Requirement contracts → entrypoint, configuration loader, alias expansion and transport boundary → original positive/negative checks. Tests found incorrect group dispatch and drove local repair. Reusable technique: paired integration-path and negative-path tests are useful here; effectiveness beyond this case is not demonstrated. No tool/skill files were changed. No retrospective maintainability improvement claimed.

## Freeze disposition
**INCOMPLETE engineering verification; recovery checkpoint recorded and committed.** Remaining gates: exact-published-tree regression execution, explicit hidden-parameter evidence, external SSH integration if feasible. No authorization to advance checkpoint 3 from this result without completing these verification gates.
