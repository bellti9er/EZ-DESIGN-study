from abc import ABC, abstractmethod

# Memory, RAM, ROM
class Memory(ABC):
    @abstractmethod
    def __init__(self, size, data=None):
        self.size = size if size is not None else len(data if data else [])
        self.data = data if data is not None else [0] * self.size

    @abstractmethod
    def read(self, address):
        pass

    @abstractmethod
    def write(self, address, value):
        pass


class RAM(Memory):
    def __init__(self, size, data=None):
        super().__init__(size, data)

    def read(self, address):
        return self.data[address]

    def write(self, address, value):
        self.data[address] = value


class ROM(Memory):
    def __init__(self, size=None, data=None):
        super().__init__(size, data)

    def read(self, address):
        return self.data[address]

    def write(self, address, value):
        raise ValueError("Can't write to ROM, only read")


# MemoryFactory, RamFactory, RomFactory
class MemoryFactory(ABC):
    @abstractmethod
    def make_memory(size, data):
        pass


class RamFactory(MemoryFactory):
    @staticmethod
    def make_memory(size=None, data=None):
        if data is not None:
            raise ValueError("Can't initialize RAM with data")
        return RAM(size=size)


class RomFactory(MemoryFactory):
    @staticmethod
    def make_memory(size=None, data=None):
        if size is not None:
            raise ValueError("Can't initialize ROM with size")
        return ROM(data=data)
