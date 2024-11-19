from collections import deque
import queue
from queue import PriorityQueue
import copy
import random

class Stone:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

class Map:
    def __init__(self, size, stones, homes):  
        self.size = size
        self.stones = stones
        self.homes = homes
        self.negative = None
        self.positive = None
        self.metals = []
        self.new_map = [[]]
        self.set_stones()

    def set_stones(self):
        for row in self.stones:
            if row[2] == "negative":
                self.negative = Stone(row[0], row[1], row[2])
            elif row[2] == "positive":
                self.positive = Stone(row[0], row[1], row[2])
            else:
                self.metals.append(Stone(row[0], row[1], row[2]))

    def set_map(self):
        new_map = [["empty" for _ in range(self.size)] for _ in range(self.size)]
        if self.negative:
            new_map[self.negative.x][self.negative.y] = self.negative.type
        if self.positive:
            new_map[self.positive.x][self.positive.y] = self.positive.type
        for metal in self.metals:
            new_map[metal.x][metal.y] = metal.type
        for home in self.homes:
            if 0 <= home[0] < self.size and 0 <= home[1] < self.size:  
                if new_map[home[0]][home[1]] == "empty":
                    new_map[home[0]][home[1]] = "home"
        self.new_map = new_map          
        for row in new_map:
            print(row)
        print("\n")
    def move_negative(self, newx, newy):
     self.negative.x = newx
     self.negative.y = newy
     if self.positive:  
          if self.positive.y==newy :
             if self.positive.x < newx: 
                 if self.positive.x + 1 < self.size:
                     self.positive.x += 1
             elif self.positive.x > newx: 
                 if self.positive.x - 1 >= 0:
                     self.positive.x -= 1
          if self.positive.x==newx :
             if self.positive.y < newy:  
                 if self.positive.y + 1 < self.size:
                     self.positive.y += 1
             elif self.positive.y > newy:  
                  if self.positive.y - 1 >= 0:
                     self.positive.y -= 1
     for metal in self.metals:
             if newy == metal.y:
                 if metal.x < newx and metal.x - 1 >= 0:  
                     metal.x -= 1      
                 if metal.x > newx and metal.x + 1 <self.size:  
                     metal.x += 1 
             if newx == metal.x:
                 if metal.y < newy and metal.y - 1 >=0:  
                     metal.y -= 1      
                 if metal.y > newy and metal.y + 1 <self.size:  
                     metal.y += 1 
     self.set_map()

    def move_positive(self, newx, newy):
    
      self.positive.x = newx
      self.positive.y = newy
      if self.negative:
         if self.negative.x not in {newx + 1, newx - 1} and self.negative.y not in {newy + 1, newy - 1}:
             if self.negative.y==newy :
                 if self.negative.x < newx:  
                         self.negative.x += 1
                 elif self.negative.x > newx:  
                         self.negative.x -= 1
             if self.negative.x==newx:
                 if self.negative.y < newy: 
                          self.negative.y += 1
                 elif self.negative.y > newy: 
                         self.negative.y -= 1

      for metal in self.metals:
          if metal.x not in {newx + 1, newx - 1} and metal.y not in {newy + 1, newy - 1}:
             if newy == metal.y:
                 if metal.x < newx:  
                     metal.x += 1      
                 if metal.x > newx:  
                     metal.x -= 1 
             if newx == metal.x:
                 if metal.y < newy:  
                     metal.y += 1      
                 if metal.y > newy:  
                     metal.y -= 1 
      self.set_map()


    def move(self, movetype, newx, newy):
        if 0 <= newx < self.size and 0 <= newy < self.size:
            if movetype == "n" and self.new_map[newx][newy] in {"empty", "home"}:
                self.move_negative(newx, newy)
            elif movetype == "p" and self.new_map[newx][newy] in {"empty", "home"}:
                self.move_positive(newx, newy)
        return self

    def check_game(self):
        for home in self.homes:
            if 0 <= home[0] < self.size and 0 <= home[1] < self.size:  
                if self.new_map[home[0]][home[1]] not in {"negative", "positive", "metal"}:
                    return False
        return True 

class Node:
    def __init__(self, game_map, parent_node=None,cost=0):
        self.game_map = game_map
        self.children = []
        self.parent = parent_node
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost
    def add_child(self, child_node):
        self.children.append(child_node)
        
class MainGame:
    def __init__(self):
        print("start")   

    def create_game(self):   
        map_number = input("map number: ")   
        if map_number == "1":
            stones = [[2, 0, "negative"], [1, 2, "metal"]]
            homes = [[1, 1], [1, 3]]
            size = 4
        elif map_number == "2":
            stones = [[4, 0, "negative"], [1, 2, "metal"], [2, 1, "metal"], [2, 3, "metal"], [3, 2, "metal"]]
            homes = [[0, 2], [2, 0], [2, 2], [2, 4], [4, 2]]
            size = 5
        elif map_number == "3":
            stones = [[2, 0, "negative"], [1, 2, "metal"]]
            homes = [[0, 3], [2, 3]]
            size = 4
        elif map_number == "4":
            stones = [[2, 0, "negative"], [1, 1, "metal"]]
            homes = [[1, 0], [1, 2]]
            size = 3
        elif map_number =="r":
            
            stones = [[random.randint(0, 2), random.randint(0, 2), random.choice(["negative", "positive"])],
                      [random.randint(0, 2),random.randint(0, 2), "metal"],
                      [random.randint(0, 2), random.randint(0, 2), "metal"],
                      [random.randint(0, 2), random.randint(0, 2), "metal"]]
            homes = [[random.randint(0, 2), random.randint(0, 2)], [random.randint(0, 2), random.randint(0, 2)]]
            size = 3    
       
       
        game_map = Map(size, stones, homes)
        game_map.set_map()
        who_play=input("who play:")
        if  who_play=="player":
          self.play(game_map)
        if  who_play=="bfs":
          self.solve_bfs(game_map) 
        if  who_play=="dfs":
          self.solve_dfs(game_map)   
        if  who_play=="ucs":
          self.solve_ucs(game_map)
          
    def play(self, map):
     current_node = Node(map,None)
     while True:
            stone_type = input("stone type: ")
            newx = int(input("move x: "))
            newy = int(input("move y: "))
            newmap = copy.deepcopy(current_node.game_map)
            newmap = newmap.move(stone_type, newx, newy)
            current_node.add_child(Node(newmap,current_node))
            current_node=current_node.children
            if newmap.check_game():
                    print("win")
                    break
                
                
    def stone_move_auto(self,current_node,type):
        children = []
        for i in range(current_node.game_map.size):
            for j in range(current_node.game_map.size):
                if current_node.game_map.new_map[i][j] == "empty" or current_node.game_map.new_map[i][j] == "home":
                    child_map = copy.deepcopy(current_node.game_map)
                    child_map = child_map.move(type, i, j)
                    child_node = Node(child_map, current_node)
                    current_node.add_child(child_node)
                    children.append(child_node)
        return children
     
    def solve_bfs(self, map):
        
      queue = deque()  
      visited = set()  
      childs=[]
      current_node = Node(map, None)
      queue.append(current_node)
      stone_type = input("stone type:")
      while queue:
          current_node = queue.popleft()  
          if current_node.game_map not in visited:
             if current_node.game_map.check_game():
                 path = self.get_parent_of_node(current_node)
                 for step in path:
                     print(step)
                 return
             childs=self.stone_move_auto(current_node, stone_type)
             for child_node in childs:
                 if child_node.game_map not in visited: 
                     queue.append(child_node)
             visited.add(current_node.game_map)       
      else:
         print("Solution not found") 
          
    def solve_dfs(self, map):
        stack = [] 
        visited = set()  
        childs=[]
        current_node = Node(map, None)
        stack.append(current_node)
        stone_type = input("stone type:")
        while stack:
            current_node = stack.pop() 
            if current_node.game_map not in visited:
                if current_node.game_map.check_game():
                     path = self.get_parent_of_node(current_node)
                     for step in path:
                          print(step)
                     return
                childs=self.stone_move_auto(current_node, stone_type)
                for child_node in childs:
                   if child_node.game_map not in visited: 
                      stack.append(child_node)  
                visited.add(current_node.game_map)      
        else:
               print("Solution not found")     

    def solve_ucs(self, map):
     pqueue = PriorityQueue()   
     visited = set()  
     childs = []
     current_node = Node(map, None)
     pqueue.put((current_node.cost, current_node))  
     stone_type = input("stone type:")
     while not pqueue.empty():  
         pr, current_node = pqueue.get()  
         if current_node.game_map not in visited:
             if current_node.game_map.check_game():
                 path = self.get_parent_of_node(current_node)
                 for step in path:
                     print(step)
                 print(f"Total cost: {pr}") 
                 return
             childs = self.stone_move_auto(current_node, stone_type)
             for child_node in childs:
                 if child_node.game_map not in visited:
                     cost = pr + 1  
                     pqueue.put((cost, child_node))  
             visited.add(current_node.game_map)  
     print("Solution not found")

 


  

  

    def get_parent_of_node(self, node):
     path = []
    
     while node:
         current_map = node.game_map
         move_description = ""
         if current_map.negative:
             if move_description:
                 move_description += " and "
             move_description += f" negative  ({current_map.negative.x}, {current_map.negative.y})"
        
      
         if current_map.positive:
             if move_description:
                  move_description += " and "
             move_description += f" positive  ({current_map.positive.x}, {current_map.positive.y})"
        
         if move_description:
             path.append(move_description)
         node = node.parent
     return path  [::-1]
  

game = MainGame()
game.create_game()
