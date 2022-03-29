import make_dict
import search_algorithms as search
import visibility as vis


def main():

  # Constrói o dicionário do problema.
  problem = make_dict.main()

  # Configura os polígonos não-convexos
  vis.make_concavity(problem)

  # Debugging

  # vis.print_bays(problem)

  # start_vert = problem["start_end_vertices"][0]
  # debug_vert_visibility(problem, start_vert)

  # print(problem["vertices"][7].name)
  vert = problem["vertices"][4]
  debug_vert_visibility(problem, vert)

  # Algoritmos de busca
  bfs_path = search.bfs(problem)

  ids_path = search.ids(problem)

  a_star_path = search.a_star(problem)

  ida_star_path = search.ida_star(problem)

  return


def debug_vert_visibility(problem, vert):
  vis.expand_vert(problem, vert)
  vis.vert_visibility(vert)


if __name__ == "__main__":
  main()
