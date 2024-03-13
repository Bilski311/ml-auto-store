import cv2


def show_image_with_annotation(name, _class, frame, bounding_box):
    display_frame = frame.copy()
    cv2.rectangle(display_frame,
                  (bounding_box.top_left_corner.x, bounding_box.top_left_corner.y),
                  (bounding_box.bottom_right_corner.x, bounding_box.bottom_right_corner.y),
                  (255, 0, 0), 2)
    cv2.putText(display_frame, str(_class), (bounding_box.top_left_corner.x, bounding_box.top_left_corner.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow(name, display_frame)
    return cv2.waitKey(0)
