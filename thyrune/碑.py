from typing import List

import numpy as np
from stl import mesh


def 矩形分割算法(d: np.array) -> list:
    # 我已经忘记了这个算法怎么写了，所以我来写一个奇怪版的
    res = []
    for x, _l in enumerate(d):
        now = None
        for y, h in enumerate(_l):
            if h == 0:
                if now:
                    res.append(now)
                    now = None
                continue
            assert h == 1
            if now is None:
                now = [x, y, 1, 1]
            else:
                now[3] += 1
        if now:
            res.append(now)
    return res


def box(x=0, y=0, z=0, sx=1, sy=1, sz=1) -> np.array:
    r = []
    for p in range(2):
        for q in range(2):
            r.append([[0, 1, p],
                      [1, q, p],
                      [q, 0, p]])
            r.append([[p, q, q],
                      [p, 0, 1],
                      [p, 1, 0]])
            r.append([[0, p, 0],
                      [q, p, 1-q],
                      [1, p, 1]])
    data = np.zeros(len(r), dtype=mesh.Mesh.dtype)
    for i, l in enumerate(r):
        data['vectors'][i] = np.array(l)
    data['vectors'][:, :] *= (sx, sy, sz)
    data['vectors'][:, :] += (x, y, z)
    return data


def _碑(data: np.array, X: int, Y: int, S: float) -> mesh.Mesh:
    assert len(data) == X * Y
    layer = np.ones(shape=(X+4, Y+4), dtype=np.uint8)
    layer[1:-1, 1:-1] = 0
    layer[-3:-1, -3:-1] = 1
    p = 0
    for x in range(2, X+2):
        for y in range(2, Y+2):
            layer[x, y] = data[p]
            p += 1
    bl = np.concatenate([box(x, y, 0, dx, dy, 1) for x, y, dx, dy in 矩形分割算法(layer)] + [box(0, 0, -1, X+4, Y+4, 1)])
    bl['vectors'] *= S
    return mesh.Mesh(bl, remove_empty_areas=False)


def 碑(data: bytes, X: int = 32, Y: int = 32, S: float = 2) -> List[mesh.Mesh]:
    data = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    res = []
    while len(data):
        if len(data) < X*Y:
            data = np.concatenate((data, np.zeros(X*Y-len(data), dtype=np.uint8)))
        res.append(_碑(data[:X*Y], X, Y, S))
        data = data[X*Y:]
    return res
