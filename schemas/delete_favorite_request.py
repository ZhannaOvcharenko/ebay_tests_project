delete_favorite_request = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "entities": {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "entityIds": {
                            "type": "array",
                            "items": [{"type": "integer"}]
                        },
                        "entityType": {"type": "string"}
                    },
                    "required": ["entityIds", "entityType"]
                }
            ]
        }
    },
    "required": ["entities"]
}
