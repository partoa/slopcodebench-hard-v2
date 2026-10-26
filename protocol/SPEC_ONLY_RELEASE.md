# Spec-only release protocol

Pinned benchmark: `gabeorlanski/scb-problems@9cd9ca3a51c3d3e2a99d2488a25baf73a2204451`.

1. Before release: name only current problem/stage and verify stage is next and previous freeze exists. Do not retrieve a future stage.
2. Fetch **only** the exact current `checkpoint_N.md` and `config.yaml` for that problem. Record exact URL/commit, hash and read log. Metadata is not an invitation to enumerate test files or solution trees.
3. Implement from released specifications and generic repertoire. Write own tests independently, with oracle provenance.
4. Run all relevant authored regressions; capture raw results and environment. Verify explicit requirements with application-level behavior, not just test totals.
5. Record structure and change localization, tool blind spots, crosswalk, negative transfers and effort. Improve only justified techniques/tools and run their controls.
6. Commit app code, own tests, evidence and skill changes. Freeze including source identities and honest unverified cases.
7. Only after committed freeze may the next stage be fetched.

Evaluation firewall: official evaluator tests and scoring remain outside the implementing repository and session. External evaluation may be performed separately after freeze without communicating hidden test content, failures or scores back into active implementation context. Publishing a numeric official score to the implementer could itself bias later checkpoints.

For a repeated problem such as recli, the new session should neither import old chat memory nor inspect old implementation branches. This is a fresh engineering attempt but not demonstrably statistically blind to historical model training or remembered experience.
