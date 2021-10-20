import json
from config import ENCODING

serialize = lambda value: json.dumps(value).encode(ENCODING)
deserialize = lambda value: json.loads(value.decode(ENCODING))
