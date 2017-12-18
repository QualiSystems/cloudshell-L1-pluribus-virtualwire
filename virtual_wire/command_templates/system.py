from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict()
ERROR_MAP = OrderedDict([(r'[Ee]rror:', 'Command error')])

GET_STATE_ID = CommandTemplate('switch-setup-show parsable-delim ; format motd', ACTION_MAP, ERROR_MAP)
SET_STATE_ID = CommandTemplate('switch-setup-modify motd {state_id}', ACTION_MAP, ERROR_MAP)
