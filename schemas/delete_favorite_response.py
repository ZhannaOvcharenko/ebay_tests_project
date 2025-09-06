delete_favorite_response = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "isDeleted": {"type": "boolean"},
        "deletedIds": {
            "type": "array",
            "items": {"type": "integer"}
        }
    },
    "required": ["isDeleted"]
}
