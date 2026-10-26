# recli checkpoint 2 — final implementation freeze

## Disposition

**ENGINEERING-COMPLETE AT LOCAL CONTRACT-VERIFICATION SCOPE.** This replaces the earlier incomplete experimental freeze and the subsequent recovery status. All released checkpoint-2 requirement families have implemented boundaries and original locally executed checks. External held-out evaluation is explicitly excluded; no official correctness score is asserted. Real SSH connectivity is NOT_RUN because no authorized endpoint was provided; controlled subprocess integration verifies the remote execution boundary, command construction, precommand, propagation of status 255 and the specified error.

## Exact committed source verification

The files from the active `main` branch were independently fetched from GitHub, and their Git blob SHAs were compared to the local test workspace:

- `problems/recli/cli.py`: `a1c63853b32e688171513ab86edcbe90c22a6f5b` — exact match.
- `problems/recli/configuration.py`: `7a0520c40ed066110b7ba297ea9e2c87f80855fe` — exact match.
- `problems/recli/appctl`: `a7001836430e95df43036ada1ad011c31e74cbff`; entrypoint previously published unchanged.

The local test sources include stylistic reconstruction differences from published tests, but they run against **byte-identical published application source**. Original suite versions are retained in the repository.

## Executed commands and raw output

At `/mnt/data/cp2finish/problems/recli` on Linux, Python 3.13, pytest 9.0.2:

```
$ python -m pytest -q tests
..........................                                               [100%]
26 passed in 2.52s
(exit 0; timeout 200 seconds; stderr empty)

$ python -m compileall -q .
(exit 0; stderr/stdout empty)

$ APPCTL_ROOT_DIR=$(mktemp -d) python appctl --version
0.1.0
(exit 0)

$ APPCTL_ROOT_DIR=$(mktemp -d) python appctl
usage: appctl <command> [<args>] [--<flags>]
Commands:
  cli
  help  Show command help
(exit 0)
```

The new completion gate initially produced two failing tests, exposing an invalid file-alias validation gap and missing explicit metadata registration for deprecated/hidden global parameters. Both were corrected on GitHub and retested. An earlier recovery failure caught incorrect `@all` handling of groups; it was also corrected and preserved in the prior evidence.

## Requirement disposition

| Requirement | Evidence |
|---|---|
| Global, nearest project and runtime precedence | CP2 original/configuration and completion tests — VERIFIED_LOCAL |
| Config discovery and file priority | CP2 original tests — VERIFIED_LOCAL |
| YAML inheritance, override, append, cycle detection | CP2 original tests — VERIFIED_LOCAL |
| Global default initialization, file errors | CP2 tests and direct entrypoint — VERIFIED_LOCAL |
| Global allowlist, strict-mode split and negative flags | CP2 boundary and completion tests — VERIFIED_LOCAL |
| Deprecated and hidden global behavior | CP2 completion tests — VERIFIED_LOCAL |
| Disabled commands | CP2 original tests — VERIFIED_LOCAL |
| Alias name validation and runtime overrides | CP2 completion and original tests — VERIFIED_LOCAL |
| Alias grouping, duplicate handling, unknown/suggestions and broadcast ordering | CP2 original and boundary tests — VERIFIED_LOCAL |
| Local path resolution | CP2 original tests — VERIFIED_LOCAL |
| Remote SSH command and precommand; error on 255 | Controlled subprocess mock — VERIFIED_LOCAL at transport adapter only; endpoint NOT_RUN |
| Packages directory precedence | CP2 original tests — VERIFIED_LOCAL |
| Prior checkpoint-1 regression suite | Six prior tests included in 26 — PASS |

## Architecture and crosswalk

Configuration loading and YAML inheritance are in `configuration.py`, while dispatch and command contracts remain in `cli.py`. Obligations with consequence at interfaces were crosswalked to actual tests for positive, negative and integration behavior. Retained negative transfer: first-run auto-create introduces filesystem effects and explicit failure handling. No invented tool improvement claim or external evaluator result. No new skills were needed, and no skill effectiveness claim is inferred from the number of passing tests.

## Experiment release boundary

Checkpoint 2 is **frozen at the published implementation and local verification scope**, with external infrastructure/evaluator limits explicit. Checkpoint 3 was prematurely opened earlier, and its files were subsequently removed from the active `main` tree; historical exposure cannot be erased, but no checkpoint-3 contents were used for this repair. The next authorized implementation begins from the checkpoint-2 code state and must carry forward cumulative authored regressions.
