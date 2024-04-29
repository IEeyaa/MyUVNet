# -*- coding:utf-8 -*-
# @Author: IEeya

import numpy as np
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import *
from OCC.Core.TopAbs import TopAbs_Orientation
from OCC.Core.gp import gp_Pnt, gp_Vec


def u_grid_samples(u_bound, u_number=10):
    """
    Generate a grid of U samples within the specified U bounds.

    Args:
        u_bound (tuple): Tuple containing (u_min, u_max).
        u_number (int): Number of samples in the U direction.

    Returns:
        np.array: 3D array of U sample points.
    """

    u_min, u_max = u_bound

    # 这里打个标记
    u_params = np.linspace(u_min, u_max, u_number)
    u_params = u_params.T
    return np.array(u_params)


class EdgeModel:
    def __init__(self, topods_edge, index_number):
        """
        Initialize a FaceModel instance.

        Args:
            topods_edge: TopoDS_Edge instance representing the edge geometry.
            index_number (int): Index number associated with the edge.
        """
        self.topods_edge = topods_edge
        self.index_number = index_number
        self.isReserved = self.topods_edge.Orientation() != TopAbs_Orientation.TopAbs_REVERSED

    def u_bounds(self):
        """
        Get the U bounds of the face.

        Returns:
            tuple: Tuple containing (u_min, u_max).
        """
        _, u_min, u_max = BRep_Tool.Curve(self.topods_edge)
        if self.isReserved:
            return u_min, u_max
        return u_max, u_min

    def u_grid_point(self, u_sample):
        """
        Get the actual XYZ coordinates of a point on the face based on U coordinates.

        Args:
            u_sample (float): Float containing u_pos.

        Returns:
            np.array: NumPy array containing [X, Y, Z] coordinates of the point.
        """
        u_pos = u_sample
        curve = BRep_Tool.Curve(self.topods_edge)[0]

        point = gp_Pnt()
        curve.D0(u_pos, point)
        return np.array([point.X(), point.Y(), point.Z()])

    def u_grid_tangent(self, u_sample):
        """
        Get the normal vector of a point on the face based on UV coordinates.

        Args:
            u_sample (float): Float containing u_pos.

        Returns:
            np.array: NumPy array containing [X, Y, Z] components of the tangent vector.
        """
        u_pos = u_sample
        curve = BRep_Tool.Curve(self.topods_edge)[0]

        point = gp_Pnt()
        tangent = gp_Vec()

        curve.D1(u_pos, point, tangent)

        tangent.Normalize()

        if self.isReserved:
            return np.array([tangent.X(), tangent.Y(), tangent.Z()])

        return np.array([-tangent.X(), -tangent.Y(), -tangent.Z()])


    def u_grid_curvature(self, u_sample):
        """
        Get the curvature of a point on the curve based on its parameter.

        Args:
            u_sample (float): Float containing u_pos.

        Returns:
            float: Curvature at the specified parameter.
        """
        u_pos = u_sample
        curve = BRep_Tool.Curve(self.topods_edge)[0]

        point = gp_Pnt()
        tangent = gp_Vec()
        curvature = gp_Vec()  # Initialize curvature

        curve.D2(u_pos, point, tangent, curvature)

        return curvature.Magnitude()

    def specific_curve(self):
        """
        Get the specific edge curve geometry

        Returns:
            OCC.Geom.Handle_Geom_*: Specific geometry type for the curve geometry
                                    or None if the curve type is GeomAbs_OtherCurve
        """
        brep_adaptor_curve = BRepAdaptor_Curve(self.topods_edge)
        curv_type = brep_adaptor_curve.GetType()
        if curv_type == GeomAbs_Line:
            return brep_adaptor_curve.Line()
        if curv_type == GeomAbs_Circle:
            return brep_adaptor_curve.Circle()
        if curv_type == GeomAbs_Ellipse:
            return brep_adaptor_curve.Ellipse()
        if curv_type == GeomAbs_Hyperbola:
            return brep_adaptor_curve.Hyperbola()
        if curv_type == GeomAbs_Parabola:
            return brep_adaptor_curve.Parabola()
        if curv_type == GeomAbs_BezierCurve:
            return brep_adaptor_curve.Bezier()
        if curv_type == GeomAbs_BSplineCurve:
            return brep_adaptor_curve.BSpline()
        if curv_type == GeomAbs_OffsetCurve:
            return brep_adaptor_curve.OffsetCurve()
        return None
