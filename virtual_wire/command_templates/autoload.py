from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict()
ERROR_MAP = OrderedDict([(r'[Ee]rror:', 'Command error')])

SWITCH_INFO = CommandTemplate('switch-info-show', ACTION_MAP, ERROR_MAP)
SWITCH_SETUP = CommandTemplate('switch-setup-show', ACTION_MAP, ERROR_MAP)
