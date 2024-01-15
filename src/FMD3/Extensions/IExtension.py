import abc


class IExtension(abc.ABC):
    ...
    extension_name = None

    @abc.abstractmethod
    def print_ext_name(self):
        print(f"Extension name: {self.extension_name}")
