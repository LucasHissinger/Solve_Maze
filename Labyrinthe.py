import random
import math
import pygame
import time

class Labyrinthe:

    def __init__(self, size):
        self.size = size

    def create_labyrinthe(self):
        self.create_grille()
        self.couleur()
        self.join_color()
        self.breakwall()
        for i in range(self.size):
            for j in range(self.size):
                if self.labyrinthe[i][j] != -1 and self.labyrinthe[i][j] != -2:
                    self.labyrinthe[i][j] = -6
        self.distance()
        #self.solve()

    def create_grille(self):
        self.labyrinthe = [[0 for i in range(self.size)] for i in range(self.size)]
        self.create_wall()
        self.create_line()
        self.labyrinthe[1][0] = 0
        self.labyrinthe[self.size-2][self.size-1] = 0

    def create_wall(self):
        for i in range(self.size): #ligne
          for j in range(math.ceil(self.size/2)): #colonne
            self.labyrinthe[i][j*2] = -1

    def create_line(self):
        for i in range(math.ceil(self.size/2)):
          for j in range(self.size):
            self.labyrinthe[i*2][j] = -2

    def couleur(self):
        nb = 0
        for i in range(self.size):
          for j in range(self.size):
            if self.labyrinthe[i][j] == 0:
              nb += 1
              self.labyrinthe[i][j] = nb

    def is_finished(self):
        for i in range(1, self.size-1, 2):
          for j in range(1, self.size-1, 2):
            if self.labyrinthe[i][j] != self.labyrinthe[1][1]:
              return False
        return True

    def join_color(self):
        while not self.is_finished():
          x = random.randint(1, self.size-2)
          if x % 2 == 0:
            y = random.randrange(1, self.size-1, 2)
          else:
            y = random.randrange(2, self.size-2, 2)
          if self.labyrinthe[x][y] == -1: #Récupère les couleurs des 2 cases
            color1 = self.labyrinthe[x][y-1]
            color2 = self.labyrinthe[x][y+1]
          else:
            color1 = self.labyrinthe[x-1][y]
            color2 = self.labyrinthe[x+1][y]

          if color1 != color2:
            self.labyrinthe[x][y] = color1

            for i in range(self.size):
              for j in range(self.size):
                if self.labyrinthe[i][j] == color2:
                  self.labyrinthe[i][j] = color1

    def breakwall(self):
        mur = int(self.size/5)
        nb = 0
        while nb < mur:
            x = random.randint(1, self.size-2)
            y = random.randint(1, self.size-2)
            if self.labyrinthe[x][y] == -1 or self.labyrinthe[x][y] == -2:
                self.labyrinthe[x][y] = -3
                nb += 1

    def distance(self):
      for i in range(self.size):
        for j in range(self.size):
          self.labyrinthe[i][j] = [self.labyrinthe[i][j], 0]
      self.labyrinthe[self.size-2][self.size-1] = [1, 0]
      self.labyrinthe[self.size-2][self.size-2] = [7, 1]
      while self.labyrinthe[1][0][0] == -6:
        for i in range(self.size):
          for j in range(self.size):
            if self.labyrinthe[i][j][0] == 7:
              self.labyrinthe[i][j][0] = self.labyrinthe[i][j][1] + 1
              for x, y in zip([i, i+1, i, i-1], [j+1, j, j-1, j]):
                if self.labyrinthe[x][y][0] == -6:
                  self.labyrinthe[x][y] = [7, self.labyrinthe[i][j][0]]

    def solve(self):
      self.labyrinthe[1][0][1] = -10
      self.labyrinthe[1][1][1] = -10
      i, j = 1, 1
      while self.labyrinthe[self.size-2][self.size-1][0] == 1:
        update()
        list_distance = []
        list_positif = []
        for x, y in zip([i, i+1, i, i-1], [j+1, j, j-1, j]):

          list_distance.append(self.labyrinthe[x][y][0])
          if self.labyrinthe[x][y][0] > 0:
            list_positif.append(self.labyrinthe[x][y][0])
        coordonnées = [[i, i+1, i, i-1][list_distance.index(min(list_positif))], [j+1, j, j-1, j][list_distance.index(min(list_positif))]]
        i, j = coordonnées[0], coordonnées[1]
        self.labyrinthe[i][j][0] = -10
        time.sleep(0.01)
        pygame.display.flip()

Maze_size = int(input("Entrez la taille du Labyrinthe "))
if (Maze_size % 2 == 0):
    Maze_size = Maze_size + 1
print("Loading..")
Maze = Labyrinthe(Maze_size)
Maze.create_labyrinthe()
print("Complete !")

pygame.init()

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
size = width, height = 1000, 800

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
running = True

def update():
  for i in range(Maze.size):
    for j in range(Maze.size):
      if Maze.labyrinthe[i][j][0] == -1 or Maze.labyrinthe[i][j][0] == -2:
          pygame.draw.rect(screen, (0, 0, 0), (10+int(800/Maze_size)*j, 10+int(800/Maze_size)*i, int(800/Maze_size), int(800/Maze_size)))
      elif Maze.labyrinthe[i][j][0] == -10:
          pygame.draw.rect(screen, (238,130,238), (10+int(800/Maze_size)*j, 10+int(800/Maze_size)*i, int(800/Maze_size), int(800/Maze_size)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))


    Maze.solve()
    update()


    time.sleep(0.005)
    pygame.display.flip()
