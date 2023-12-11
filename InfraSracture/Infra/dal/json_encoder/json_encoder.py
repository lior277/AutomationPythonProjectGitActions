# Custom JSON encoder to handle ObjectId serialization
import json

from bson import ObjectId


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)  # Convert ObjectId to its string representation
        return json.JSONEncoder.default(self, o)