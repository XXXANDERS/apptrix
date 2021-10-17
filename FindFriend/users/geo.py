import math
from decimal import Decimal


def get_distance(lat1, lon1, lat2, lon2):
    lat1 *= Decimal(math.pi / 180)
    lon1 *= Decimal(math.pi / 180)
    lat2 *= Decimal(math.pi / 180)
    lon2 *= Decimal(math.pi / 180)
    d_lon = lon2 - lon1
    # d_lat = lat2 - lat1
    r = 6371.009  # среднее расстояние "радиусов" Земли. Погрешность при вычислении получается = 0.005
    delta = math.atan(
        math.sqrt((math.cos(lat2) * math.sin(d_lon)) ** 2 +
                  (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)) ** 2) /
        (math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(d_lon))
    )
    #########################################################################################################
    # подумать над вопросом деления на ноль: возможна ли такая ситуация
    #########################################################################################################

    d = delta * r
    return round(d, 6)
