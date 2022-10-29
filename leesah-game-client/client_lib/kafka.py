from pathlib import Path
from typing import Dict


def base_config(bootstrap_servers: str) -> Dict:
    config = {
        "bootstrap.servers": bootstrap_servers
    }
    if "localhost" not in bootstrap_servers:
        CA_PATH = Path("certs/ca.pem")
        KEYSTORE = Path("certs/service.cert")

        assert CA_PATH.is_file()
        assert KEYSTORE.is_file()

        config = config | {
                    "security.protocol": "SSL",
                    "ssl.check.hostname": "true",
                    "ssl.ca.location": CA_PATH,
                    "ssl.keystore.location": KEYSTORE,
                    "ssl.keystore.password": "changeme"
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
