import numpy as np
import numpy.linalg as npla
from numba import jit

def interpolate3d(p1, p2, p3, p4, point, v1, v2, v3, v4):
    J = np.array([[p2[0]-p1[0], p3[0]-p1[0], p4[0]-p1[0]],
                  [p2[1]-p1[1], p3[1]-p1[1], p4[1]-p1[1]],
                  [p2[2]-p1[2], p3[2]-p1[2], p4[2]-p1[2]]])
    J = npla.inv(J)

    # ref1 = J.dot(np.array([ p1[0]-p1[0], p1[1]-p1[1], p1[2]-p1[2] ]))
    # ref2 = J.dot(np.array([ p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2] ]))
    # ref3 = J.dot(np.array([ p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2] ]))
    # ref4 = J.dot(np.array([ p4[0]-p1[0], p4[1]-p1[1], p4[2]-p1[2] ]))
    ref_point = J.dot(np.array([ point[0]-p1[0], point[1]-p1[1], point[2]-p1[2] ]))

    tot_vol = 1./6  # Volume of trirectangular tetrahedron
    # Volume of tetrahedron = 1/3 * base_area * height
    vol2 = (1./3)*(1./2)*ref_point[0]
    vol3 = (1./3)*(1./2)*ref_point[1]
    vol4 = (1./3)*(1./2)*ref_point[2]
    vol1 = tot_vol - vol2 - vol3 - vol4

    v_point = v1*(vol1/tot_vol) + v2*(vol2/tot_vol) + v3*(vol3/tot_vol) + v4*(vol4/tot_vol)

    mask = np.ones_like(v_point, dtype="bool")
    for v in [vol1, vol2, vol3, vol4]:
        mask *= (v/tot_vol) > 0
        mask *= (v/tot_vol) < 1

    return v_point, mask

@jit
def interpolate2d(p1, p2, p3, point, v1, v2, v3):
    trans = np.array([[ p2[0]-p1[0], p3[0]-p1[0] ],
                      [ p2[1]-p1[1], p3[1]-p1[1] ]])
    trans = npla.inv(trans)

    ref_point = np.empty_like(point)
    for i in range(point.shape[0]):
        for j in range(point.shape[1]):
            ref_point[i][j] = trans[i,0]*(point[0,j]-p1[i]) + trans[i,1]*(point[1,j]-p1[i])

    tot_area = 0.5  # Area of 45-45-90 triangle, side length=1
    area2 = 0.5*1*ref_point[0]
    area3 = 0.5*1*ref_point[1]
    area1 = tot_area - area2 - area3

    v_point = v1*(area1/tot_area) + v2*(area2/tot_area) + v3*(area3/tot_area)

    mask = np.ones_like(v_point, dtype="bool")
    for a in [area1, area2, area3]:
        print a     # only works with print statement?
        mask *= (a/tot_area) > 0
        mask *= (a/tot_area) < 1

    return v_point, mask
