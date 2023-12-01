import importlib
import os
from typing import Any

class TaskInterface:
    
    @staticmethod
    def parse_input(input: str) -> Any:
        """Parses the input"""
    
    @staticmethod
    def run_a(input: Any) -> None:
        """Runs part a"""

    @staticmethod
    def run_b(input: Any) -> None:
        """Runs part b"""
    

def _import_task(name: str) -> TaskInterface:
    return importlib.import_module(name)

def load_task(day: str) -> TaskInterface:
    try: 
        task = _import_task(f"tasks.{day}")
        return task
    except ImportError as e:
        print(e)
        print(f"No task found with name: {day}.py")
        exit(1)

    
def load_input(day: str) -> str:
    try:
        with open(f"inputs/{day}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"No input with name: {day}.txt")
        exit(1)
        