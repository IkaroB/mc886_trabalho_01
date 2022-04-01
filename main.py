import make_dict
import search_algorithms as search
import visibility as vis


def pos_solution(problem):
  for i in range(2):
    problem["start_end_vertices"][i].visible = []
    problem["start_end_vertices"][i].distance = 0
    problem["start_end_vertices"][i].visited = False
    problem["start_end_vertices"][i].parent = None
  for v in problem["vertices"]:
    v.visible = []
    v.distance = 0
    v.visited = False
    v.parent = None
  return problem


def main():

  # Constrói o dicionário do problema.
  problem = make_dict.make_dict()

  # Configura os polígonos não-convexos
  problem = vis.make_concavity(problem)

  # Algoritmos de busca

  #bfs_path = search.bfs(problem)
  #for i in bfs_path:
  #  print(i)
  #print(bfs_path)

  # Clear vertices
  problem = pos_solution(problem)

  #ids_path = search.ids(problem)
  #print(ids_path)
  #for i in ids_path:
  #  print(i)
  #print(problem["paths"])

  #problem = pos_solution(problem)

  #a_star_path = search.a_star(problem)
  # print(a_star_path)

  ida_star_path = search.ida_star(problem)

  # Debugging

  # vis.print_bays(problem)

  # start_vert = problem["start_end_vertices"][0]
  # debug_vert_visibility(problem, start_vert)

  # print(problem["vertices"][7].name)
  # vert = problem["vertices"][15]
  # vert = problem["vertices"][4]
  # vert = problem["vertices"][8]
  # vert = problem["vertices"][20]
  # vert = problem["vertices"][7]

  # for i in range(22):
  #   if i == 5 or i == 14:
  #     print(problem["vertices"][i].name,
  #           problem["vertices"][i].belongs_poly.name)
  #     print('')
  #     continue
  #   else:
  #     vis.debug_vert_visibility(problem, problem["vertices"][i])

  # vis.debug_vert_visibility(problem, problem["start_end_vertices"][0])

  return


if __name__ == "__main__":
  main()
