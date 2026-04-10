import numpy as np
import math

HEX_SIZE = 30
OFFSET_X = 600
OFFSET_Y = 500

def hex_to_pixel(i, j, radius):
    dj = j - radius
    di = i - radius

    hex_width = math.sqrt(3) * HEX_SIZE

    y = (dj + di / 2) * hex_width
    x = di * HEX_SIZE * 1.5

    return x + OFFSET_X, y + OFFSET_Y


def pixel_to_hex(x, y, tabla_recnik, radius):

    najblizi_hex = None
    least_dist = float('inf')

    for koordinate in tabla_recnik.keys():
        i, j = koordinate

        cx, cy = hex_to_pixel(i, j, radius)

        dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)

        if dist < least_dist:
            least_dist = dist
            najblizi_hex = (i, j)

    if least_dist <= HEX_SIZE:
        return najblizi_hex
    else:
        return None