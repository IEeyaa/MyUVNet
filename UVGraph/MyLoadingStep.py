from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.gp import gp_Pnt
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file


def create_arrow(display, base_point, normal_vector, scale=1.0):

    # Create base point
    vertex = BRepBuilderAPI_MakeVertex(gp_Pnt(*base_point)).Vertex()

    # Create arrow tip
    arrow_tip = base_point + normal_vector * scale
    arrow_tip_vertex = BRepBuilderAPI_MakeVertex(gp_Pnt(*arrow_tip)).Vertex()

    # Create arrow edge
    arrow_edge = BRepBuilderAPI_MakeEdge(vertex, arrow_tip_vertex).Edge()

    # Display arrow
    display.DisplayShape(arrow_edge, color="BLUE1")


def visualization(datas, shape):
    # Create a 3D display
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Display points and normals
    # for face in datas:
    #     for u_grid in face:
    #         for row in u_grid:
    #             point = row[:3]
    #             normal = row[3:6]
    #             create_arrow(display, point, normal, 1.0)

    display.DisplayShape(shape)
    # Start the display
    start_display()


if __name__ == '__main__':
    shp = read_step_file("1.step")
    visualization(None, shp)

