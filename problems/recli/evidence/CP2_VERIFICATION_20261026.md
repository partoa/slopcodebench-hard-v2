# Checkpoint 2 additional verification — 2026-10-26

Only the released checkpoint-1 and checkpoint-2 specifications were used for these repairs; checkpoint-3 material was not consulted.

## Implemented in main

1. Rejected malformed file-based alias names instead of silently discarding them (`configuration.py`).
2. Added explicit registration of deprecated and hidden global parameters, with functional runtime use and warning behavior (`cli.py`).
3. Added three independent contract-derived regression checks (`tests/test_cp2_completion.py`).
4. Retained prior fixes for group broadcasting, cycle detection, initial config creation and negated runtime flags.

## Actual executed checks

Working directory `/mnt/data/cp2finish/problems/recli`. Python 3.13, pytest 9.0.2, Linux. Commands:

- `python -m pytest -q tests`: exit **0**, stdout `26 passed in 2.77s`, stderr empty, timeout not reached.
- `python -m compileall -q .`: exit **0**, empty output.
- `APPCTL_ROOT_DIR=$(mktemp -d) python appctl --version`: exit **0**, stdout `0.1.0`.
- `APPCTL_ROOT_DIR=$(mktemp -d) python appctl`: exit **0**, printed alphabetical top-level help.

Previous added tests initially failed 2 of 3 checks: invalid alias silently ignored and no public registration method for deprecated/hidden parameters. Both were fixed, and the regression suite rerun successfully.

## Evidence identity and limitations

Local `cli.py` Git blob = `a1c63853b32e688171513ab86edcbe90c22a6f5b`, **identical** to published GitHub blob. The local `configuration.py` is behaviorally equivalent but **not byte-identical** to the GitHub version. Therefore `26 passed` does **not** certify an execution of the exact published tree. Authored tests also have whitespace and reconstruction differences from GitHub.

The SSH test uses a subprocess mock validating invocation and exit-code 255 handling; actual connection to a remote host was NOT_RUN. Official benchmark evaluation was NOT_RUN and remains held out. The hidden-parameter API is locally tested for runtime use and omission from help; the specification does not prescribe concrete hidden parameter names.

## Requirement-gate disposition

Implementation repaired and published. Local authored evidence now covers the formerly open hidden/deprecated behavior and invalid-alias rejection. **Engineering-complete is NOT certified** because execution of exact committed source has not been established. The exact-tree verification gate remains open. Do not release checkpoint 3 on the strength of this record.

No experiment-specific hidden tests or evaluator scores were accessed.
