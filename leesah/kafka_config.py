"""Create configuration for Kafka clients."""

from pathlib import Path
from typing import Dict
import yaml
from yaml.loader import SafeLoader


def base_config(path_to_cert: str) -> Dict:
    """Create a base configuration for Kafka clients."""
    creds = yaml.load(Path(path_to_cert).open(mode="r").read(),
                      Loader=SafeLoader)

    config = {
        "bootstrap.servers": creds["broker"],
        "security.protocol": "SSL",
        "ssl.ca.pem": creds["ca"],
        "ssl.key.pem": creds['user']["access_key"],
        "ssl.certificate.pem": creds['user']["access_cert"]
    }

    return config


def consumer_config(path_to_cert: str, group_id: str, auto_commit: bool):
    """Create a configuration for Kafka consumers."""
    config = base_config(path_to_cert)
    return config | {
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": str(auto_commit)
    }


def producer_config(path_to_cert: str):
    """Create a configuration for Kafka producers."""
    return base_config(path_to_cert) | {
        "broker.address.family": "v4"
    }
