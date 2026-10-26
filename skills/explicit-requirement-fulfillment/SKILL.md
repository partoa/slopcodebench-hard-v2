---
name: explicit-requirement-fulfillment
description: Prevent closing a checkpoint while any released explicit requirement lacks observable, boundary-level fulfillment evidence.
---
# Verify every stated requirement

Before inferring further responsibilities, enumerate each *released* explicit requirement with a stable ID, exact authorized source, conditions, independently justified expected behavior, execution boundary, negative/failure cases when required, implementation link and evidence link. Do not read future specifications or solutions.

Run the actual entrypoint in a clean declared environment. Check normal, edge, invalid and partial-failure paths as demanded by the contract. A helper-level test, a simulated dependency or a passing aggregate test count cannot substitute for a required observable behavior.

Mark each requirement VERIFIED_LOCAL, VERIFIED_EXTERNAL, FAILED, BLOCKED, INCONCLUSIVE or NOT_RUN. Record environment, actual results and evidence scope. Reopen a claim after any relevant change or contradictory observation. Fail engineering acceptance if **any** explicit requirement is not verified at the justified scope; freezing an incomplete benchmark submission is permitted but must be labeled INCOMPLETE.

After explicit requirements, perform recurring obligation-method crosswalk for inferred and design-created responsibilities too. Consider each core applicability axis separately and record actual technique applications, not labels. When an obligation is resolved, trace authority → reasoning need → method → implementation → runtime effect → evidence. Preserve unknowns and legitimately inapplicable methods; never create record quotas.

The acceptance criterion for this skill is behavior preservation and demonstrable requirement coverage, not the number of ledger records. Use contrasting positive/negative examples and independently validate this procedure on new tasks before claiming a general effectiveness gain.
