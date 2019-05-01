import json

from . import protocol_and_address

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


def parse_channel_config(value, force_dict=False):
    try:
        config = json.loads(value)
    except JSONDecodeError:
        # Fallback to string channel config
        config = value
        if force_dict:
            protocol, address = protocol_and_address(value)
            config = {"connection": {
                "protocol": protocol,
                "parameters": {"address": address}
            }}
    return config
