from abc import ABC, abstractmethod


class CPU(ABC):
    @abstractmethod
    def process(self, data):
        pass


class SingleCoreCPU(CPU):
    def process(self, data):
        return [data]


class DualCoreCPU(CPU):
    def process(self, data):
        return [data[::2], data[1::2]]


class CPUFactory:
    @staticmethod
    def make_cpu(type):
        if type == "single":
            return SingleCoreCPU()
        elif type == "dual":
            return DualCoreCPU()
        else:
            raise ValueError("Invalid CPU type :", type)
