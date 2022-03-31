import sys

import classes
import make_dict
import search_algorithms as search
import visibility as vis


def print_paths(paths):
  for path in paths:
    for vertex in path:
      if vertex != path[-1]:
        print(vertex.name, end=" ")
      else:
        print(f"{vertex.name}.")


def report(solution, paths, print_all, has_cust):
  print(f"Path found: ", end="")
  for vertex in solution:
    if vertex.__class__ == classes.Vertex:
      if vertex != solution[-1]:
        print(vertex.name, end=" ")
      else:
        print(f"{vertex.name}.")
  if has_cust:
    if solution[-1].__class__ == classes.Vertex:
      print(f"Distance: {solution[-1].distance}")
  if print_all:
    print_paths(paths)
  print()


def pos_solution(problem):
  for i in range(2):
    problem["start_end_vertices"][i].visible = []
    problem["start_end_vertices"][i].distance = 0
    problem["start_end_vertices"][i].visited = False
    problem["start_end_vertices"][i].parent = None
    problem["paths"] = []
  for v in problem["vertices"]:
    v.visible = []
    v.distance = 0
    v.visited = False
    v.parent = None
  return problem


def main():

  # Constrói o dicionário do problema.
  if len(sys.argv) < 2:
    print("""
      Usage: python main.py <filepath> [-a [all,bfs,ids,a_star,ida]] [-r]
      -a: search algorithm to use. Default is all.
      -r: print all paths.
      """)
    exit(1)
  else:
    filepath = sys.argv[1]
    algorithm = "all"
    print_all = False
    if len(sys.argv) > 2:
      if sys.argv[2] == "-a":
        algorithm = sys.argv[3]
      if sys.argv[2] == "-r" or sys.argv[4] == "-r":
        print_all = True
    problem = make_dict.make_dict(filepath)

    # Configura os polígonos não-convexos
    problem = vis.make_concavity(problem)

    # Algoritmos de busca

    if algorithm == "bfs":
      print("Best-First Search")
      bfs_path = search.bfs(problem)
      bfs_all_paths = problem["paths"]
      report(bfs_path, bfs_all_paths, print_all, True)
    elif algorithm == "ids":
      print("Iterative Deepening Search")
      ids_path = search.ids(problem)
      ids_all_paths = problem["paths"]
      report(ids_path, ids_all_paths, print_all, False)
    elif algorithm == "a_star":
      print("A*")
      a_star_path = search.a_star(problem)
      a_star_all_paths = problem["paths"]
      report(a_star_path, a_star_all_paths, print_all, False)
    elif algorithm == "ida":
      print("IDA*")
      ida_star_path = search.ida_star(problem)
      ida_star_all_paths = problem["paths"]
      report(ida_star_path, ida_star_all_paths, print_all, True)
    elif algorithm == "all":
      # BFS
      print("Best-First Search")
      bfs_path = search.bfs(problem)
      bfs_all_paths = problem["paths"]
      report(bfs_path, bfs_all_paths, print_all, True)
      problem = pos_solution(problem)
      # IDS
      print("Iterative Deepening Search")
      ids_path = search.ids(problem)
      ids_all_paths = problem["paths"]
      report(ids_path, ids_all_paths, print_all, False)
      problem = pos_solution(problem)
      # A*
      print("A*")
      a_star_path = search.a_star(problem)
      a_star_all_paths = problem["paths"]
      report(a_star_path, a_star_all_paths, print_all, False)
      # IDA*
      print("IDA*")
      ida_star_path = search.ida_star(problem)
      ida_star_all_paths = problem["paths"]
      report(ida_star_path, ida_star_all_paths, print_all, True)


main()
