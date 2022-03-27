import make_dict
import visibility
import search_algorithms as search


def main():

	# Constrói o dicionário do problema.
	problem = make_dict.main()

	# Configura os polígonos não-convexos
	visibility.make_concavity(problem)
	#print_bays(problem)
	

	# Algoritmos de busca
	bfs_path = search.bfs(problem)

	ids_path = search.ids(problem)

	a_star_path = search.a_star(problem)

	ida_star_path = search.ida_star(problem)

	return


def print_bays(problem):

	for polygon in problem["polygons"]:
		if polygon.concavity:
			print(f"\nPolygon {polygon.name} has a bay.")
			print("Bay:", end="")
			for vert in polygon.bay:
				print(vert.name, end=" ")
			print()

	return


if __name__ == "__main__":
	main()