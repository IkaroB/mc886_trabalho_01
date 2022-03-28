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

	def print(self):
		print(f"{self.name}: x={self.coord.x}, y={self.coord.y};")
		if self.visible:
			print(f"\tVisible:{self.visible}")
		if self.belongs_poly:
			print(f"\tBelongs to:{self.belongs_poly.name}\n")

	def belongs_to(self, polygon):
		self.belongs_poly = polygon


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

	def print(self):
		print(f"x={self.x}, y={self.y};")