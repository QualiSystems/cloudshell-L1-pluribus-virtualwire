from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

ACTION_MAP = OrderedDict()
ERROR_MAP = OrderedDict([(r'[Ee]rror:', 'Command error')])

ASSOCIATIONS = CommandTemplate('port-association-show format master-ports,slave-ports,name,bidir, parsable-delim ":"',
                               ACTION_MAP, ERROR_MAP)
MAP_UNI = CommandTemplate(
    'port-association-create name {name} master-ports {master_ports} slave-ports {slave_ports} virtual-wire no-bidir',
    ACTION_MAP, ERROR_MAP)
MAP_BIDI = CommandTemplate(
    'port-association-create name {name} master-ports {master_ports} slave-ports {slave_ports} virtual-wire bidir',
    ACTION_MAP, ERROR_MAP)

MAP_CLEAR = CommandTemplate('port-association-delete name {name}', ACTION_MAP, ERROR_MAP)
