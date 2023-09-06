from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.layer_one.core.driver_commands_interface import DriverCommandsInterface
from cloudshell.layer_one.core.helper.logger import get_l1_logger
from cloudshell.layer_one.core.layer_one_driver_exception import LayerOneDriverException
from cloudshell.layer_one.core.response.response_info import (
    AttributeValueResponseInfo,
    GetStateIdResponseInfo,
    ResourceDescriptionResponseInfo,
)

from pluribus_virtualwire.autoload.autoload import Autoload
from pluribus_virtualwire.cli.vw_cli_handler import VWCliHandler
from pluribus_virtualwire.command_actions.autoload_actions import AutoloadActions
from pluribus_virtualwire.command_actions.mapping_actions import MappingActions
from pluribus_virtualwire.command_actions.system_actions import SystemActions
from pluribus_virtualwire.helpers.actions_helper import ActionsManager

if TYPE_CHECKING:
    from cloudshell.layer_one.core.helper.runtime_configuration import (
        RuntimeConfiguration,
    )

logger = get_l1_logger(name=__name__)


class DriverCommands(DriverCommandsInterface):
    """Driver commands implementation."""

    def __init__(self, runtime_config: RuntimeConfiguration) -> None:
        self._runtime_config = runtime_config
        self._cli_handler = VWCliHandler(runtime_config)

        self.__mapping_actions: MappingActions | None = None
        self.__system_actions: SystemActions | None = None

    @property
    def _mapping_actions(self) -> MappingActions:
        if not self.__mapping_actions:
            self.__mapping_actions = MappingActions(cli_service=None)
        return self.__mapping_actions

    @property
    def _system_actions(self) -> SystemActions:
        if not self.__system_actions:
            self.__system_actions = SystemActions(cli_service=None)
        return self.__system_actions

    def login(self, address: str, username: str, password: str) -> None:
        """Perform login operation on the device."""
        self._cli_handler.define_session_attributes(address, username, password)
        with self._cli_handler.default_mode_service() as session:
            autoload_actions = AutoloadActions(session)
            logger.info(autoload_actions.board_table())
            self.__mapping_actions = None
            self.__system_actions = None

    def get_state_id(self) -> GetStateIdResponseInfo:
        """Check if CS synchronized with the device."""
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._system_actions, session) as system_actions:
                return GetStateIdResponseInfo(system_actions.get_state_id())

    def set_state_id(self, state_id: str) -> None:
        """Set synchronization state id to the device.

        Called after Autoload or SyncFomDevice commands.
        """
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._system_actions, session) as system_actions:
                system_actions.set_state_id(state_id)

    def map_bidi(self, src_port: str, dst_port: str) -> None:
        """Create a bidirectional connection between source and destination ports."""
        logger.info(f"MapBidi: SrcPort: {src_port}, DstPort: {dst_port}")
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._mapping_actions, session) as mapping_actions:
                src_logical_port = self._convert_port_address(src_port)
                dst_logical_port = self._convert_port_address(dst_port)
                mapping_actions.map_bidi(src_logical_port, dst_logical_port)

    def map_uni(self, src_port: str, dst_ports: list[str]) -> None:
        """Unidirectional mapping of two ports."""
        logger.info(f"MapUni: SrcPort: {src_port}, DstPort: {', '.join(dst_ports)}")
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._mapping_actions, session) as mapping_actions:
                mapping_actions.map_uni(
                    self._convert_port_address(src_port),
                    [self._convert_port_address(port) for port in dst_ports],
                )

    def get_resource_description(self, address: str) -> ResourceDescriptionResponseInfo:
        """Auto-load function to retrieve all information from the device."""
        logger.info(f"GetResourceDescriprion for: {address}")
        with self._cli_handler.default_mode_service() as session:
            autoload_actions = AutoloadActions(session)
            boart_table = autoload_actions.board_table()
            ports_table = autoload_actions.ports_table()
            association_table = autoload_actions.associations_table()
            autoload_helper = Autoload(
                address, boart_table, ports_table, association_table
            )
            return ResourceDescriptionResponseInfo(autoload_helper.build_structure())

    def map_clear(self, ports: list[str]) -> None:
        """Remove simplex/duplex connection ending on the destination port."""
        logger.info(f"MapClear: Ports: {', '.join(ports)}")
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._mapping_actions, session) as mapping_actions:
                mapping_actions.map_clear(
                    [self._convert_port_address(port) for port in ports]
                )

    def map_clear_to(self, src_port: str, dst_ports: list[str]) -> None:
        """Remove simplex/duplex connection ending on the destination port."""
        logger.info(
            f"MapClearTo: SrcPort: {src_port}, DstPorts: {', '.join(dst_ports)}"
        )
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._mapping_actions, session) as mapping_actions:
                mapping_actions.map_clear_to(
                    self._convert_port_address(src_port),
                    [self._convert_port_address(port) for port in dst_ports],
                )

    def get_attribute_value(
        self, cs_address: str, attribute_name: str
    ) -> AttributeValueResponseInfo | None:
        """Retrieve attribute value from the device."""
        if attribute_name == "Serial Number":
            if len(cs_address.split("/")) == 1:
                with self._cli_handler.default_mode_service() as session:
                    autoload_actions = AutoloadActions(session)
                    board_table = autoload_actions.board_table()
                    return AttributeValueResponseInfo(board_table.get("chassis-serial"))
            else:
                return AttributeValueResponseInfo("NA")
        else:
            raise LayerOneDriverException("GetAttributeValue command is not supported")

    def set_attribute_value(
        self, cs_address: str, attribute_name: str, attribute_value: str
    ) -> None:
        """Set attribute value to the device."""
        if attribute_name == "Auto Negotiation":
            with self._cli_handler.default_mode_service() as session:
                with ActionsManager(self._system_actions, session) as system_actions:
                    system_actions.set_auto_negotiation(
                        self._convert_port_address(cs_address), attribute_value
                    )
        else:
            raise LayerOneDriverException(
                f"SetAttributeValue for address {cs_address} is not supported"
            )

    def map_tap(self, src_port: str, dst_ports: list[str]) -> None:
        logger.info(f"MapTap: SrcPort: {src_port}, DstPorts: {', '.join(dst_ports)}")
        with self._cli_handler.default_mode_service() as session:
            with ActionsManager(self._mapping_actions, session) as mapping_actions:
                mapping_actions.map_tap(
                    self._convert_port_address(src_port),
                    [self._convert_port_address(port) for port in dst_ports],
                )

    def set_speed_manual(self, src_port: str, dst_port: str, speed: str, duplex: str):
        """Set connection speed.

        DEPRECATED. Is not used with the new standard
        """
        raise NotImplementedError

    @staticmethod
    def _convert_port_address(port: str) -> str:
        return port.split("/")[-1]
