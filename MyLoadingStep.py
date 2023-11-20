from OCC.Core.STEPControl import STEPControl_Reader
import networkx as nx

# 读取STEP文件
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer

step_reader = STEPControl_Reader()
shp = read_step_file("0-0-0-0-0-23.step")
face_face_graph = nx.Graph()

t = TopologyExplorer(shp)

# 建立面到顺序编号的映射
face_to_number = {}
counter = 1

# 遍历每个面
for f in t.faces():
    face_to_number[f] = counter
    counter += 1  # Increment counter here

# Reset counter for the next loop
counter = 1

# 遍历每个面
for f in t.faces():
    face_face_graph.add_node(face_to_number[f])

    # 遍历面上的边
    for line_in_face in t.edges_from_face(f):
        # 遍历与边相邻的面
        for neighbor_f in t.faces_from_edge(line_in_face):
            # 避免重复
            if f != neighbor_f:
                # 添加边连接代表两个面的点
                face_face_graph.add_edge(face_to_number[f], face_to_number[neighbor_f])

# 构建面之间的编号关系
face_number_relations = {}
for node, face_number in enumerate(face_face_graph.nodes, start=1):
    neighbors = list(face_face_graph.neighbors(node))
    face_number_relations[face_number] = neighbors

print(face_number_relations)
