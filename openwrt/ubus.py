import json
import logging

import requests

RPC_VERSION = "2.0"
INIT_SESSION_ID = "00000000000000000000000000000000"

logging.captureWarnings(True)
_LOGGER = logging.getLogger(__name__)

class Ubus:
    """Interacts with the OpenWrt ubus API."""

    @staticmethod
    def connect(host, username, password, timeout=15, verify=False):
        """Create and authenticate a new session."""

        session = __class__(host, timeout, verify)

        result = session.call_rpc(
            "session", "login",
            {
                "username": username,
                "password": password,
            },
        )
        if "ubus_rpc_session" not in result:
            raise PermissionError("Login Failed. Check host credentials.")
        session.session_id = result["ubus_rpc_session"]

        return session

    def __init__(self, host, timeout, verify):
        self.host = host
        self.timeout = timeout
        self.verify = verify

        self.rpc_id = 1
        self.session_id = None

    def call_api(self, rpc_method, *params):
        """Perform API call."""
        _LOGGER.debug(
            'api call: rpc_method="%s" params="%s"',
            rpc_method,
            params,
        )

        params = [self.session_id or INIT_SESSION_ID, *params]

        data = json.dumps(
            {
                "jsonrpc": RPC_VERSION,
                "id": self.rpc_id,
                "method": rpc_method,
                "params": params,
            }
        )
        _LOGGER.debug('api call: data="%s"', data)

        self.rpc_id += 1
        try:
            response = requests.post(
                self.host, data=data, timeout=self.timeout, verify=self.verify
            )
        except requests.exceptions.RequestException as e:
            _LOGGER.error("api_call exception: %s", e)
            raise e

        response.raise_for_status()

        json_response = response.json()

        _LOGGER.debug(
            'api call: status="%s" response="%s"',
            response.status_code,
            response.text,
        )

        if "error" in json_response:
            raise RuntimeError(json_response["error"]["message"])

        return json_response["result"]

    def call_rpc(self, subsystem, method, params={}):
        result = self.call_api("call", subsystem, method, params)

        if result[0] != 0:
            raise Exception(f"RPC returned non-zero exit code: {result[0]}")
        if len(result) > 1:
            return result[1]

    def read_file(self, path):
        """Read file from device."""
        result = self.call_rpc(
            "file",
            "read",
            {
                "path": path
            }
        )
        return result["data"]

    def write_file(self, path, data, mode=0o600):
        self.call_rpc(
            "file",
            "write",
            {
                "path": path,
                "mode": mode,
                "data": data
            }
        )

    def append_file(self, path, data, mode=0o600):
        try:
            data = self.read_file(path) + data
        except Exception:
            pass
        self.write_file(path, data, mode)

    def get_uci_config(self, config, type):
        """Get UCI config."""
        result = self.call_rpc(
            "uci",
            "get",
            {
                "config": config,
                "type": type,
            }
        )
        return result["values"]
