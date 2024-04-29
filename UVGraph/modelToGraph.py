# -*- coding:utf-8 -*-
# @Author: IEeya
import json
import os
import sys

import time
import dgl
import numpy as np
import torch
from OCC.Extend.DataExchange import read_step_file

from UVGraph.EntityMap import EntityMapModel
from UVGraph.Graph import face_adjacency
from UVGraph.uv_grid import get_uvgrid_by_face, get_ugrid_by_edge

from dgl import save_graphs, load_graphs


# 将shp模型转换成uv_grid
def step_model_to_graph(graph_info, model_load_path, model_save_path, face_u_num=10, face_v_num=10, edge_u_num=10):

    model_name, label_name, label_index = graph_info
    model = read_step_file(model_load_path + "/" + label_name + "/STEP/" + model_name)

    # 建立索引Map
    eMap = EntityMapModel(model)

    graph_face_feat = []

    src_list, dst_list, edge_list = face_adjacency(model, eMap)
    # 遍历所有面: point, normal(法向量), mask(是否在面上)
    for face in eMap.face_map.values():
        uv_grid_point, uv_grid_normal, uv_grid_visibility, uv_grid_curve = get_uvgrid_by_face(face, face_u_num, face_v_num)
        mask = np.logical_or(uv_grid_visibility == 0, uv_grid_visibility == 2)  # 0: Inside, 1: Outside, 2: On boundary
        # Concatenate channel-wise to form face feature tensor
        face_feat = np.concatenate((uv_grid_point, uv_grid_normal, uv_grid_curve, mask), axis=-1)
        graph_face_feat.append(face_feat)
    graph_face_feat = np.asarray(graph_face_feat)
    graph_edge_feat = []
    # 遍历所有边: point, tangent(切向量)
    for edge in edge_list:
        u_grid_point, u_grid_tangent, u_grid_curve = get_ugrid_by_edge(edge, edge_u_num)
        edge_feat = np.concatenate((u_grid_point, u_grid_tangent, u_grid_curve), axis=-1)
        graph_edge_feat.append(edge_feat)
    graph_edge_feat = np.asarray(graph_edge_feat)


    # 储存信息
    dgl_graph = dgl.graph((src_list, dst_list), num_nodes=len(eMap.face_map))
    # 节点信息
    dgl_graph.ndata["x"] = torch.from_numpy(graph_face_feat)
    # 边信息
    dgl_graph.edata["x"] = torch.from_numpy(graph_edge_feat)

    save_to_dgl_file(dgl_graph, label_name, label_index, model_save_path)


# 保存文件到.bin中
def save_to_dgl_file(graph, graph_name, graph_index, graph_save_path):
    # 储存训练文件
    graph_path = os.path.join(graph_save_path, graph_name + "_" + str(graph_index) + '.bin')
    # 储存训练数据以及它们对应的label
    save_graphs(graph_path, [graph])


# 从.bin中加载文件
def load_from_dgl_file(graph_name, graph_save_path):
    graph_path = os.path.join(graph_save_path, graph_name)
    dgl_graph, _ = load_graphs(graph_path)
    return dgl_graph


def split_list(input_list, ratios):
    # 计算每个部分的长度
    total_length = len(input_list)
    lengths = [int(ratio * total_length) for ratio in ratios]

    # 使用切片分割列表
    parts = [input_list[sum(lengths[:i]):sum(lengths[:i + 1])] for i in range(len(lengths))]

    return parts


# 获取所有文件
def get_step_files_in_folders(parent_folder):
    """
       Get a list of STEP files in the specified parent folder and its subfolders.

       Args:
           parent_folder (str): The path to the parent folder.

       Returns:
           list: A list of tuples, where each tuple contains the file name and the label.
       """
    step_files = []
    split_file = {
        "train": [],
        "val": [],
        "test": [],
    }
    # 遍历每个子目录
    for root, dirs, files in os.walk(parent_folder):
        # 检查是否存在 "STEP" 文件夹
        if "STEP" in dirs:
            step_folder = os.path.join(root, "STEP")
            # 获取 "STEP" 文件夹中的所有文件
            temp_result = [(file, os.path.basename(root), index) for index, file in enumerate(os.listdir(step_folder))
                           if file.endswith(".stp")]
            if len(temp_result) > 0:
                step_files.extend(temp_result)
                temp_result = [item[1] + "_" + str(item[2]) for item in temp_result]
                split_result = split_list(temp_result, [0.5, 0.3, 0.2])
                split_file["train"].extend(split_result[0])
                split_file["val"].extend(split_result[1])
                split_file["test"].extend(split_result[2])

    return step_files, split_file


def build_from_graph(parent_folder, split_save_path, bin_save_path):
    all_files, split_file = get_step_files_in_folders(parent_folder)
    file_len = len(all_files)

    directory = bin_save_path
    files_in_directory = os.listdir(directory)

    for index, item in enumerate(all_files):
        file_name = item[1] + "_" + str(item[2]) + ".bin"
        if file_name in files_in_directory:
            continue
        step_model_to_graph(item, parent_folder, bin_save_path, 10, 10, 10)
        print("\r", end="")
        i = int(index / file_len * 100)
        print("Graph Encoder progress: {}%: ".format(i), "▋" * (i // 2), end="")
        print("Loading Info: {}\{}".format(index, file_len), end="")
        sys.stdout.flush()
        time.sleep(0.05)

    with open(split_save_path, "w") as json_file:
        json.dump(split_file, json_file, indent=4)


if __name__ == '__main__':
    print(1)

