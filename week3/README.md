# Week 3

command, memento 패턴에 대해 공부합니다.

</br>

## Lecture

- [memento](https://refactoring.guru/design-patterns/memento)
- [command](https://refactoring.guru/design-patterns/command)

### Memento

- `memento` 는 객체의 이전 상태를 저장하고 복원할 수 있게 해주지만 그 구현 세부 사항을 드러내지 않는 행동 디자인 패턴
  - 해당 패턴은 "실행 취소" 와 같은 기능을 구현하거나 객체의 상태를 특정 시점으로 되돌리는 등의 시나리오에서 유용하게 사용됨
  - 객체의 상태를 저장하는 과정에서 객체의 캡슐화를 깨뜨리지 않으면서 상태 정보에 접근해야 하는 문제를 해결할 수 있음
    - 일반적으로 객체 내부의 상태 정보는 private 으로 보호되기 때문에 외부에서 직접 접근하기 어려움
  - `Originator` : 상태 정보를 가지고 있는 객체로, 메멘토 객체를 생성하여 현재 상태를 저장하고, 메멘토를 사용하여 이전 상태로 복원할 수 있음
  - `Memento` : Originator 객체의 상태를 저장하는 객체. 메멘토는 Originator 외에는 자신의 상태 정보에 접근할 수 없도록 제한하여 캡슐화를 유지함.
  - `Caretaker` : 메멘토 객체를 관리하는 역할을 힘. Caretaker는 메멘토를 생성하거나 사용하는 시점을 결정하지만, 메멘토의 내부 상태에는 접근할 수 없음.


### Command

- `command` 는 요청을 독립된 객체로 변환하여 요청에 관한 모든 정보를 포함시키는 행동 디자인 패턴
  - 이러한 객체 변환을 통해 요청을 메소드 인자로 전달하거나, 요청의 실행을 지연시키거나, 대기열에 넣거나, 실행 취소 가능한 작업을 지원할 수 있게 됨
  - 해당 패턴의 주된 목적은 요청을 객체로 캡슐화 하여, 요청을 발생시키는 객체와 요청을 수행하는 객체 사이의 결합도를 낮추는 것임
  - 애플리케이션에서 요청을 수행하는 방법에 대한 직접적인 호출 대신, 요청을 객체로 만들어 관리함으로 요청에 대한 더 유연한 실행 방법을 제공함
  - 커맨드 패턴은 사용자 인터페이스 버튼 클릭, 메뉴 선택 등과 같이 사용자의 액션에 대응하는 다양한 요청을 처리하거나, 작업의 실행, 취소, 재실행 등을 관리해야 할 때 특히 유용함


</br>

## Assignment

https://github.com/bellti9er/EZ-DESIGN-study/assets/132914700/9c613332-184c-4e30-a968-ff745e030e74

위처럼 동작이 가능한 eval 계산기를 구현합니다.

- [python curses 라이브러리](https://docs.python.org/3/howto/curses.html)를 사용합니다. 아래와 같은 형식이지만 구현만 똑같다면 형식은 자유입니다.
    
    ```python
    from curses import wrapper
    
    def main(stdscr):
        
    	...		
    
      stdscr.refresh()
      stdscr.getkey()
    
    wrapper(main)
    ```
    
- eval 계산기 프로그램이 시작하고 나서
    - 글자를 하나씩 입력하면 맨 아랫줄에 expression에 추가됩니다.
    - backspace를 입력하면 계산기의 expression이 하나씩 지워집니다.
    - enter를 입력하면 `eval(expression)` 의 결과가 오른쪽 위에 하나씩 쌓입니다.
        - 계산 결과가 float이 아닐 경우, 혹은 syntax error가 발생하는 등의 예외 경우에는 그동안의 expression은 `Invalid syntax` 로 expression이 대체됩니다.
            - int output이 나와도 float으로 형변환됩니다.
            - 결과는 `{expression} = {value}` 형식입니다.
- u를 입력하면 이전 상태로 되돌아갑니다.
    - 이전 계산에서 enter를 누르기 직전의 expression을 기억해놨다가 되돌아갑니다.
- q를 입력하면 종료합니다.
- 각각의 동작은 `Command.execute`의 형태로 실행됩니다.
- 이외에 불필요하거나 핵심을 제외한 부분은 refactoring guru의 디자인 패턴과 완전히 동일하지 않아도 됩니다.

</br>

## Apply

```python
# memento.py

class Memento:
    def __init__(self, state: str) -> None:
        self._state = state

    def get_state(self) -> str:
        return self._state


class Caretaker:
    def __init__(self) -> None:
        self._mementos: List[Memento] = []

    def backup(self, state: str) -> None:
        self._mementos.append(Memento(state))

    def undo(self) -> str:
        if not self._mementos:
            return ""
        memento = self._mementos.pop()
        return memento.get_state()

```

- `memento.py` 파일을 통해 메멘토 패턴을 구현
- `Memento` 클래스는 객체의 상태(`state`)를 저장하며 이 경우, 계산기의 현재 `expression` 이 상태로 저장됨
- `Caretaker` 클래스는 이러한 상태들의 기록을 관리함.
  - `backup` 메소드로 현재 상태를 저장하고, `undo` 메소드로 이전 상태를 복원함
- 메멘토 패턴에 따라 객체의 내부 상태를 외부에 노출시키지 않으면서 상태를 관리할 수 있게 함
  - `Caretaker` 는 `Memento` 객체를 통해 상태를 관리하지만, `Memento` 의 내부 상태에는 직접 접근하지 않음


</br>

```python
# command.py

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class AddCharacterCommand(Command):
    def __init__(self, receiver: Any, character: str) -> None:
        self.receiver = receiver
        self.character = character

    def execute(self) -> None:
        self.receiver.add_character(self.character)


class BackspaceCommand(Command):
    def __init__(self, receiver: Any) -> None:
        self.receiver = receiver

    def execute(self) -> None:
        self.receiver.backspace()


class EvaluateCommand(Command):
    def __init__(self, receiver: Any) -> None:
        self.receiver = receiver

    def execute(self) -> None:
        self.receiver.evaluate()


class UndoCommand(Command):
    def __init__(self, receiver: Any) -> None:
        self.receiver = receiver

    def execute(self) -> None:
        self.receiver.undo()

```

- `command.py` 파일을 통해 커맨드 패턴을 구현
- `Command` 추상 클래스는 모든 명령에 공통된 `execute` 메소드를 정의함
- 커맨드 패턴의 핵심은 요청 자체를 캡슐화 하는 것으로, 이를 통해 요청을 발생시킨 객체와 요청을 수행하는 객체를 분리함
  - 구체적인 커맨드 클래스(`AddCharacterCommand`, `BackspaceCommand`, `EvaluateCommand`, `UndoCommand`)는 `Command` 인터페이스를 구현하며, 계산기의 각 동작(문자 추가, 삭제, 계산, 되돌리기)을 실행함

</br>

## Tests

> ⚠️ terminal 테마로 인해 실행파일에서의 텍스트에 대한 가독성이 매우 안좋습니다.. 


https://github.com/bellti9er/EZ-DESIGN-study/assets/132914700/037fe56b-a44b-4225-99d6-6343a96a7501


</br>
