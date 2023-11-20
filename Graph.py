# -*- coding:utf-8 -*-
# @Author: IEeya
from OCC.Core.STEPControl import STEPControl_Reader

# 读取STEP文件
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer

from EntityMap import EntityMapModel


def face_adjacency(solid_shape):
    face_adjacent_map = {}
    eMap = EntityMapModel(solid_shape)

    t = TopologyExplorer(solid_shape)
    # 遍历每个面
    for f in t.faces():
        face = eMap.get_face(f)
        face.uv_bounds()
        face_index = eMap.get_face(f).index_number
        face_adjacent_map[face_index] = []
        # 遍历面上的边
        for line_in_face in t.edges_from_face(f):
            # 遍历与边相邻的面
            for neighbor_f in t.faces_from_edge(line_in_face):
                # 避免重复
                if f != neighbor_f:
                    # 添加边连接代表两个面的点
                    face_neighbor_index = eMap.get_face(neighbor_f).index_number
                    face_adjacent_map[face_index].append(face_neighbor_index)

    return face_adjacent_map


if __name__ == '__main__':
    step_reader = STEPControl_Reader()
    shp = read_step_file("0-0-0-0-0-23.step")
    print(face_adjacency(shp))

