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
  # vert = problem["vertices"][15]
  # vert = problem["vertices"][4]
  # vert = problem["vertices"][8]
  # vert = problem["vertices"][20]
  # vert = problem["vertices"][7]
  for i in range(22):
    if i == 5 or i == 14:
      print(problem["vertices"][i].name, problem["vertices"][i].belongs_poly.name)
      print('')
      continue
    else:
      vis.debug_vert_visibility(problem, problem["vertices"][i])

  vis.debug_vert_visibility(problem, problem["start_end_vertices"][0])


  
  # Algoritmos de busca
  bfs_path = search.bfs(problem)

  ids_path = search.ids(problem)

  a_star_path = search.a_star(problem)

  ida_star_path = search.ida_star(problem)

  return



if __name__ == "__main__":
  main()
