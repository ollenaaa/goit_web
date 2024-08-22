from abc import ABC, abstractmethod


class Output(ABC):
    @abstractmethod
    def print(self, *args, **kwargs):
        pass

    @abstractmethod
    def input(self, *args, **kwargs):
        pass


class CLIOutput(Output):
    def print(self, *args, **kwargs):
        print(*args, **kwargs)

    def input(self, *args, **kwargs):
        return input(*args, **kwargs)