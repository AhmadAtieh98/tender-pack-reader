"""The AI layer (session 09): a model retrieves evidence, reasons and PROPOSES changes; deterministic code owns
calculations, dates, comparisons, validation, state transitions and publication.

    contract.py    one typed contract for claims and change proposals (StateIdentity, EvidenceRef, Statement,
                   ChangeProposal, ProposalSet); the JSON schema the model is given is trimmed from it
    tools.py       narrow read-only tools over the existing modules (search, unit/group/crop retrieval, state
                   comparison, approved date calculations, amendment and programme simulation, validation) and the
                   one writer, `request_review`, which writes to staging/ only
    controller.py  the orchestration: task packet -> provider turns with tool calls -> strict parse -> validation
                   (the controller, never the model, assigns verification_status) -> impact -> staging
    budget.py      caps, the price table, the persistent spend meter and the per-addendum orchestrator lock
    providers/     recorded (offline tests), anthropic, openrouter, ollama (application routes) and host (a coding
                   host drives the same tools through MCP or the CLI and submits a proposal file; no API call)

Nothing here writes to curation/, config/, build/ or out/. Models may write proposals to staging only; they never
approve, never edit source evidence, never change validation policy, never execute generated code and never publish.
`tenderpack ai promote RUN_ID --by NAME` (a person) copies verified items into curation as PROPOSED drafts.
"""
