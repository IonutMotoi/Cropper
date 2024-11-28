import cv2
import os


def is_overlapping(rect1, rect2):
    """
    Check if two rectangles overlap.

    Args:
        rect1 (tuple): Coordinates of the first rectangle as ((x1, y1), (x2, y2)).
        rect2 (tuple): Coordinates of the second rectangle as ((x1, y1), (x2, y2)).

    Returns:
        bool: True if the rectangles overlap, False otherwise.
    """
    # If one rectangle is to the right of the other or above the other, they don't overlap
    if rect1[1][0] < rect2[0][0] or rect1[0][0] > rect2[1][0] or rect1[1][1] < rect2[0][1] or rect1[0][1] > rect2[1][1]:
        return False
    return True


def save_crops(image_path, bboxes, output_path):
        image = cv2.imread(image_path)
        for i, bbox in enumerate(bboxes):
            patch = image[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
            cv2.imwrite(os.path.join(output_path, f"{os.path.basename(image_path)[:-4]}_{i}.png"), patch)
        print(f"Number or crops saved for {os.path.basename(image_path)}: {len(bboxes)}")
