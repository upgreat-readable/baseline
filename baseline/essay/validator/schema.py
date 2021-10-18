from typing import Final

SCHEMA_ESSAY: Final[dict] = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Read//able essay structure",
    "description": "",
    "type": "object",
    "required": ["meta", "text"],
    "properties": {
        "meta": {
            "description": "Meta information of the essay",
            "type": "object",
            "required": ["id", "theme", "subject", "taskText"],
            "properties": {
                "id": {
                    "type": "string",
                    "minLength": 7,
                },
                "uuid": {
                    "type": "string",
                    "minLength": 26,
                },
                "theme": {
                    "type": "string"
                },
                "class": {
                    "type": "string",
                    "default": ""
                },
                "year": {
                    "type": "number"
                },
                "category": {
                    "type": "string",
                    "default": ""
                },
                "test": {
                    "type": "string",
                    "default": ""
                },
                "subject": {
                    "type": "string",
                    "minLength": 3,
                },
                "taskText": {
                    "type": "string",
                    "default": ""
                },
                "expert": {
                    "type": "string",
                    "default": ""
                },
                "name": {
                    "type": "string",
                    "default": ""
                }
            },
        },
        "text": {
            "description": "Text of the essay",
            "type": "string",
            "minLength": 50,
        },
        "selections": {
            "description": "Selections for the essay",
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "startSelection", "endSelection", "type", "group"],
                "properties": {
                    "id": {
                        "type": "number"
                    },
                    "startSelection": {
                        "type": "integer"
                    },
                    "endSelection": {
                        "type": "integer"
                    },
                    "type": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "comment": {
                        "type": "string",
                        "default": ""
                    },
                    "explanation": {
                        "type": "string",
                        "default": ""
                    },
                    "correction": {
                        "type": "string",
                        "default": ""
                    },
                    "tag": {
                        "type": "string",
                        "default": ""
                    },
                    "group": {
                        "type": "string",
                        "default": ""
                    },
                    "subtype": {
                        "type": "string",
                        "default": ""
                    },
                },
            },
        },
    },
}
