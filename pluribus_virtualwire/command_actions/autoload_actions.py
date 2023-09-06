from __future__ import annotations

import re
from typing import TYPE_CHECKING

from cloudshell.cli.command_template.command_template_executor import (
    CommandTemplateExecutor,
)

import pluribus_virtualwire.command_templates.autoload as command_template

if TYPE_CHECKING:
    from cloudshell.cli.service.cli_service import CliService


class AutoloadActions:
    """Autoload actions."""

    def __init__(self, cli_service: CliService) -> None:
        self._cli_service = cli_service

    def board_table(self) -> dict[str, str]:
        """Build board table."""
        board_table = {}
        info_out = CommandTemplateExecutor(
            self._cli_service, command_template.SWITCH_INFO
        ).execute_command()

        board_table.update(self._parse_data(info_out.strip()))
        sw_version_out = CommandTemplateExecutor(
            self._cli_service, command_template.SOFTWARE_VERSION
        ).execute_command()

        board_table.update(self._parse_data(sw_version_out.strip()))
        sw_setup_out = CommandTemplateExecutor(
            self._cli_service, command_template.SWITCH_SETUP
        ).execute_command()

        board_table.update(self._parse_data(sw_setup_out.strip()))

        return board_table

    def ports_table(self) -> dict[str, dict[str, str]]:
        """Build ports table."""
        port_table = {}
        logic_ports_output = CommandTemplateExecutor(
            self._cli_service, command_template.PORT_SHOW
        ).execute_command()

        phys_ports = self.phys_ports_table()
        for rec in re.findall(r"^\d+:.+:.+$", logic_ports_output, flags=re.MULTILINE):
            port_id, speed, autoneg = re.split(r":", rec.strip())
            phys_id = phys_ports.get(port_id)
            if phys_id:
                port_table[port_id] = {
                    "speed": speed,
                    "autoneg": autoneg,
                    "phys_id": phys_id,
                }

        return port_table

    def phys_ports_table(self) -> dict[str, str]:
        """Build physical ports table."""
        phys_ports_table = {}
        phys_ports_output = CommandTemplateExecutor(
            self._cli_service, command_template.PHYS_PORT_SHOW
        ).execute_command()
        for rec in re.findall(r"^\d+:.+$", phys_ports_output, flags=re.MULTILINE):
            logical_id, phys_id = re.split(r":", rec.strip())
            phys_ports_table[logical_id] = phys_id

        return phys_ports_table

    @staticmethod
    def _validate_port(port: str) -> None:
        if re.search(r"[-,]", port):
            raise Exception(
                "Cannot build mappings, driver does not support port ranges"
            )

    def associations_table(self) -> dict[str, str]:
        """Build port mapping table."""
        associations_table = {}
        associations_output = CommandTemplateExecutor(
            self._cli_service, command_template.ASSOCIATIONS
        ).execute_command()
        for rec in re.findall(
            r"^[\d,-]+:[\d,-]+:\w+$", associations_output, flags=re.MULTILINE
        ):
            master_ports, slave_ports, bidir = re.split(r":", rec.strip())
            self._validate_port(master_ports)
            self._validate_port(slave_ports)
            if bidir.lower() == "true":
                associations_table[master_ports] = slave_ports
                associations_table[slave_ports] = master_ports
            else:
                associations_table[slave_ports] = master_ports
        return associations_table

    @staticmethod
    def _parse_data(out: str) -> dict[str, str]:
        table = {}
        for rec in out.splitlines():
            if re.search(r":\s+", rec):
                key, value = re.split(r":\s+", rec)[:2]
                table[key] = value
        return table
