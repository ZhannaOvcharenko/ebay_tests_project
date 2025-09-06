add_favorite_response = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "watchlistItemId": {"type": "string"},
        "ack": {"type": "string"}
    },
    "required": ["ack"]
}
