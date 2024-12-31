import json
from jsonschema import validate
from pathlib import Path

def validate_json(json_data):
    schema_path = Path(__file__).parent.parent / 'schema' / 'character.schema.json'
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    try:
        validate(instance=json_data, schema=schema)
        return True
    except Exception as e:
        print(e)
        return False