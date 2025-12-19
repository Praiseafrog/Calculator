from typing import Any
from typing import Self

class Node:
    def __init__(self, data:Any , pre:Self|None = None, next:Self|None = None) -> None:
        self.pre = pre
        self.next = next
        self.data = data
    
    def __repr__(self) -> str:
        n = self.get_head()
        a = ""
        while n != None:
            a += str(n.data)
            a += ", "
            n = n.next
        a = a[:-2]
        return f"{a} ({self.data})"
    
    def insert(self, object:Any) -> None:
        if isinstance(object, Node):
            temp = self.next
            
            self.next = object
            object.pre = self
            while object.next != None:
                object = object.next
            object.next = temp

            if temp:
                temp.pre = object
            
        else:
            o = Node(object,self,self.next)
            if self.next:
                self.next.pre = o
            self.next = o
        
    
    def pop(self) -> Self:
        if self.next:
            self.next.pre = self.pre
        if self.pre:
            self.pre.next = self.next
        return self
    
    def set(self, object) -> None:
        self.data = object
    
    def get_head(self) -> Self:
        node = self
        while node.pre:
            node = node.pre
        return node
    
    def deepcopy(self) -> Self:
        node = self
        node = node.get_head()
        new = Node(self.data)
        while node.next:
            new.insert(Node(node.next.data))
            new = new.next
            node = node.next
        return new.get_head()
    
    def deepprint(self) -> None:
        node = self.get_head()
        while node != None:
            print(node)
            node = node.next


        


if __name__ == "__main__":
    a = Node(0)
    a.insert(2)
    a.insert(1)
    print(a)
    b = a.deepcopy()
    print(b, b.next, b.next.next)
    print(a is a.deepcopy())