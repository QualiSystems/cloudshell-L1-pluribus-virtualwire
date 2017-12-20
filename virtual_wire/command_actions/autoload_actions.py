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
        logic_ports_output = CommandTemplateExecutor(self._cli_service,
                                                     command_template.PORT_SHOW).execute_command()

        phys_ports = self.phys_ports_table()
        for record in re.findall(r'^\d+:.+:.+$', logic_ports_output, flags=re.MULTILINE):
            port_id, speed, autoneg = re.split(r':', record.strip())
            port_id = port_id
            speed = speed
            autoneg = autoneg
            phys_id = phys_ports.get(port_id)
            if phys_id:
                port_table[port_id] = {'speed': speed, 'autoneg': autoneg, 'phys_id': phys_id}

        return port_table

    def phys_ports_table(self):
        phys_ports_table = {}
        phys_ports_output = CommandTemplateExecutor(self._cli_service,
                                                    command_template.PHYS_PORT_SHOW).execute_command()
        for record in re.findall(r'^\d+:.+$', phys_ports_output, flags=re.MULTILINE):
            logical_id, phys_id = re.split(r':', record.strip())
            phys_ports_table[logical_id] = phys_id

        return phys_ports_table

    @staticmethod
    def _parse_ports(ports):
        port_list = []
        single_records = ports.split(',')
        for record in single_records:
            if '-' in record:
                start, end = map(int, record.split("-"))
                range_list = map(str, range(start, end + 1))
            else:
                range_list = [record]
            port_list.extend(range_list)
        return port_list

    def associations(self):
        associations_table = {}
        associations_output = CommandTemplateExecutor(self._cli_service,
                                                      command_template.ASSOCIATIONS).execute_command()
        for record in associations_output.split('\n'):
            master_ports, slave_ports, name, bidir = re.split(r':', record)
            master_ports = master_ports.strip()
            slave_ports = slave_ports.strip()
            name = name.strip()
            bidir = bidir.strip()
            master_ports_list = self._parse_ports(master_ports)
            slave_ports_list = self._parse_ports(slave_ports)
            if bidir.lower() == 'true':
                for port in slave_ports_list:
                    associations_table[port] = {'name': name,
                                                'slave_ports': master_ports_list,
                                                'bidir': bidir.lower() == 'true'}
            for port in master_ports_list:
                associations_table[port] = {'name': name,
                                            'slave_ports': slave_ports_list,
                                            'bidir': bidir.lower() == 'true'}
        return associations_table

    @staticmethod
    def _parse_data(out):
        table = {}
        for record in out.split('\n'):
            key, value = re.split(r':\s+', record)
            table[key] = value
        return table
