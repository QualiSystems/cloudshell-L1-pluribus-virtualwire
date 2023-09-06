from __future__ import annotations

import re
from typing import TYPE_CHECKING

from cloudshell.cli.command_template.command_template_executor import (
    CommandTemplateExecutor,
)

import pluribus_virtualwire.command_templates.system as command_template

if TYPE_CHECKING:
    from cloudshell.cli.service.cli_service import CliService


class SystemActions:
    """System actions."""

    def __init__(self, cli_service: CliService) -> None:
        self._cli_service = cli_service
        self.__phys_to_logical_table: dict = {}

    @property
    def cli_service(self) -> CliService:
        return self._cli_service

    @cli_service.setter
    def cli_service(self, cli_service: CliService):
        self._cli_service = cli_service

    def _build_phys_to_logical_table(self) -> dict[str, str]:
        logical_to_phys_dict = {}
        output = CommandTemplateExecutor(
            self._cli_service, command_template.PHYS_TO_LOGICAL
        ).execute_command()
        for phys_id, logical_id in re.findall(
            r"^([\d\.]+):(\d+)$", output, flags=re.MULTILINE
        ):
            logical_to_phys_dict[phys_id] = logical_id
        return logical_to_phys_dict

    @property
    def _phys_to_logical_table(self) -> dict[str, str]:
        if not self.__phys_to_logical_table:
            self.__phys_to_logical_table = self._build_phys_to_logical_table()
        return self.__phys_to_logical_table

    def _get_logical(self, phys_name: str) -> str:
        logical_id = self._phys_to_logical_table.get(phys_name)
        if logical_id:
            return logical_id
        else:
            raise Exception("Cannot convert physical port name to logical")

    def get_state_id(self) -> str:
        state_id = CommandTemplateExecutor(
            self._cli_service, command_template.GET_STATE_ID
        ).execute_command()
        return re.split(r"\s", state_id.strip())[1]

    def set_state_id(self, state_id: str) -> str:
        out = CommandTemplateExecutor(
            self._cli_service, command_template.SET_STATE_ID
        ).execute_command(state_id=state_id)
        return out

    def set_auto_negotiation(self, phys_port: str, value: str):
        logical_port_id = self._get_logical(phys_port)
        if value.lower() == "true":
            CommandTemplateExecutor(
                self._cli_service, command_template.SET_AUTO_NEG_ON
            ).execute_command(port_id=logical_port_id)
        else:
            CommandTemplateExecutor(
                self._cli_service, command_template.SET_AUTO_NEG_OFF
            ).execute_command(port_id=logical_port_id)
