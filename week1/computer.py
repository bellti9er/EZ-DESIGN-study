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
            "rom_data": self.rom.data
        }
    
class ComputerBuilder:
    @staticmethod
    def build_computer(type):
        if type == "laptop":
            cpu = CPUFactory.make_cpu(type="single")
            ram = RamFactory.make_memory(size=8)
            rom = RomFactory.make_memory(data=[1, 2, 3, 4])
        elif type == "desktop":
            cpu = CPUFactory.make_cpu(type="dual")
            ram = RamFactory.make_memory(size=16)
            rom = RomFactory.make_memory(data=[1, 2, 3, 4, 5, 6, 7, 8])
        else:
            raise ValueError("Invalid computer type :", type)
        
        return Computer(cpu=cpu, ram=ram, rom=rom)
    