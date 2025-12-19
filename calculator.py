import doubleList as dl 
from typing import Self

digits = "1234567890"
signs = "+-"
operators = "*/" #Plus is converted to operators after it changes the signs of numbers and minus is changed to plus negative
parentheticals = "()[]{}"

class Operator:
    priority = ["/*","+"]
    
    def __init__(self, type:str):
        self.symbol = type
    
    def __repr__(self) -> str:
        return f"o{self.symbol}"

    def calculate(self, tok1: float | Self | None,tok2: float | Self | None) -> dl.Node:
        if self.symbol == "*":
            if type(tok1) is float and type(tok2) is float:
                return dl.Node(tok1 * tok2)

        if self.symbol == "/":
            if type(tok1) is float and type(tok2) is float:
                if tok2 == 0:
                    raise ZeroDivisionError
                return dl.Node(tok1 / tok2)

        if self.symbol == "+":
            if type(tok1) is float and type(tok2) is float:
                return dl.Node(tok1 + tok2)
            elif type(tok2) is int:
                return dl.Node(tok2)
            elif type(tok2) is Operator and tok2.symbol == "-" or "+":
                n = dl.Node(tok1)
                n.insert(tok2)
                return n


        raise ValueError

class Sign:
    def __init__(self, type:str) -> None:
        self.symbol = type
    
    def __repr__(self) -> str:
        return f"~{self.symbol}"
    
    def __neg__(self):
        return Sign("-" if self.symbol == "+" else "+")
    
    def calculate(self, tok1: float | Operator | None,tok2: float | Self) -> dl.Node:
        node = dl.Node(tok1) #first object (always what was already there) (1)+1

        if self.symbol == "-": #last object (what was there or negated version) 1+(1)
            node.insert(-tok2)
        elif self.symbol == "+":
            node.insert(tok2)

        if type(tok1) is float:
            node.insert(Operator("+")) #optional middle object (only if object before was not an operator and thus this should be treated as addition)
        
        if node.data == None:
            node = node.next
        
        return node

def calculate(text: str):
    head = tokenize(text)
    print(f"tokenized to: {head}")
    return evaluate(head)

def evaluate(head:dl.Node) -> float:
    print(f"evaluating {head}")
    node = head
    
    while check_parentheses(head):
        node = evaluate_parentheses(node)

    node = evaluate_signs(node)
    print(f"converted signs to: {node}")

    num:float = evaluate_operators(node).data
    
    assert type(num) == float
    return num

def check_parentheses(head:dl.Node) -> bool:
    node = head
    while node:
        if node.data == "(":
            return True

        node = node.next

    return False

    

def evaluate_parentheses(head : dl.Node) -> dl.Node:
    temp = head.deepcopy()
    count = 0

    while temp != None: #iterates through a copy of the list to trim only whats inside parentheses

        if temp.data == "(":
            count += 1
            if count == 1:
                temp = temp.next
                temp.pre = None
                continue

        
        if temp.data == ")":
            count -= 1
            if count == 0:
                temp = temp.pre
                temp.next = None
                break
        
        if temp.next != None:
            temp = temp.next
        else:
            break
    
    node = head
    while node != None: #iterates through the actual list to find where to paste the evaluated segment

        if node.data == "(":
            if node.pre and type(node.pre.data) == float:
                node.pre.insert(Operator("*"))
            count += 1
            if count == 1:
                l = node

        
        if node.data == ")":
            if node.next and type(node.next.data) == float:
                node.insert(Operator("*"))
            count -= 1
            if count == 0:
                r = node
                break
        
        node = node.next

    solved = evaluate(temp.get_head())
    l.data = solved
    try:
        l.next = r.next
        l.next.pre = l
    except:
        l.next = None
    
    return head


def evaluate_signs(head : dl.Node) -> dl.Node:
    
    node = head

    while True:

        if type(node.data) == Sign:

            pre = node.pre.pop().data if type(node.pre) is dl.Node else None
            next = node.next.pop().data if type(node.next) is dl.Node else None

            node.insert(node.data.calculate(pre, next))
            node.pop()

        if node.next:
            node = node.next
        else:
            break


    return node.get_head()


def evaluate_operators(head : dl.Node) -> dl.Node:
    
    node = head

    for ops in Operator.priority:

        while True:

            if type(node.data) == Operator and node.data.symbol in ops:

                pre = node.pre.pop().data if type(node.pre) is dl.Node else None
                next = node.next.pop().data if type(node.next) is dl.Node else None

                node.insert(node.data.calculate(pre, next))
                node.pop()

            if node.next:
                node = node.next
            else:
                break
        
        node = node.get_head()
        print(f"converted operators {ops} to {node}")


    return node.get_head()

def tokenize(text:str) -> dl.Node:
    currnum = "" 
    head = dl.Node(None)
    currnode = head

    for char in text:

        if char in digits or char == ".":
            if char == ".":
                assert "." not in currnum, "multiple decimals in one number"
            currnum += char
            continue 
        elif char in signs + operators + parentheticals:
            if currnum != "":
                currnode.insert(float(currnum))
                currnode = currnode.next
                currnum = ""



        if char in signs:
            currnode.insert(Sign(char))
            currnode = currnode.next

        elif char in operators:
            currnode.insert(Operator(char))
            currnode = currnode.next
        
        elif char in parentheticals:
            currnode.insert(char)
            currnode = currnode.next
    
    if currnum != "":
        currnode.insert(float(currnum))
    
    head.pop()
    return head.next

if __name__ == "__main__":
    print("ANSWER:" , calculate(input()))