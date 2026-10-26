# Sequential release and freeze protocol

1. Authorize exactly one checkpoint using its pinned public `checkpoint_N.md`; do not open future specs or benchmark solutions.
2. Record released problem, checkpoint, benchmark commit, requirement blob SHA, prior implementation SHA, tool version and skill registry version.
3. Review newly relevant unbound questions first, applicable code-linked questions and up to five highest-priority existing questions independently. Drop unjustified obsolete knowledge.
4. Record actual technique use, its hypothesized benefit and evidence. Keep tool/skill changes in distinct paths and commits where practical.
5. Implement in `problems/<problem>/` and test all required public tests, plus relevant prior regressions even where the benchmark opts out. Separate official-policy vs supplemental results.
6. Capture raw command/argv, cwd, environment fingerprint, timeout, source identity, stdout, stderr, exit code and timeout flag. Store interpretation separately.
7. Run versioned architecture/maintenance sensors and their own tests. Record parse coverage, hotspot mass, peak complexity, boundary responsibility, dependency growth and edit localization. Avoid inferring architectural quality from scalar metrics alone.
8. Audit sensor blind spots and skill negative transfer; add positive and negative controls before claiming a measurement fix.
9. Freeze with explicit PASS/FAIL/NOT_RUN for each gate. Do not release next checkpoint without a freeze and commit SHA.
10. Local success is not official evaluator correctness. Simulations are scoped evidence only.

## Continuity caveat
A single agent in one conversation does not provide formal information-flow isolation, even when future checkpoint files remain unopened. Conflicts or unintended exposure must be logged rather than erased.
