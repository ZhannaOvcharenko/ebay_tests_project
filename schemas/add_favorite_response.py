add_favorite_response = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "isAdded": {"type": "boolean"},
        "favoriteId": {"type": "integer"}
    },
    "required": ["isAdded"]
}
