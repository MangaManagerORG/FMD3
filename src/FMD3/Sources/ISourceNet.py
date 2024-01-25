"""
Contains interface to configure source net settings
"""
import requests
# from aiohttp import ClientSession, TCPConnector
import asyncio


class ISourceNet:
    _session = None

    # @property
    # def session(self) -> ClientSession:
    #     if self._session is None:
    #         self._session = self.create_session()
    #     return self._session

    # def create_session(self) -> ClientSession:
    #     """
    #     Override this method to configure the session and connection settings more specifically.
    #     """
    #     connector = TCPConnector(limit=5)  # Example: Setting connection limit to 5
    #     session = ClientSession(connector=connector)
    #     return session
    @property
    def session(self):
        if self._session is None:
            self._session = self.create_session()
        return self._session

    @staticmethod
    def create_session():
        """
        Override this method to configure the session and connection settings more specifically.
        """
        return requests.Session()
        # Make sure to close the session when the instance is destroyed
