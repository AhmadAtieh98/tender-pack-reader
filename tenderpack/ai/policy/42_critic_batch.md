# Critic reply: several items

The request lists SEVERAL items, each with its own key; the units they cite are printed once under `units`. Review each item on its own evidence. Reply with ONLY a JSON object: {"reviews": [{"item": "<the item's key>", "agrees": true|false, "concerns": ["..."], "evidence_checked": ["unit ids or the quotations you checked"]}]}, one review per item listed. `agrees` true means the item follows from the evidence shown; it is not an approval.
