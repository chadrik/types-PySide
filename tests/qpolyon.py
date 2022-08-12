from typing import List

from PySide2.QtGui import QPolygon
from PySide2.QtCore import QPoint


point: QPoint
point_list: List[QPoint]


point = QPoint()
point_list = [point]

polygon = QPolygon()  # type: QPolygon
polygon << point
polygon << point << point
polygon << [point, point]
polygon << [point, point] << [point, point]

assert type(polygon << point) == QPolygon
poly: QPolygon
poly = polygon << point

assert type(polygon << [point]) == QPolygon
poly = polygon << [point]

point_list = polygon + [point]
assert type(point_list) == list
assert type(point_list[0]) == QPoint
point_list = polygon + [point]

polygon += point
assert type(polygon) == QPolygon
