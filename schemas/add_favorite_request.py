add_favorite_request = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "entityId": {"type": ["integer", "null"]},
        "dealType": {"type": "string"},
        "entityType": {"type": "string"},
        "addToFolder": {"type": "boolean"}
    },
    "required": ["entityId", "dealType", "entityType", "addToFolder"]
}
