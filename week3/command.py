from abc import ABC, abstractmethod
from typing import Any


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
