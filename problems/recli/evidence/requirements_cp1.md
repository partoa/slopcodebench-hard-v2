# Checkpoint 1 requirement and freeze audit

Source: pinned recli/checkpoint_1.md; evaluator material not accessed.

| IDs | Released behaviors | Implementation | Local check | Status |
|---|---|---|---|---|
| R01-R04 | entrypoint, top-level sorted aligned help, hierarchical dispatch, parent usage | appctl, CLI.register/run/help | real subprocess + tree | VERIFIED_LOCAL |
| R05-R07 | aliases, --help, --version rewrites | CLI._resolve/run | CLI tree and subprocess | VERIFIED_LOCAL |
| R08-R12 | positional, keyed, boolean, generic field and optional/repeating synopsis | signature, CLI._parse | handler-boundary test | VERIFIED_LOCAL (sample signatures) |
| R13-R17 | missing/excess positionals, associative required/unknown, error streams/codes | CLI._parse/run | error-path tests | VERIFIED_LOCAL (sample cases) |
| R18-R20 | strict global flag ordering, synonym only if registered, deterministic sort/suggestions | CLI.run/_suggest/_sorted | synonym test only | INCONCLUSIVE (strict mode and determinism not exhaustively exercised) |

Crosswalk: contract verification APPLIES, implemented with original tests and entrypoint. State-machine lifecycle DOES_NOT_APPLY (stateless checkpoint). Integration APPLIES for actual executable, tested under Python subprocess. Negative-path coverage APPLIES, incomplete for some global-parameter boundary cases. Architecture assessment: registration tree, synopsis parser and dispatcher are distinct boundaries within a single module; no unsupported claim of improved maintainability. Tool/skill changes: none. Unbound question: config provides no app-specific command registry; this implementation exposes a registration API rather than guessing commands.

FREEZE STATUS: NOT FROZEN. GitHub publication not yet verified. External evaluator not run. This record is honest local evidence only, not an official benchmark score.
