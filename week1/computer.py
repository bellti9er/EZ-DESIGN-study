from cpu import CPUFactory
from memory import RamFactory, RomFactory


class Computer:
    def __init__(self, cpu, ram, rom):
        self.cpu = cpu
        self.ram = ram
        self.rom = rom

    def bootstrap(self):
        return {
            "cpu_processed": self.cpu.process(self.rom.data),
            "ram_data": self.ram.data,
            "rom_data": self.rom.data,
        }


class ComputerBuilder:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.rom = None

    def set_cpu(self, type):
        self.cpu = CPUFactory.make_cpu(type=type)
        return self

    def set_ram(self, size):
        self.ram = RamFactory.make_memory(size=size)
        return self

    def set_rom(self, data):
        self.rom = RomFactory.make_memory(data=data)
        return self

    def build(self):
        if not self.cpu or not self.ram or not self.rom:
            raise ValueError("Missing components for Computer construction")
        return Computer(cpu=self.cpu, ram=self.ram, rom=self.rom)
