"""
Contains interface to configure source net settings
"""

from aiohttp import ClientSession, TCPConnector
import asyncio


class ISourceNet:
    _session: ClientSession | None = None

    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self._session = self.create_session()
        return self._session

    def create_session(self) -> ClientSession:
        """
        Override this method to configure the session and connection settings more specifically.
        """
        connector = TCPConnector(limit=5)  # Example: Setting connection limit to 5
        session = ClientSession(connector=connector)
        return session

        # Make sure to close the session when the instance is destroyed

    def __del__(self):
        if self._session:
            asyncio.ensure_future(self._session.close())