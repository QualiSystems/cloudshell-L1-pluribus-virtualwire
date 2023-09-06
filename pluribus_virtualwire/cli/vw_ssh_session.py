from __future__ import annotations

from cloudshell.cli.session.ssh_session import SSHSession


class VWSSHSession(SSHSession):
    def _connect_actions(self, prompt: str):
        self.hardware_expect(None, expected_string=prompt, timeout=self._timeout)
