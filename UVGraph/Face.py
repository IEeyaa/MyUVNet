# -*- coding:utf-8 -*-
# @Author: IEeya

import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepTools import breptools
from OCC.Core.BRepTopAdaptor import BRepTopAdaptor_FClass2d
from OCC.Core.GeomAbs import *
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.TopAbs import TopAbs_Orientation
from OCC.Core.gp import gp_Pnt, gp_Pnt2d


def uv_grid_samples(uv_bound, u_number=10, v_number=10):
    """
    Generate a grid of UV samples within the specified UV bounds.

    Args:
        uv_bound (tuple): Tuple containing (u_min, u_max, v_min, v_max).
        u_number (int): Number of samples in the U direction.
        v_number (int): Number of samples in the V direction.

    Returns:
        np.array: 3D array of UV sample points.
    """
    u_min, u_max, v_min, v_max = uv_bound

    # 这里打个标记
    u_params = np.linspace(u_max, u_min, u_number)
    v_params = np.linspace(v_min, v_max, v_number)

    # 这里再打个标记
    u_matrix, v_matrix = np.meshgrid(u_params, v_params, indexing="ij")

    # Combine u_matrix and v_matrix into a 2D array
    param_matrix = np.vstack((u_matrix.flatten(), v_matrix.flatten())).T

    return param_matrix


class FaceModel:
    def __init__(self, topods_face, index_number):
        """
        Initialize a FaceModel instance.

        Args:
            topods_face: TopoDS_Face instance representing the face geometry.
            index_number (int): Index number associated with the face.
        """
        self.topods_face = topods_face
        self.index_number = index_number
        self.isReserved = self.topods_face.Orientation() != TopAbs_Orientation.TopAbs_REVERSED

    def uv_bounds(self):
        """
        Get the UV bounds of the face.

        Returns:
            tuple: Tuple containing (u_min, u_max, v_min, v_max).
        """
        u_min, u_max, v_min, v_max = breptools.UVBounds(self.topods_face)
        return u_min, u_max, v_min, v_max

    def uv_grid_point(self, uv_sample):
        """
        Get the actual XYZ coordinates of a point on the face based on UV coordinates.

        Args:
            uv_sample (tuple): Tuple containing (u_pos, v_pos).

        Returns:
            np.array: NumPy array containing [X, Y, Z] coordinates of the point.
        """
        u_pos, v_pos = uv_sample
        surface = BRep_Tool.Surface(self.topods_face)
        point = gp_Pnt()
        surface.D0(u_pos, v_pos, point)
        return np.array([point.X(), point.Y(), point.Z()])

    def uv_grid_normal(self, uv_sample):
        """
        Get the normal vector of a point on the face based on UV coordinates.

        Args:
            uv_sample (tuple): Tuple containing (u_pos, v_pos).

        Returns:
            np.array: NumPy array containing [X, Y, Z] components of the normal vector.
        """
        u_pos, v_pos = uv_sample
        surface = BRep_Tool.Surface(self.topods_face)
        props = GeomLProp_SLProps(surface, u_pos, v_pos, 1, 1e-9)
        normal_vec = props.Normal()
        # 没有反
        if not self.isReserved:
            return np.array([-normal_vec.X(), -normal_vec.Y(), -normal_vec.Z()])

        return np.array([normal_vec.X(), normal_vec.Y(), normal_vec.Z()])

    def uv_grid_visibility(self, uv_sample):
        """
        Check if the uv-coordinate in on the visible region of the face

        Args:
            uv_sample (np.ndarray or tuple): Surface parameter

        Returns:
            int (TopAbs_STATE enum): 0: TopAbs_IN, 1: TopAbs_OUT, 2: TopAbs_ON, 3: TopAbs_UNKNOWN
        """
        u_pos, v_pos = uv_sample
        result = BRepTopAdaptor_FClass2d(self.topods_face, 1e-9).Perform(gp_Pnt2d(u_pos, v_pos))
        return int(result)


    def surface_type(self):
        """
        Get the type of the surface geometry.

        Returns:
            str: Type of the surface geometry.
        """
        surf_type = BRepAdaptor_Surface(self.topods_face()).GetType()
        if surf_type == GeomAbs_Plane:
            return "plane"
        if surf_type == GeomAbs_Cylinder:
            return "cylinder"
        if surf_type == GeomAbs_Cone:
            return "cone"
        if surf_type == GeomAbs_Sphere:
            return "sphere"
        if surf_type == GeomAbs_Torus:
            return "torus"
        if surf_type == GeomAbs_BezierSurface:
            return "bezier"
        if surf_type == GeomAbs_BSplineSurface:
            return "bspline"
        if surf_type == GeomAbs_SurfaceOfRevolution:
            return "revolution"
        if surf_type == GeomAbs_SurfaceOfExtrusion:
            return "extrusion"
        if surf_type == GeomAbs_OffsetSurface:
            return "offset"
        if surf_type == GeomAbs_OtherSurface:
            return "other"
        return "unknown"
