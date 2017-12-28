import re

import virtual_wire.command_templates.mapping as command_template
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class MappingActions(object):
    """
    Autoload actions
    """

    def __init__(self, cli_service, logger):
        """
        :param logger:
        :type logger: Logger
        :return:
        """
        self._logger = logger
        self._cli_service = cli_service

        self.__associations_table = None
        self.__phys_to_logical_table = None

    @property
    def cli_service(self):
        return self._cli_service

    @cli_service.setter
    def cli_service(self, cli_service):
        self._cli_service = cli_service

    def _build_associations_table(self):
        associations_table = {}
        output = CommandTemplateExecutor(self._cli_service, command_template.ASSOCIATIONS).execute_command()
        for master_port, slave_port, name in re.findall(r'^(\d+):(\d+):([\w-]+)$', output, flags=re.MULTILINE):
            associations_table[name] = [master_port, slave_port]
        return associations_table

    @property
    def _associations_table(self):
        if not self.__associations_table:
            self.__associations_table = self._build_associations_table()
        return self.__associations_table

    def _build_phys_to_logical_table(self):
        logical_to_phys_dict = {}
        output = CommandTemplateExecutor(self._cli_service, command_template.PHYS_TO_LOGICAL).execute_command()
        for phys_id, logical_id in re.findall(r'^([\d\.]+):(\d+)$', output, flags=re.MULTILINE):
            logical_to_phys_dict[phys_id] = logical_id
        return logical_to_phys_dict

    @property
    def _phys_to_logical_table(self):
        if not self.__phys_to_logical_table:
            self.__phys_to_logical_table = self._build_phys_to_logical_table()
        return self.__phys_to_logical_table

    def _get_logical(self, phys_name):
        logical_id = self._phys_to_logical_table.get(phys_name)
        if logical_id:
            return logical_id
        else:
            raise Exception(self.__class__.__name__, 'Cannot convert physical port name to logical')

    def _find_associations(self, port):
        result = []
        for association, ports in self._associations_table.iteritems():
            if port in ports:
                result.append(association)
        return result

    def _find_uni_association(self, ports):
        for association, as_ports in self._associations_table.iteritems():
            if ports == as_ports:
                return association

    def map_uni(self, master_port, slave_ports):
        logical_master_id = self._get_logical(master_port)
        command_executor = CommandTemplateExecutor(self._cli_service, command_template.MAP_UNI)
        exception_messages = []
        for slave_port in slave_ports:
            try:
                logical_slave_id = self._get_logical(slave_port)
                command_executor.execute_command(master_ports=logical_master_id, slave_ports=logical_slave_id,
                                                 name='{0}-uni-{1}'.format(logical_master_id, logical_slave_id))
            except Exception as e:
                if len(e.args) > 1:
                    exception_messages.append(e.args[1])
                elif len(e.args) == 1:
                    exception_messages.append(e.args[0])
        if exception_messages:
            raise Exception(self.__class__.__name__, ', '.join(exception_messages))

    def map_bidi(self, master_port, slave_port):
        logical_master_id = self._get_logical(master_port)
        logical_slave_id = self._get_logical(slave_port)
        associations_output = CommandTemplateExecutor(self._cli_service, command_template.MAP_BIDI).execute_command(
            master_ports=logical_master_id, slave_ports=logical_slave_id,
            name='{0}-bidi-{1}'.format(logical_master_id, logical_slave_id))
        return associations_output

    def map_clear(self, ports):
        command_executor = CommandTemplateExecutor(self._cli_service, command_template.MAP_CLEAR)
        exception_messages = []
        for port in ports:
            try:
                port_id = self._get_logical(port)
                associations = self._find_associations(port_id)
                if associations:
                    for association_name in associations:
                        command_executor.execute_command(name=association_name)
                        del self._associations_table[association_name]
            except Exception as e:
                if len(e.args) > 1:
                    exception_messages.append(e.args[1])
                elif len(e.args) == 1:
                    exception_messages.append(e.args[0])
        if exception_messages:
            raise Exception(self.__class__.__name__, ', '.join(exception_messages))

    def map_clear_to(self, master_port, slave_ports):
        map_clear_command_executor = CommandTemplateExecutor(self._cli_service, command_template.MAP_CLEAR)
        master_port_logical_id = self._get_logical(master_port)
        exception_messages = []
        for port in slave_ports:
            try:
                port_id = self._get_logical(port)
                association = self._find_uni_association([master_port_logical_id, port_id])
                if association:
                    map_clear_command_executor.execute_command(name=association)
                    del self._associations_table[association]
            except Exception as e:
                if len(e.args) > 1:
                    exception_messages.append(e.args[1])
                elif len(e.args) == 1:
                    exception_messages.append(e.args[0])
        if exception_messages:
            raise Exception(self.__class__.__name__, ', '.join(exception_messages))
