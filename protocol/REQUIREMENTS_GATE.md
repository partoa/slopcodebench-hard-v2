# Mandatory explicit-requirements gate (Arm C)

This gate complements the uploaded `obligation-method-crosswalk` skill. At every release and freeze:

1. Extract current and inherited **explicit** requirements from authorized releases. Each must have a unique ID and testable criterion.
2. Check real entrypoint operation, environment installation and meaningful negative/failure cases. Real-service validity and fake-service validity are distinct.
3. Link requirement → owned code boundary → observable test command/results → scope, including coverage of non-effects and failure handling.
4. Require one of VERIFIED_LOCAL / VERIFIED_EXTERNAL / FAILED / BLOCKED / INCONCLUSIVE / NOT_RUN for every requirement. Anything other than justified verification blocks **engineering complete**, though it does not prevent an honest experiment freeze.
5. Independently re-crosswalk changes, unbound questions, and top-five existing high-priority questions. Keep interpretations/assumptions separate from explicit requirements.
6. Re-run required cumulative tests and preserve raw streams and source identity. A passed test suite does not override a missing requirement.
7. Run sensor tests and inspect caveats, not just scalar complexity score. No retroactive transfer claims.

This protocol deliberately does not require implementing only one architecture or accepting invented requirements.
