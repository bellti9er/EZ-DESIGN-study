import curses
from curses import wrapper
from typing import List

from command import AddCharacterCommand, BackspaceCommand, EvaluateCommand, UndoCommand
from memento import Caretaker


class Calculator:
    def __init__(self) -> None:
        self.caretaker = Caretaker()
        self.expression: str = ""
        self.results: List[str] = []

    def add_character(self, character: str) -> None:
        self.expression += character

    def backspace(self) -> None:
        self.expression = self.expression[:-1]

    def evaluate(self) -> None:
        try:
            result = eval(self.expression)

            if not isinstance(result, float):
                result = float(result)

            formatted_result = f"{self.expression} = {result:.3f}"
            self.results.append(formatted_result)
            self.caretaker.backup(self.expression)
            self.expression = f"{result:.3f}"
        except Exception:
            self.expression = "Invalid syntax"

    def undo(self) -> None:
        if len(self.results) > 0:
            self.results.pop()
            if len(self.results) > 0:
                self.expression = self.caretaker.undo().split(" = ")[0]
            else:
                self.expression = ""


def main(stdscr) -> None:
    calc = Calculator()
    curses.echo()

    while True:
        stdscr.clear()
        stdscr.addstr(
            0,
            0,
            "Press 'q' to quit\nPress 'backspace' to delete\nPress 'enter' to calculate\nPress 'u' to undo\n",
        )

        height, width = stdscr.getmaxyx()

        for idx, result in enumerate(calc.results):
            result_x_position = width - len(result) - 1
            stdscr.addstr(idx + 1, result_x_position, result)

        stdscr.addstr(height - 1, 0, calc.expression)

        stdscr.refresh()
        ch = stdscr.getkey()

        if ch == "q":
            break
        elif ch == "\n":
            EvaluateCommand(calc).execute()
        elif ch == "u":
            UndoCommand(calc).execute()
        elif ch == "\x7f" or ch == "\x08":
            BackspaceCommand(calc).execute()
        else:
            AddCharacterCommand(calc, ch).execute()


wrapper(main)
