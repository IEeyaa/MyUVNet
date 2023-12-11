# -*- coding:utf-8 -*-
# @Author: IEeya

# 产生实体内部所有元素的索引关系
from OCC.Extend.TopologyUtils import TopologyExplorer

from UVGraph.Edge import EdgeModel
from UVGraph.Face import FaceModel


def generate_hash_code(shape):
    return shape.__hash__()


class EntityMapModel:
    def __init__(self, solid):
        # 通过graph node 来排序


        # face hash值和index的映射关系
        self.face_map = dict()
        self.edge_map = dict()

        self.init_faces(solid)
        self.init_edges(solid)

    def append_face(self, face):
        self.face_map[generate_hash_code(face)] = FaceModel(face, len(self.face_map))


    def append_edge(self, edge):
        self.edge_map[generate_hash_code(edge)] = EdgeModel(edge, len(self.edge_map))


    def get_face(self, face):
        return self.face_map[generate_hash_code(face)]

    def get_edge(self, edge):
        return self.edge_map[generate_hash_code(edge)]

    def init_faces(self, solid):
        t = TopologyExplorer(solid)
        # 遍历每个面
        for f in t.faces():
            self.append_face(f)

    def init_edges(self, solid):
        t = TopologyExplorer(solid)
        # 遍历每个面
        for f in t.edges():
            self.append_edge(f)