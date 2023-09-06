from __future__ import annotations

from cloudshell.cli.command_template.command_template import CommandTemplate

ERROR_MAP: dict = {r"[Ee]rror:": "Command error"}

GET_STATE_ID = CommandTemplate("switch-setup-show format motd", error_map=ERROR_MAP)
SET_STATE_ID = CommandTemplate(
    "switch-setup-modify motd {state_id}", error_map=ERROR_MAP
)
SET_AUTO_NEG_ON = CommandTemplate(
    "port-config-modify port {port_id} autoneg", error_map=ERROR_MAP
)
SET_AUTO_NEG_OFF = CommandTemplate(
    "port-config-modify port {port_id} no-autoneg", error_map=ERROR_MAP
)
PHYS_TO_LOGICAL = CommandTemplate(
    'bezel-portmap-show format bezel-intf,port parsable-delim ":"', error_map=ERROR_MAP
)
