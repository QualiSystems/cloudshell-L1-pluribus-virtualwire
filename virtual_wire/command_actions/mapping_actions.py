import re

import virtual_wire.command_templates.mapping as command_template
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class MappingActions(object):
    """
    Autoload actions
    """

    def __init__(self, cli_service, logger):
        """
        :param cli_service: default mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def get_associations_table(self):
        associations_table = {}
        associations_output = CommandTemplateExecutor(self._cli_service,
                                                      command_template.ASSOCIATIONS).execute_command()
        for record in re.findall(r'^[\d,-]+:[\d,-]+:[\w-]+:\w+$', associations_output, flags=re.MULTILINE):
            master_ports, slave_ports, name, bidir = re.split(r':', record)
            master_ports = master_ports.strip()
            slave_ports = slave_ports.strip()
            name = name.strip()
            bidir = bidir.strip()
            associations_table[name] = {'master_ports': master_ports,
                                        'slave_ports': slave_ports,
                                        'bidir': bidir.lower == 'true'}
        return associations_table

    def create_uni(self, master_ports, slave_ports, name):
        associations_output = CommandTemplateExecutor(self._cli_service, command_template.MAP_UNI).execute_command(
            master_ports=master_ports, slave_ports=slave_ports, name=name)
        return associations_output

    def create_bidi(self, master_ports, slave_ports, name):
        associations_output = CommandTemplateExecutor(self._cli_service, command_template.MAP_BIDI).execute_command(
            master_ports=master_ports, slave_ports=slave_ports, name=name)
        return associations_output

    def delete(self, name):
        associations_output = CommandTemplateExecutor(self._cli_service, command_template.MAP_CLEAR).execute_command(
            name=name)
        return associations_output
