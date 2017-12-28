class ActionsManager(object):
    def __init__(self, actions_instance, cli_service):
        self._actions_instance = actions_instance
        self._cli_service = cli_service

    def __enter__(self):
        self._actions_instance.cli_service = self._cli_service
        return self._actions_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._actions_instance.cli_service = None
