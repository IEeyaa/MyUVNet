# -*- coding:utf-8 -*-
# @Author: IEeya
from OCC.Core.STEPControl import STEPControl_Reader

# 读取STEP文件
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer


def face_adjacency(solid_shape, eMap):
    t = TopologyExplorer(solid_shape)
    src_list = []
    dst_list = []
    line_list = []
    # 遍历每个面
    for f in t.faces():
        face_index = eMap.get_face(f).index_number
        # 遍历面上的边
        for line_in_face in t.edges_from_face(f):
            # 遍历与边相邻的面
            for neighbor_f in t.faces_from_edge(line_in_face):
                # 避免重复
                if f != neighbor_f:
                    # 添加边连接代表两个面的点
                    face_neighbor_index = eMap.get_face(neighbor_f).index_number
                    line_info = eMap.get_edge(line_in_face)
                    # 连接的两个面序号
                    src_list.append(face_index)
                    dst_list.append(face_neighbor_index)
                    # 对应的边序号
                    line_list.append(line_info)
    return src_list, dst_list, line_list


if __name__ == '__main__':
    step_reader = STEPControl_Reader()
    shp = read_step_file("RawFiles/0acde690-095f-4bc7-bffa-94c61e1528cc.stp")
    print(face_adjacency(shp))

