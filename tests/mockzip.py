from unittest.mock import MagicMock


class MockZip(MagicMock):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.files = []

    def __iter__(self):
        return iter(self.files)

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return True
    def writestr(self,*args,**kwargs):
        ...
