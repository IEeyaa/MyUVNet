# -*- coding:utf-8 -*-
# @Author: IEeya
import numpy as np

from UVGraph.Edge import u_grid_samples
from UVGraph.Face import uv_grid_samples


def get_uvgrid_by_face(face, num_u=10, num_v=10):
    uv_bound = face.uv_bounds()
    # 获取参数列表
    sample_params = uv_grid_samples(uv_bound, num_u, num_v)
    # 初始化结果矩阵
    point_result_matrix = []
    normal_result_matrix = []

    curve_result_matrix = []

    visibility_result_matrix = []

    # 遍历 param_matrix 中的每个元素，代入到 uv_grid_point 函数中
    for uv_sample in sample_params:
        point_result_matrix.append(face.uv_grid_point(uv_sample))
        normal_result_matrix.append(face.uv_grid_normal(uv_sample))
        curve_result_matrix.append(face.uv_grid_curvature(uv_sample))
        visibility_result_matrix.append(face.uv_grid_visibility(uv_sample))
    # 将结果矩阵转换为 NumPy 数组
    point_result_matrix = np.array(point_result_matrix).reshape(-1, num_u, 3)
    normal_result_matrix = np.array(normal_result_matrix).reshape(-1, num_u, 3)
    visibility_result_matrix = np.array(visibility_result_matrix).reshape(-1, num_u, 1)
    curve_result_matrix = np.array(curve_result_matrix).reshape(-1, num_u, 2)
    return point_result_matrix, normal_result_matrix, visibility_result_matrix, curve_result_matrix


def get_ugrid_by_edge(edge, num_u=10):
    u_bound = edge.u_bounds()
    # 获取参数列表
    sample_params = u_grid_samples(u_bound, num_u)
    # 初始化结果矩阵
    point_result_matrix = []
    tangent_result_matrix = []
    curve_result_matrix = []

    # 遍历 param_matrix 中的每个元素，代入到 uv_grid_point 函数中
    for u_sample in sample_params:
        point_result_matrix.append(edge.u_grid_point(u_sample))
        tangent_result_matrix.append(edge.u_grid_tangent(u_sample))
        curve_result_matrix.append([edge.u_grid_curvature(u_sample)])


    return point_result_matrix, tangent_result_matrix, curve_result_matrix

