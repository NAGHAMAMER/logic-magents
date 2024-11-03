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
        try:
            for metal in self.metals:
                new_map[metal.x][metal.y] = metal.type
        except Exception as e:
            print(f"Error: {e}")

        for home in self.homes:
            if 0 <= home[0] < self.size and 0 <= home[1] < self.size:  
                if new_map[home[0]][home[1]] == "empty":
                    new_map[home[0]][home[1]] = "home"
        self.new_map = new_map          
        for row in new_map:
            print(row)

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
          if movetype == "n":
              if self.new_map[newx][newy] in {"empty", "home"}:
                 self.move_negative(newx, newy)
          if movetype == "p":
              if self.new_map[newx][newy] in {"empty", "home"}:
                  self.move_positive(newx, newy)
       
          return self
          
    def check_game(self):
        for home in self.homes:
            if 0 <= home[0] < self.size and 0 <= home[1] < self.size:  
              if self.new_map[home[0]][home[1]]  not in {"negative", "positive"}:
                 return False
        return True 

class Node:
    def __init__(self, game_map):
        self.game_map = game_map
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class MainGame:
    def __init__(self):
        print("start")
    
               
    def create_game(self):   
        map_number = input("map number: ")   
        if map_number == "1":
            stones = [[3, 1, "negative"], [2, 3, "metal"]]
            homes = [[2, 2], [2, 4]]
            size=4
           
        elif map_number == "2":
            stones = [[5, 1, "negative"], [2, 3, "metal"], [3, 2, "metal"], [3, 4, "metal"], [4, 3, "metal"]]
            homes = [[1, 3], [3, 1], [3, 3], [3, 5], [5, 3]]
            size=5
        elif map_number == "3":
            stones = [[3, 1, "negative"], [2, 3, "metal"]]
            homes = [[1, 4], [3, 4]]
            size=4

        map = Map(size, stones, homes)
        map.set_map()
        self.play(map)
        
    def play(self, map):
     current_node = Node(map)
     newmap=map
     while True:
            stone_type = input("stone type: ")
            newx = int(input("move x: "))
            newy = int(input("move y: "))
            newmap = newmap.move(stone_type, newx, newy)
            current_node.add_child(Node(newmap))
        
            if newmap.check_game():
                    print("win")
                    break
            
        

game = MainGame()
game.create_game()
    
    
    
    
    
    
    
 
