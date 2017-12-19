#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

import virtual_wire.command_templates.autoload as command_template
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class AutoloadActions(object):
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

    def board_table(self):
        """
        :rtype: dict
        """
        board_table = {}
        info_out = CommandTemplateExecutor(self._cli_service, command_template.SWITCH_INFO).execute_command()

        board_table.update(self._parse_data(info_out.strip()))

        sw_version_out = CommandTemplateExecutor(self._cli_service, command_template.SOFTWARE_VERSION).execute_command()
        board_table.update(self._parse_data(sw_version_out.strip()))

        sw_setup_out = CommandTemplateExecutor(self._cli_service, command_template.SWITCH_SETUP).execute_command()
        board_table.update(self._parse_data(sw_setup_out.strip()))

        return board_table

    def ports_table(self):
        """
        :rtype: dict
        """
        port_table = {}
        port_logic_output = CommandTemplateExecutor(self._cli_service,
                                                    command_template.PORT_SHOW).execute_command()
        for record in port_logic_output.split('\n'):
            port_id, speed, autoneg = re.split(r':\s+', record)
            port_table[port_id] = {'speed': speed, 'autoneg': autoneg}

        return port_table

    @staticmethod
    def _parse_data(out):
        table = {}
        for record in out.split('\n'):
            key, value = re.split(r':\s+', record)
            table[key] = value
        return table
