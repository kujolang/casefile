# External Blockers

blockers:
  - id: process-result-normalization-contract
    command: "execute_status / ProcessResult access"
    evidence: "CaseFile preserves adapters for legacy dict-shaped results, missing fields, and non-string stderr/stdout so failure receipts remain stable; direct native field access would change the error contract."
    status: needs-contract-first
    next_action: "Define a typed ProcessResult compatibility contract for missing fields and null streams, then replace the defensive adapter with native fields and regression fixtures."
