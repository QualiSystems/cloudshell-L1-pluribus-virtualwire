from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict()
ERROR_MAP = OrderedDict([(r'[Ee]rror:', 'Command error')])

SWITCH_INFO = CommandTemplate('switch-info-show format model,chassis-serial', ACTION_MAP, ERROR_MAP)
SWITCH_SETUP = CommandTemplate('switch-setup-show format switch-name', ACTION_MAP, ERROR_MAP)
SOFTWARE_VERSION = CommandTemplate('software-show', ACTION_MAP, ERROR_MAP)
PORT_SHOW = CommandTemplate('port-config-show format port,speed,autoneg parsable-delim ":"', ACTION_MAP, ERROR_MAP)
PHYS_PORT_SHOW = CommandTemplate('bezel-portmap-show format port,bezel-intf parsable-delim ":"', ACTION_MAP, ERROR_MAP)
ASSOCIATIONS = CommandTemplate('port-association-show format master-ports,slave-ports,bidir, parsable-delim ":"',
                               ACTION_MAP, ERROR_MAP)
