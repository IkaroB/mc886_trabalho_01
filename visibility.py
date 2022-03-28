# Exercício 1 de MO416A/MC886B 1s2022

# Este módulo python contém os algoritmos necessários para
# a expansão dos vértices, que consiste em descobrir quais
# outros vértices são visíveis para o vértice atual.

import make_dict
import classes
import numpy as np


# Registra no vértice atual (curr_vert) todos os outros
# vértices visíveis a partir dele.
def expand_vert(problem, curr_vert):

	visible = []

	for polygon in problem["polygons"]:

		# Checa o caso em que o polígono contém curr_vert.
		if (curr_vert.belongs_poly == polygon):
			visible_in_poly = get_visible_in_poly(curr_vert)
			for vis_vert in visible_in_poly:
				if (vis_vert not in problem["explored"]):
					visible.append(vis_vert)
					problem["explored"].append(vis_vert)
		
		# Outros polígonos.
		else:
			for poly_vert in polygon.vertices:
				possible_line = classes.LineSeg(curr_vert, poly_vert)
				if (is_visible(possible_line, problem)):
					if (poly_vert not in problem["explored"]):
						visible.append(poly_vert)
						problem["explored"].append(poly_vert)

	# Checa o caso em que o destino é visível
	goal = problem["start_end_vertices"][1]
	possible_line = classes.LineSeg(curr_vert, poly_vert)
	if (is_visible(possible_line, problem)):
		if (poly_vert not in problem["explored"]):
			visible.append(poly_vert)
			problem["explored"].append(poly_vert)

	curr_vert.visible = visible


# Retorna True se o segmento de reta não cruza nenhum polígono
# e False se há cruzamento.
def is_visible(possible_line, problem):
	
	for polygon in problem["polygons"]:
		if(do_cross_poly(possible_line, polygon)):
			return False
	
	return True


# Checa a concavidade dos polígonos e altera os atributos "bay"
# e "concavity" nos polígonos que possuem concavidade.
def make_concavity(problem):

	for polygon in problem["polygons"]:
		poly_concavity(polygon)

	return


# Como, na definição do problema, os vértices foram declarados
# no sentido anti-horário, quando a orientação de 3 pontos
# consecutivos for no sentido horário, eles fazem parte da baía.
# A função constrói o vetor "bay" e define o valor do parâmetro 
# "concavity" como True no polígono de entrada, se ele possuir
# alguma concavidade.
def poly_concavity(polygon):

	no_vert = len(polygon.vertices) - 1
	if (no_vert > 3):
		for i in range(no_vert):
			v1 = polygon.vertices[i]
			v2 = polygon.vertices[(i+1)%no_vert]
			v3 = polygon.vertices[(i+2)%no_vert]
			p1 = v1.coord
			p2 = v2.coord
			p3 = v3.coord

			#print(f"\nPolygon: {polygon.name}, vertices: {v1.name}, {v2.name}, {v3.name};")
			#print("\tx:" + p1.x,p2.x,p3.x)
			#print("\ty:" + p1.y,p2.y,p3.y)
			
			# Constrói a baía e modifica o parâmetro de
			# concavidade.
			if (orientation(p1, p2, p3) == -1):
				polygon.concavity = True
				for a in range(3):
					bay_vert = polygon.vertices[(i+a)%no_vert]
					if (bay_vert not in polygon.bay):
						polygon.bay.append(bay_vert)

	return


# Calcula se os três pontos ordenados são orientados no sentido
# horário (negativo), anti-horário (positivo) ou são colineares
# (zero).
def orientation(p1, p2, p3):

	m = [[float(p1.x), float(p2.x), float(p3.x)],
		 [float(p1.y), float(p2.y), float(p3.y)],
		 [1.0, 1.0, 1.0]]
	det = np.linalg.det(m)
	#print("\tdet:", det)

	# O determinante do numpy nem sempre retorna zero quando
	# há colinearidade.
	if (abs(det) < 0.000001):
		orientation = 0
	elif (det < 0):
		orientation = -1
	elif (det > 0):
		orientation = 1

	#print("\torientation:", orientation)

	return orientation


# Retorna todos os vértices visíveis para "vert" que estão
# no mesmo polígono que ele.
def get_visible_in_poly(vert):

	visible = []
	polygon = vert.belongs_poly

	# Checa se o polígono que contém "vert" tem concavidade.
	# Se "vert" estiver na baía, todos pertencentes a ela são
	# visíveis. Caso contrário, somente os adjacentes a "vert".
	if (polygon.concavity and vert in polygon.bay):
		visible = polygon.bay
	else:
		visible = get_adjacent(vert)

	return visible


def get_adjacent(vert):

	adjacent = vert.adjacent

	if not adjacent:
		polygon = vert.belongs_poly
		no_vert = len(polygon.vertices) - 1

		for i in range(no_vert):
			if (vert == polygon.vertices[i]):
				index_1 = (i-1) % no_vert
				index_2 = (i+1) % no_vert
				adjacent.append(polygon.vertices[index_1])
				adjacent.append(polygon.vertices[index_2])
				print("Adjacent:", polygon.vertices[index_1].name, polygon.vertices[index_2].name)
				break
	
	return adjacent


# Entrada: dois segmentos de reta, que são formados por dois
# vértices cada.
# A função retorna True se os segmentos se cruzam, e False
# caso contrário.
# Se os segmentos se cruzam em um ponto apenas, considera-se
# que não se cruzam, já que os vértices se enxergam.
# Nos casos de colinearidade, também considera-se que não
# se cruzam, pelo mesmo motivo.
def do_cross_seg(line_seg_1, line_seg_2):

	p1 = line_seg_1.v1.coord
	p2 = line_seg_1.v2.coord

	p3 = line_seg_2.v1.coord
	orientation_1 = orientation(p1, p2, p3)

	p3 = line_seg_2.v2.coord
	orientation_2 = orientation(p1, p2, p3)

	if (orientation_1 == 0):
		return line_seg_2.v1

	elif(orientation_2 == 0):
		return line_seg_2.v2

	elif (orientation_1 == orientation_2):
		return "No"

	else:
		return "Yes"


# Checa se um segmento de reta cruza alguma das arestas
# de um polígono.
def do_cross_poly(line_seg, polygon):

	collinear = []

	for i in range(len(polygon.vertices) - 1):
		v1 = polygon.vertices[i]
		v2 = polygon.vertices[i+1]

		if (line_seg.v1 == v1 or line_seg.v1 == v2):
			continue
		elif (line_seg.v2 == v1 or line_seg.v2 == v2):
			continue

		edge = classes.LineSeg(v1, v2)

		cross_seg_1 = do_cross_seg(line_seg, edge)
		cross_seg_2 = do_cross_seg(edge, line_seg)

		# Debugging print
		#print(f"{line_seg.v1.name}-{line_seg.v2.name} cross {v1.name}-{v2.name}? 1:{cross_seg_1}, 2:{cross_seg_2}")

		if (cross_seg_1 == cross_seg_2 == "Yes"):
			return True
		elif(cross_seg_1 == "No" or cross_seg_2 == "No"):
			continue


		# TODO Verificar o problema com os vértices:
		# e, h, i, t, u.

		# Pelo menos um dos vértices da aresta em questão
		# está contido no segmento de reta.
		else:
			# Se for adjacente ao vértice de destino (que está
			# em um polígono diferente do vértice de partida),
			# então o vértice em cross_seg_1 é visível.
			# Se for adjacente ao vértice de partida, também.
			not_added = cross_seg_1 not in collinear
			start_adjacent = get_adjacent(line_seg.v1)
			dest_adjacent = get_adjacent(line_seg.v2)
			if(cross_seg_1 in dest_adjacent or cross_seg_1 in start_adjacent):
				continue
			elif (not_added):
				collinear.append(cross_seg_1)

	for vert in collinear:

		# TODO: Funciona para O entre IQ, mas não para
		# 		I e H entre ET e EU

		# Se o comprimento de line_seg for maior que a 
		# distância de seus dois vértices a algum dos
		# vértices colineares selecionados, então o 
		# segmento cruza algum polígono.
		aux_seg_1 = classes.LineSeg(line_seg.v1, vert)
		aux_seg_2 = classes.LineSeg(line_seg.v2, vert)
		seg_length = line_length(line_seg)
		comp_1 = seg_length > line_length(aux_seg_1)
		comp_2 = seg_length > line_length(aux_seg_2)
		if (comp_1 and comp_2):
			return True
	
	return False


# Retorna o tamanho de um segmento de reta.
def line_length(line_seg):

	x_diff = line_seg.v1.coord.x - line_seg.v2.coord.x
	y_diff = line_seg.v1.coord.y - line_seg.v2.coord.y

	length = (x_diff**2 + y_diff**2)**0.5

	return length


# Printa todos os vértices visíveis a partir de "vert"
def vert_visibility(vert):

	if vert.visible:
		print(f"Vertex {vert.name} sees: ", end="")
		for vert in vert.visible:
			print(f"{vert.name}", end=" ")
	else:
		print(f"Vertex {vert.name} not expanded.", end="")
	print("\n")


# Revela todas as concavidades do problema.
def print_bays(problem):

	for polygon in problem["polygons"]:
		if polygon.concavity:
			print(f"\nPolygon {polygon.name} has a bay.")
			print("Bay:", end="")
			for vert in polygon.bay:
				print(vert.name, end=" ")
			print("\n")

	return



def main():
	return

if __name__ == "__main__":
	main()