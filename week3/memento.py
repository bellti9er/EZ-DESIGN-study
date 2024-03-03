from typing import List


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
