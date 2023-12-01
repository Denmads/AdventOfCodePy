from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class Node(Generic[T]):
    value: T
    is_end: bool = field(default=False)
    next: 'Node' = field(default=None)


class Stack(Generic[T]):
    
    def __init__(self):
        self.head: Node = Node[str]("END", is_end=True)
        self.length: int = 0

    def push(self, val: T) -> None:
        node = Node[T](val, next=self.head)
        self.head = node

        self.length += 1

    def pop(self) -> Node[T]:
        if self.head.is_end:
            raise RuntimeError("Trying to pop an empty stack.")

        self.length -= 1

        node = self.head
        self.head = node.next
        return node
    
    def peek(self) -> T:
        if self.head.is_end:
            raise RuntimeError("Cannot peek empty stack.")

        return self.head.value

    def transfer_to(self, other: 'Stack[T]', amount: int) -> None:
        if amount > self.length:
            raise RuntimeError("Trying to move more values than possible.")

        cnt = amount
        node = self.head
        while cnt > 0:
            old_next = node.next
            node.next = other.head
            other.head = node
            
            self.length -= 1
            other.length += 1

            node = old_next
            cnt -= 1

        self.head = node

    def transfer_to_without_restack(self, other: 'Stack[T]', amount: int) -> None:
        if amount > self.length:
            raise RuntimeError("Trying to move more values than possible.")

        cnt = amount - 1
        orig_head = self.head
        node = self.head
        while cnt > 0:
            node = node.next
            cnt -= 1

        self.head = node.next
        node.next = other.head
        other.head = orig_head

        self.length -= amount
        other.length += amount


    def __len__(self):
        return self.length

    def __str__(self):
        output = []
        node = self.head

        while not node.is_end:
            output.append(node.value)
            node = node.next
        
        return "->".join(map(lambda x: str(x), output))