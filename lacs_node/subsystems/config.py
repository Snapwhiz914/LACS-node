from schema import Schema
from yaml.scanner import ScannerError
from yaml.parser import ParserError
import yaml
import sys
import syslog

conf_schema = Schema({
    "key": str,
    "bind_addr": str,
    "port": int
})

def get_config_object():
    try:
        file_obj = open("/etc/lacs-node.yaml", "r")
        result = yaml.safe_load(file_obj)
        validated = conf_schema.validate(result)
        return validated
    except FileNotFoundError as e:
        syslog.syslog(syslog.LOG_ALERT, "Config file not found.")
        sys.exit(1)
    except ScannerError as e:
        syslog.syslog(syslog.LOG_ALERT, f"YAML scanner error when trying to load config: {e}")
        sys.exit(1)
    except ParserError as e:
        syslog.syslog(syslog.LOG_ALERT, f"YAML Parser error: check config syntax: {e}")
        sys.exit(1)