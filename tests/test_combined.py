from absp import VertexGroup, AdjacencyGraph, CellComplex
import numpy as np
import random
random.seed(100)


def example_combined():
    vertex_group = VertexGroup(filepath='./test_data/test_points.vg')
    planes, bounds, points = np.array(vertex_group.planes), np.array(vertex_group.bounds), np.array(
        vertex_group.points_grouped, dtype=object)

    cell_complex = CellComplex(planes, bounds, points, build_graph=True)
    cell_complex.refine_planes()
    cell_complex.prioritise_planes()
    cell_complex.construct()
    cell_complex.print_info()

    graph = AdjacencyGraph(cell_complex.graph)
    weights_list = [random.random() for _ in range(cell_complex.num_cells)]
    weights_dict = graph.to_dict(weights_list)

    graph.assign_weights_to_n_links(cell_complex.cells, attribute='area_overlap',
                                    factor=0.1, cache_interfaces=True)  # provided by the cell complex
    graph.assign_weights_to_st_links(weights_dict)  # provided by the neural network prediction
    _, _ = graph.cut()
    graph.save_surface_obj(filepath='../output/surface.obj', cells=cell_complex.cells)


if __name__ == '__main__':
    example_combined()
