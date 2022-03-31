# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém as classes usadas no exercício.


class LineSeg:

  def __init__(self, v1, v2):
    self.v1 = v1
    self.v2 = v2


class Vertex:

  def __init__(self, name, x, y):
    self.name = name
    self.coord = Point(x, y)
    self.visible = []
    self.belongs_poly = None
    self.adjacent = []
    self.visited = False

  def __eq__(self, other):
    if other.__class__ == Point:
      return self.coord.x == other.x and self.coord.y == other.y
    elif other.__class__ == Vertex:
      return self.name == other.name
    else:
      return False

  def print(self):
    print(f"{self.name}: x={self.coord.x}, y={self.coord.y};")
    if self.visible:
      print(f"\tVisible:{self.visible}")
    if self.belongs_poly:
      print(f"\tBelongs to:{self.belongs_poly.name}\n")

  def belongs_to(self, polygon):
    self.belongs_poly = polygon

  def set_visited(self, value):
    self.visited = value

  def get_visited(self):
    return self.visited


class Polygon:

  def __init__(self, name, *vertices):
    self.name = name
    self.vertices = vertices
    self.concavity = False
    self.bay = []

  def print(self):
    print(f"{self.name}:", end="")
    for vert in self.vertices:
      print("\t", end="")
      vert.print()
    print("\n")


class Point:

  def __init__(self, x, y):
    self.x = float(x)
    self.y = float(y)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def print(self):
    print(f"x={self.x}, y={self.y};")
