---
name: audit-analysis-findings
description: Assess whether analysis findings identify a justified engineering responsibility or useful hypothesis, and whether acting on them improves outcomes rather than generating noise or metric-driven changes.
---

# Audit the finding-to-decision chain

Structural facts, correlations, risk hypotheses, contract violations and demonstrated improvement are different claims. Determine which one the tool actually supports.

For a consequential finding, identify:

- The exact observed fact and its source/version.
- The authority or domain relationship connecting it to a responsibility or risk.
- The affected consumer, invariant, resource or future change scenario.
- The distinguishing evidence that could confirm or falsify the interpretation.
- The decision the finding could legitimately change.

A complexity threshold does not establish harmful complexity. Co-occurring names do not establish an invariant. An AST change does not establish that an obligation is now violated. Conversely, an unchanged function does not establish that changed dependencies leave its commitments intact.

Challenge a finding with a plausible benign case. Challenge a quiet tool with a known violation within its claimed scope. For classifiers or detectors, record true/false positives, false negatives, inconclusive cases and unsupported cases where the oracle permits that distinction. Keep calibration conditional on the tested population; development fixtures do not provide untouched confirmation evidence.

Assess downstream utility as well as detection. Track whether the agent inspected, rejected, confirmed, acted on or deferred the finding, and why. A justified decision not to change code can be useful. Count generated artifacts only as artifacts, not learning or architectural progress.

When an action follows, compare relevant behavior, change effort, runtime/resource cost, maintainability evidence or later transfer before and after. Check new harms and unnecessary changes. Attribute the result cautiously when several interventions changed together. Do not convert a successful fix to a supplied example into evidence of unaided future discovery.

Triage by significance, evidence strength, expected information value and investigation cost. Deduplicate related findings and expose shared causes. Retire or narrow repeatedly unhelpful detectors instead of endlessly appending recognizers. Retain valuable low-frequency findings when their consequences justify them.

Keep a concise disposition trail: **finding → hypothesis or obligation → challenge → decision → consequence → limits**. If the chain stops at a hypothesis, say so. This skill should improve the agent's decisions, not require a prose dossier for every harmless metric.
