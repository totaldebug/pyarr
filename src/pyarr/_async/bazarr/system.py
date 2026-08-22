import httpx

from pyarr._async.common.base import CommonActions
from pyarr.exceptions import PyarrConnectionError
from pyarr.types import JsonObject


class BazarrSystem(CommonActions):
    """System actions for Bazarr.

    Bazarr is a Flask application rather than a Servarr one, so it does not answer the
    shared :class:`pyarr._async.common.system.System` paths. Only ``system/status`` is
    spelled the same way; health is ``system/health``, tasks are ``system/tasks``, and
    restart and shutdown are a single ``POST system`` carrying an ``action`` parameter.
    There is no diskspace or routes endpoint at all.

    Getting this wrong is unusually easy to miss: Bazarr answers any unmatched ``/api/``
    path with its single page application's HTML at HTTP 200 rather than a 404, so a
    wrong path returns a page instead of raising.
    """

    async def get_status(self) -> JsonObject:
        """Gets system status.

        Returns:
            JsonObject: Dictionary with the status wrapped in a ``data`` key.
        """
        return await self._get("system/status")

    async def get_health(self) -> JsonObject:
        """Get health information.

        Returns:
            JsonObject: Dictionary with the health issues wrapped in a ``data`` key.
        """
        return await self._get("system/health")

    async def get_tasks(self, task_id: str | None = None) -> JsonObject:
        """Get the scheduled tasks.

        Args:
            task_id (str | None, optional): Return a single task by ID. Defaults to None,
                which returns every task.

        Returns:
            JsonObject: Dictionary with the tasks wrapped in a ``data`` key.
        """
        params = {"taskid": task_id} if task_id else None
        return await self.handler.request("system/tasks", params=params)

    async def run_task(self, task_id: str) -> None:
        """Run a scheduled task now.

        Args:
            task_id (str): ID of the task to run.
        """
        await self.handler.request("system/tasks", method="POST", params={"taskid": task_id})

    #: httpx failures that mean the request reached Bazarr and the connection was then
    #: dropped, which is exactly what Bazarr does while restarting or shutting down. A
    #: ``ConnectError`` is deliberately absent: that means Bazarr was never reached, and
    #: the caller does need to hear about it.
    _CONNECTION_DROPPED = (httpx.RemoteProtocolError, httpx.ReadError)

    async def _request_action(self, action: str) -> None:
        """Asks Bazarr to restart or shut down.

        Unlike the Servarr applications, Bazarr closes the connection while acting on this
        rather than answering first, so a dropped connection is the expected outcome and is
        swallowed. Anything else, including never reaching Bazarr at all, still raises.

        Args:
            action (str): Either ``restart`` or ``shutdown``.
        """
        try:
            await self.handler.request("system", method="POST", params={"action": action})
        except PyarrConnectionError as exception:
            if not isinstance(exception.__cause__, self._CONNECTION_DROPPED):
                raise

    async def request_restart(self) -> None:
        """Request a Bazarr restart.

        Returns:
            None: Bazarr drops the connection as it restarts rather than answering.
        """
        await self._request_action("restart")

    async def request_shutdown(self) -> None:
        """Request a Bazarr shutdown.

        Returns:
            None: Bazarr drops the connection as it shuts down rather than answering.
        """
        await self._request_action("shutdown")
