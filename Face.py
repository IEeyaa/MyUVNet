# -*- coding:utf-8 -*-
# @Author: IEeya
import numpy as np
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepTools import breptools
from OCC.Core.GeomAbs import *


class FaceModel:
    def __init__(self, topods_face, index_number):
        self.topods_face = topods_face
        self.index_number = index_number

    def uv_bounds(self):
        u_min, u_max, v_min, v_max = breptools.UVBounds(self.topods_face)
        print(u_min, u_max, v_min, v_max)

    def uv_grid_point(self):
        print(1)

    def surface_type(self):
        """
        Get the type of the surface geometry

        Returns:
            str: Type of the surface geometry
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

