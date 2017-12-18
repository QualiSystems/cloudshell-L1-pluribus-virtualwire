import virtual_wire.command_templates.system as command_template
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class SystemActions(object):
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

    def get_state_id(self):
        state_id = CommandTemplateExecutor(self._cli_service, command_template.GET_STATE_ID).execute_command()
        return state_id

    def set_state_id(self, state_id):
        out = CommandTemplateExecutor(self._cli_service, command_template.SET_STATE_ID).execute_command(
            state_id=state_id)
        return out
