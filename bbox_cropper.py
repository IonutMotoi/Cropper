import argparse
import os
import cv2

from utils import is_overlapping, save_crops


WINDOW_NAME = "Bounding Box Cropper"
drawing = False  # True if drawing a bounding box
ix, iy = -1, -1  # Initial coordinates


def draw_rectangle(event, x, y, flags, param):
    """
    Handle mouse events to draw rectangles on the image.

    Args:
        event: OpenCV mouse event.
        x (int): X-coordinate of the mouse event.
        y (int): Y-coordinate of the mouse event.
        flags: Additional flags provided by OpenCV.
        param (list): Contains the image and the list of rectangles.
    """
    global ix, iy, drawing
    image, rectangles = param

    image_copy = image.copy()

    # Draw hovering vertical and horizontal lines
    cv2.line(image_copy, (x, 0), (x, image.shape[0]), (255, 255, 0), 3)
    cv2.line(image_copy, (0, y), (image.shape[1], y), (255, 255, 0), 3)

    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            # Start drawing a new rectangle
            drawing = True
            ix, iy = x, y
        else:
            x1, y1 = ix, iy
            x2, y2 = x, y
            top_left = (min(x1, x2), min(y1, y2))
            bottom_right = (max(x1, x2), max(y1, y2))
            new_rect = (top_left, bottom_right)
            # Check for overlap
            for rect in rectangles:
                if is_overlapping(new_rect, rect):
                    return
            rectangles.append(new_rect)
            # Finish drawing the rectangle
            drawing = False

    # If the middle mouse button was clicked, remove the rectangle that contains the point
    elif event == cv2.EVENT_MBUTTONDOWN:
        for rect in rectangles:
            if rect[0][0] <= x <= rect[1][0] and rect[0][1] <= y <= rect[1][1]:
                rectangles.remove(rect)
                break

    elif event == cv2.EVENT_RBUTTONDOWN:
        if drawing:
            # Cancel current drawing
            drawing = False

    # Draw the current rectangle
    if drawing:
        cv2.rectangle(image_copy, (ix, iy), (x, y), (0, 255, 0), 3)

    # Draw all rectangles
    for rect in rectangles:
        cv2.rectangle(image_copy, rect[0], rect[1], (0, 0, 255), 3)

    cv2.imshow(WINDOW_NAME, image_copy)


def display_image(image_path, rectangles, index, num_images):
    """
    Display an image and set up the mouse callback for drawing rectangles.

    Args:
        image_path (str): Path to the image file.
        rectangles (list): List to store drawn rectangles.
        index (int): Current image index.
        num_images (int): Total number of images.
    """
    print(f"Displaying image {image_path}. ({index + 1}/{num_images})")
    rectangles.clear()
    image = cv2.imread(image_path)
    cv2.imshow(WINDOW_NAME, image)
    cv2.setMouseCallback(WINDOW_NAME, draw_rectangle, param=[image, rectangles])


def navigate_images(images_path, output_path):
    """
    Navigate through images, allowing the user to draw rectangles and save crops.

    Args:
        images_path (str): Directory containing the images.
        output_path (str): Directory where to save the crops.
    """
    image_files = sorted([os.path.join(images_path, f)
                         for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])

    if not image_files:
        print("No images found in the directory.")
        return

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 900, 900)

    print("Instructions:")
    print("Press 'd' (next), 'a' (previous), 'q' (quit), 's' (save bounding boxes)")
    print("Left click (set corners), right click (cancel drawing)\n")

    index = 0
    rectangles = []
    display_image(image_files[index], rectangles, index, len(image_files))

    while cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) > 0:
        key = cv2.waitKey(1000)

        if key == ord('q'):
            break
        elif key == ord('d') and index < len(image_files) - 1:
            index += 1
            display_image(image_files[index], rectangles, index, len(image_files))
        elif key == ord('a') and index > 0:
            index -= 1
            display_image(image_files[index], rectangles, index, len(image_files))
        elif key == ord('s'):
            save_crops(image_files[index], rectangles, output_path)

    cv2.destroyAllWindows()


def main():
    """
    Parse command-line arguments and start the bounding box cropping tool.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str, required=True, help="Path to the input images")
    parser.add_argument("-o", "--output-path", type=str, default="./crops",
                        help="Path where to save the crops (default: ./crops)")
    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)
    if os.listdir(args.output_path):
        print("Warning: The output directory is not empty. Files may be overwritten.")
        confirm = input("Do you want to continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

    navigate_images(args.images_path, args.output_path)


if __name__ == "__main__":
    main()
