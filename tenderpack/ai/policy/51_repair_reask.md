# Repair turn (the closing instruction of an application route's re-ask)

Reply again with ONLY the corrected JSON object described by `schema` in the packet: the whole object, every item, fixing what is listed (this is the one re-ask: an item that still fails its schema is set aside as malformed; a reference that still fails is rated by the controller). An item's `statements` lists only ids of entries of the set's `statements`.
