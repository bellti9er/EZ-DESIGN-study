# Week 1

factory, builder 패턴에 대해 공부합니다.

</br>

## Lecture

- [factory method](https://refactoring.guru/design-patterns/factory-method)
- [abstract factory](https://refactoring.guru/design-patterns/abstract-factory)
- [builder](https://refactoring.guru/design-patterns/builder)

### Factory Method

- `factory method` 는 객체 생성을 처리하는 클래스와 인스턴스화 되는 객체를 분리함으로써, 객체 생성에 필요한 인터페이스를 제공하는 패턴
  - 해당 패턴은 상위 클래스에서 객체 생성 인터페이스를 정의하지만, 서브 클래스에서 생성될 객체의 타입을 결정 할 수 있게 해줌. 이를 통해 factory method 패턴은 클라이언트 프로그래밍에서 객체의 생성과 클래스의 구현을 느슨하게 결합시켜 객체 생성 과정의 유연성을 높여줌.

### abstract factory

- `abstract factory` 는 관련된 여러 객체의 집합을 생성하는 인터페이스를 제공하는 패턴
  - 해당 패턴은 factory method 패턴을 확장하여, 각 팩토리가 여러 종류의 객체를 생성할 수 있도록 함.
  - 즉, abstract factory 는 일련의 관련된 객체를 생성하기 위한 인터페이스를 제공하고, 구체적인 factory class 는 이 인터페이스를 구현하여 실제 객체를 생성함.

### builder

- `builder` 는 복잡한 객체의 조립 방식과 그 결과물을 분리하여, 같은 조립 절차로 여러 가지 결과물을 만들 수 있게 하는 패턴
  - 해당 패턴은 객체의 구성 요소와 이를 조립하는 과정을 분리함으로써, 클라이언트 코드에서는 단계별로 객체를 구성할 수 있음

</br>

## Assignment

CPU, RAM, ROM으로 구성된 Computer를 구현합니다.

- CPU는 추상클래스입니다.
  - 일반적인 Factory 패턴으로 구현해 주세요.
  - CPUFactory에서 SingleCoreCPU, DoubleCoreCPU를 생성할 수 있습니다.
- RAM, ROM은 추상 클래스 Memory를 상속받습니다.
  - 각각은 Factory를 가지며, 각각의 Factory도 공통의 추상 클래스를 상속받게 Abstract factory 패턴으로 구현해 주세요.
- Computer는 Builder 패턴으로 구현해 주세요.
  - bootstrap을 하고 나면 아래 키를 가지는 dict 타입의 state를 반환합니다.
    - cpu processed
      - cpu가 process한 data list
    - ram(rom) data
      - ram(rom)의 현재 data

</br>

## Apply

```python
class CPUFactory:
    @staticmethod
    def make_cpu(type):
        if type == "single":
            return SingleCoreCPU()  # Factory Method 패턴: 객체 생성을 서브 클래스에 위임
        elif type == "dual":
            return DualCoreCPU()  # CPU 타입에 따라 다른 객체를 생성
        else:
            raise ValueError("Invalid CPU type :", type)
```

- `CPUFactory` 클래스는 `Factory Method` 패턴의 구현
  - 이 패턴의 목적은 객체 생성 과정을 서브 클래스로 캡슐화하여 클라이언트 코드가 구체 클래스에 의존하지 않도록 하는 것
  - 여기서 `make_cpu` 메서드는 CPU 객체를 생성하는 팩토리 메서드 역할을 함.
  - 클라이언트는 CPUFactory 를 통해 SingleCoreCPU 또는 DualCoreCPU 객체를 생성할 수 있으며, 생성 과정에서 필요한 로직은 CPUFactory 내부에 캡슐화

</br>

```python
class MemoryFactory(ABC):
    @abstractmethod
    def make_memory(size, data):
        pass

class RamFactory(MemoryFactory):
    @staticmethod
    def make_memory(size=None, data=None):
        return RAM(size=size)  # RAM 객체 생성

class RomFactory(MemoryFactory):
    @staticmethod
    def make_memory(size=None, data=None):
        return ROM(data=data)  # ROM 객체 생성
```

- `MemoryFactory`와 그 구현체들(`RamFactory`, `RomFactory`)은 `Abstract Factory` 패턴의 구현
  - 이 패턴의 목적은 관련있는 객체들을 생성하기 위한 인터페이스를 제공하고, 클라이언트는 이 인터페이스를 통해 필요한 객체를 생성함.
  - 여기서 RamFactory와 RomFactory는 MemoryFactory 인터페이스를 구현하여, 클라이언트가 RAM 또는 ROM 객체를 생성할 수 있게 함.
  - 이 패턴을 통해 메모리 타입에 따른 객체 생성 로직을 각 팩토리 클래스로 캡슐화하여, 클라이언트 코드의 의존성을 줄일 수 있음

</br>

```python
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

        return Computer(cpu=cpu, ram=ram, rom=rom)  # 복잡한 객체 조립
```

- `ComputerBuilder` 클래스는 `Builder` 패턴의 구현
  - 이 패턴의 목적은 복잡한 객체의 조립 과정과 그 결과물을 분리하여, 같은 조립 절차로 여러 가지 결과물을 만들 수 있도록 하는 것
  - 여기서 `build_computer` 메서드는 Computer 객체를 조립하는 과정을 담당함.
  - 클라이언트는 ComputerBuilder를 통해 다양한 타입의 컴퓨터(laptop, desktop)를 생성할 수 있으며, 각 타입에 따라 필요한 구성 요소(CPU, RAM, ROM)를 조립함.
  - 이 패턴을 통해 복잡한 객체 조립 과정을 캡슐화하여, 클라이언트 코드의 복잡성을 줄일 수 있음

</br>

## Tests

```shell
╭─     ~/Desktop/bellti9er/EZ-DESIGN-study/week1/tests     main !2 ────────────────────────────────────────────────────────── ✔  20:42:27   ─╮
╰─ pytest                                                                                                                                            ─╯
================================================================= test session starts ==================================================================
platform darwin -- Python 3.9.17, pytest-8.0.0, pluggy-1.4.0
rootdir: /Users/jongbeom/Desktop/bellti9er/EZ-DESIGN-study/week1/tests
configfile: pytest.ini
collected 9 items

test_computer.py .........                                                                                                                       [100%]

================================================================== 9 passed in 0.01s ===================================================================
```

</br>
