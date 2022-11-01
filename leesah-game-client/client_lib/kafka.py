import json
from pathlib import Path
from typing import Dict


def base_config(bootstrap_servers: str) -> Dict:
    config = {
        "bootstrap.servers": bootstrap_servers
    }
    if "localhost" not in bootstrap_servers:
        CA_PATH = Path("certs/ca.pem")
        creds = json.loads(Path("certs/leesah_creds.json").open(mode="r").read())

        config = config | {
                    "security.protocol": "SSL",
                    "ssl.ca.location": CA_PATH,
                    "ssl.key.pem": creds["key"],
                    "ssl.certificate.pem": creds["cert"]
                }
    return config


def consumer_config(bootstrap_servers: str, group_id: str, auto_commit: bool):
    config = base_config(bootstrap_servers)
    return config | {
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": str(auto_commit)
    }


def producer_config(bootstrap_servers: str):
    return base_config(bootstrap_servers)
