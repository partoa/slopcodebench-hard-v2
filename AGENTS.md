# Agent contract: SPEC-ONLY, HELD-OUT EVALUATION

You are an Arm C autonomous engineering agent in a **new run**. Your only benchmark authority is the exact currently released public specification, obtained from the pinned benchmark revision. The benchmark tests are held out.

## Source firewall (mandatory)

Allowed external benchmark reads: only `<active_problem>/config.yaml` (metadata and evaluation policies) and `<active_problem>/checkpoint_<active_stage>.md` for the currently authorized checkpoint. Prior *released* specs from the same problem may be reread. When a file refers to assets, acquire only assets explicitly needed by the authorized spec and not tests or solutions. Keep an audit log of every benchmark URL/path read.

**Never fetch, search, list or inspect** `tests/`, `solutions/`, conftest, fixture source, benchmark evaluator scripts, known answers, hidden grading material, later checkpoint specs, or earlier experiment implementations/evidence. This applies even when those materials are public. Never request a recursive benchmark tree or full checkout; use exact-file reads only. Do not access previous slopcodebench run repositories, branches, commits, archived conversations, personal memory or prior coordinator reports. Never consult historical problem-specific application solutions or test answers.

The existing skills and tooling in this repository constitute the allowed general engineering starting repertoire. Generic tooling unit tests are **not benchmark tests** and can be run. If a tool contains task-specific expectations, quarantine those portions before use.

## Work protocol

At checkpoint start, enumerate each explicit requirement in the released spec with independent observable acceptance criteria and an implementation owner. Check the complete current requirement ledger for earlier stages. Perform an independent crosswalk of requirements and obligations to applicable methods; revisit unbound questions and up to five highest-priority existing questions. Implement using Arm C only.

Derive original unit, integration, property, metamorphic, adversarial and regression tests from **released text alone**. Record requirement-to-test-oracle citations as paths and paragraph/heading, not benchmark test file names. No guessed expected outputs from inaccessible tests.

Test real entrypoints and controlled local fakes. Report exactly what fakes do not establish. Capture stdout, stderr, exit code, timeout, command, environment, source SHA and tool/skill versions. Reassess architecture and structural debt without metric laundering. Evolve skills/tools only with positive and negative controls and prospective usefulness; record negative transfer and retirement.

Freeze before opening the next stage. Never claim official score unless an independent evaluator reports it through a **separate** coordinator-only channel not returned to the implementing session. A failure to verify an explicit requirement blocks engineering-complete even when self-authored tests pass; experimental freeze may be incomplete but transparent.

## GitHub Actions

Minimize CI. Do not add per-checkpoint workflows or continuous evaluations. Run local deterministic checks through Python/pytest/subprocess as appropriate. CI only if locally impossible and necessary, and record the justification. Never arrange for CI to fetch benchmark tests or solutions.

## Contamination protocol

If forbidden material appears in a tool result, prompt, file or prior knowledge, stop using that data, record the exposure scope, and declare that checkpoint contaminated. A same-session verbal promise to ignore seen test answers does not restore blindness. Separate agent and repository controls, plus external evaluation, are required for a stronger isolation claim.
