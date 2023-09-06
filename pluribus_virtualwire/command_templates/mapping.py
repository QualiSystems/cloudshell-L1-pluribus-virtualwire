from __future__ import annotations

from cloudshell.cli.command_template.command_template import CommandTemplate

ERROR_MAP: dict = {
    r"[Ee]rror:": "Command error",
    r"[Cc]onflict": "Port conflict",
    r"[Pp]ort\s[Aa]ssoc\w*ation\s.+\salready\sexists": "Port association already exists",  # noqa: E501
    r"[Uu]nable to find port-association to delete": "Unable to find port-association to delete",  # noqa: E501
}

ASSOCIATIONS = CommandTemplate(
    "port-association-show "
    'format master-ports,slave-ports,name,bidir,monitor-ports parsable-delim ":"',
    error_map=ERROR_MAP,
)
MAP_UNI = CommandTemplate(
    "port-association-create name {name} master-ports {master_ports} slave-ports {slave_ports} virtual-wire no-bidir",  # noqa: E501
    error_map=ERROR_MAP,
)
MAP_BIDI = CommandTemplate(
    "port-association-create name {name} master-ports {master_ports} slave-ports {slave_ports} virtual-wire bidir",  # noqa: E501
    error_map=ERROR_MAP,
)
MAP_CLEAR = CommandTemplate("port-association-delete name {name}", error_map=ERROR_MAP)
PHYS_TO_LOGICAL = CommandTemplate(
    'bezel-portmap-show format bezel-intf,port parsable-delim ":"', error_map=ERROR_MAP
)
MODIFY_MONITOR_PORTS = CommandTemplate(
    'port-association-modify name {name} monitor-ports "{ports}" virtual-wire',
    error_map=ERROR_MAP,
)
IS_ENABLED = CommandTemplate(
    'port-config-show port {port} format intf,enable parsable-delim ":"',
    error_map=ERROR_MAP,
)
