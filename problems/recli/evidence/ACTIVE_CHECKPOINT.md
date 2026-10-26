# Active experiment boundary: recli checkpoint 2

Checkpoint-3 work was prematurely started and has been explicitly **reverted from main**. The former checkpoint-3 files `problems/recli/formatting.py` and `problems/recli/interaction.py` have been deleted. `problems/recli/cli.py` and `configuration.py` were restored from the dedicated checkpoint-2 recovery branch. The recovery tests and evidence are published on main, with identical blob SHAs to the recovery branch.

**No work on checkpoint 3 is authorized until checkpoint 2 is verified and frozen as engineering-complete.**

Latest local test run: `python -m pytest -q tests` from `/mnt/data/cp2finish/problems/recli`, Python 3.13, exit 0, `23 passed in 2.60s`. Compilation: `python -m compileall -q .`, exit 0. These checks used locally reconstructed source. SHA comparison proved byte identity for `cli.py` only; local `configuration.py` and some authored tests were not byte-identical to the exact GitHub blobs. Hence these checks do **not** verify the precise published tree. No held-out evaluator was accessed; live SSH endpoint integration is NOT_RUN. Treat engineering completion as **OPEN**, not certified.

No further checkpoint may be released until the outstanding verification obligations are closed or explicitly reassessed with evidence.
