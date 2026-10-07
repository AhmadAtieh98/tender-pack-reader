# Route mechanics (one section is appended to the phase, by route and phase)

## api
Route mechanics (an application route: the program sends this request and reads your reply): the tools you may call are offered with the request ({tools}); their results come back in the conversation. Your final message is the answer the reply-format rule above describes; the program checks it locally and the controller validates it. Nothing you write is kept except through that answer.

## host-submit
Host session rules (they replace the reply-format rule above; every other rule above stands):
A. You work ONLY through the tenderpack MCP tools offered to this session ({tools}); no other tool exists here. The task packet is below: do not call get_task_packet.
B. Where a provision changes, or relies on, a unit read from an image (the packet's `crops` and `image_targets`), call get_crop for that unit and LOOK at the image before you propose; say in the item's model_rationale what the image shows that you relied on (for example the row, the cell or the declaration and its script). submit_proposals is refused until get_crop has been called for every unit in `image_targets`.
C. Check ops with simulate_amendment (and the whole set with validate_proposal) before submitting.
D. When the set is ready, submit it ONCE with submit_proposals(proposal_set=<the JSON object described by `schema`>, host_model=<the host_model value given below>); a second submission in this session is refused and the first one stands, except the one repair its answer may ask for (`repair`: resubmit ONLY the items it names, corrected against the schemas it gives; the others stand). Do not reply with the JSON itself.
E. Then reply with one short line: the run_id and status the tool returned, and which crops you read.

## host-answer
Host session rules: you work ONLY through the tenderpack MCP tools offered to this session ({tools}), read-only; no other tool exists here. The packet is below: do not call get_task_packet. You submit nothing through a tool: your final message is ONLY the JSON object the reply-format rule above describes.

## plain
Session mechanics: no tools are available in this session; everything you need is in the request. Your final message is ONLY the JSON object described above.

## mcp-submit
Coding-host rules (a coding host such as Codex or Claude Code, run by a person over MCP; they replace the reply-format rule above; every other rule above stands):
A. You work through the tenderpack MCP tools. You claimed the addendum with get_task_packet(claim=true); this packet is its result.
B. Where a provision changes, or relies on, a unit read from an image (the packet's `crops`), call get_crop for that unit and LOOK at the image before you propose; say in the item's model_rationale what the image shows that you relied on.
C. Check ops with simulate_amendment (and the whole set with validate_proposal) before submitting.
D. Submit the set ONCE with submit_proposals(proposal_set, host_model), or save it to a file and run the packet's `submit_with` command; the controller validates it exactly as an application route's. Do not edit any file of the pack, the curation or the outputs.

## mcp-answer
Coding-host rules (a coding host run by a person over MCP): read with the tenderpack MCP tools ({tools}), read-only. Save your final JSON object (the reply-format rule above) to a file and run the packet's `workflow.submit_with` command; nothing else is written. Do not edit any file of the pack, the curation or the outputs.
