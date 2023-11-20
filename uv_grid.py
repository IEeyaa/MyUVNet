# -*- coding:utf-8 -*-
# @Author: IEeya
import numpy as np


def get_uvgrid_by_face(face, num_u=10, num_v=10, uvs=False, method="point"):
    """
    Creates a 2D UV-grid of samples from the given face

    Args:
        face (occwl123.face.Face): A B-rep face
        num_u (int): Number of samples along u-direction. Defaults to 10.
        num_v (int): Number of samples along v-direction. Defaults to 10.
        uvs (bool): Return the surface UVs where quantities are evaluated. Defaults to False.
        method (str): Name of the method in the occwl123.face.Face object to be called
                      (the method has to accept the uv value as argument). Defaults to "point".

    Returns:
        np.ndarray: 2D array of quantity evaluated on the face geometry
        np.ndarray (optional): 2D array of uv-values where evaluation was done
    """
    assert num_u >= 2
    assert num_v >= 2
    uv_box = face.uv_bounds()

    fn = getattr(face, method)

    uvgrid = []
    uv_values = np.zeros((num_u, num_v, 2), dtype=np.float32)

    if type(face.surface()) is float:
        if uvs:
            return None, uv_values
        return None

    for i in range(num_u):
        u = uv_box.intervals[0].interpolate(float(i) / (num_u - 1))
        for j in range(num_v):
            v = uv_box.intervals[1].interpolate(float(j) / (num_v - 1))
            uv = np.array([u, v])
            uv_values[i, j] = uv
            val = fn(uv)
            uvgrid.append(val)
    uvgrid = np.asarray(uvgrid).reshape((num_u, num_v, -1))


    if uvs:
        return uvgrid, uv_values
    return uvgrid
