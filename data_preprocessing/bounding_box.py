from coordinate import Coordinate
class BoundingBox:
    def __init__(self, x_center=None, y_center=None, width=None, height=None):
        if x_center and y_center and width and height:
            x = int(x_center - width / 2)
            y = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            self.top_left_corner = Coordinate(x, y)
            self.bottom_right_corner = Coordinate(x2, y2)
            self.width = self.bottom_right_corner.x - self.top_left_corner.x
            self.height = self.bottom_right_corner.y - self.top_left_corner.y

    def normalize(self, image_width, image_height):
        x_center = (self.top_left_corner.x + self.bottom_right_corner.x) / 2 / image_width
        y_center = (self.top_left_corner.y + self.bottom_right_corner.y) / 2 / image_height
        width = self.width / image_width
        height = self.height / image_height

        return x_center, y_center, width, height

    @classmethod
    def from_corners(cls, top_left, bottom_right):
        width = bottom_right.x - top_left.x
        height = bottom_right.y - top_left.y
        x_center = top_left.x + width / 2
        y_center = top_left.y + height / 2
        return cls(x_center, y_center, width, height)

    @classmethod
    def from_normalized_coordinates(cls, normalized_coordinates, frame):
        x_center, y_center, width, height = normalized_coordinates
        x_center *= frame.shape[1]
        y_center *= frame.shape[0]
        width *= frame.shape[1]
        height *= frame.shape[0]

        return cls(x_center, y_center, width, height)