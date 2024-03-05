class Node:
    
    def __init__(self, data) -> None:
        self.data = data
        self.next = None

class LinkedList:

    def __init__(self) -> None:
        self.head = None

    def insert_at_end(self, data):
        new_node = Node(data)

        if self.head == None:
            self.head = new_node
        else:
            last = self.head
            while(last.next != None):
                last = last.next

            last.next = new_node

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    
    def insert_after(self, previous_data, new_data):
        new_node = Node(new_data)

        if (self.head == None):
            print("Linked list is empty!")
        else:
             temp = self.head

             while(temp.data != previous_data):
                 if (temp.next == None):
                     print("Not found")
                     return
                 temp = temp.next

             new_node.next = temp.next
             temp.next = new_node

    
    def insert_before(self, next_data, new_data):
        new_node = Node(new_data)

        if (self.head == None):
            print("Linked list is empty!")
        else:
             temp = self.head

             while(temp.next.data != next_data):
                 if (temp.next.next == None):
                     print("Not found")
                     return
                 temp = temp.next

             new_node.next = temp.next
             temp.next = new_node

    def remove(self, desired_data):
        if (self.head == None):
            print("Linked list is empty!")
        elif self.head.data == desired_data:
            self.head = self.head.next
        else:
             temp = self.head

             while(temp.next != None and temp.next.data != desired_data):
                 temp = temp.next

             if temp.next == None:
                 print("Not found!")
             else:
                temp.next = temp.next.next