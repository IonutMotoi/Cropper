import argparse
import os
import cv2

from utils import is_overlapping, save_crops

WINDOW_NAME = "Patch Cropper"


def draw_squares(event, x, y, flags, param):
    """
    Handle mouse events to draw squares on the image.

    Args:
        event: OpenCV mouse event.
        x (int): X-coordinate of the mouse event.
        y (int): Y-coordinate of the mouse event.
        flags: Additional flags provided by OpenCV.
        param (list): Contains the image, the list of squares, and patch size.
    """
    # Get the image, patch size, squares, and preview square from param
    image, squares, patch_size = param

    # Adjust the center point if it's too close to the image boundaries
    x = max(patch_size // 2, min(image.shape[1] - patch_size // 2, x))
    y = max(patch_size // 2, min(image.shape[0] - patch_size // 2, y))

    # Compute the top left and bottom right points of the square
    top_left = (x - patch_size // 2, y - patch_size // 2)
    bottom_right = (x + patch_size // 2, y + patch_size // 2)

    image_copy = image.copy()

    cv2.rectangle(image_copy, top_left, bottom_right, (0, 255, 0), 4)

    # If the left mouse button was clicked, add the square to the list of squares
    if event == cv2.EVENT_LBUTTONDOWN:
        new_square = (top_left, bottom_right)
        # Check if the preview square overlaps with any of the existing squares
        for square in squares:
            if is_overlapping(new_square, square):
                return
        squares.append(new_square)

    # If the middle mouse button was clicked, remove the square that contains the point
    elif event == cv2.EVENT_MBUTTONDOWN:
        for square in squares:
            if square[0][0] <= x <= square[1][0] and square[0][1] <= y <= square[1][1]:
                squares.remove(square)
                break

    # Draw all the squares
    for square in squares:
        cv2.rectangle(image_copy, square[0], square[1], (0, 0, 255), 4)

    # Show the image with the squares
    cv2.imshow(WINDOW_NAME, image_copy)


def display_image(image_path, patch_size, squares, index, num_images):
    """
    Display an image and set up the mouse callback for drawing squares.

    Args:
        image_path (str): Path to the image file.
        patch_size (int): Size of the patch to be drawn.
        squares (list): List to store drawn squares.
        index (int): Current image index.
        num_images (int): Total number of images.
    """
    print(f"Displaying image {image_path}. ({index + 1}/{num_images})")
    squares.clear()
    image = cv2.imread(image_path)
    cv2.imshow(WINDOW_NAME, image)
    cv2.setMouseCallback(WINDOW_NAME, draw_squares, param=[image, squares, patch_size])


def navigate_images(images_path, output_path, patch_size):
    """
    Navigate through images, allowing the user to draw squares and save crops.

    Args:
        images_path (str): Directory containing the images.
        output_path (str): Directory where to save the crops.
        patch_size (int): Size of the patches to be created.
    """
    # Get a sorted list of all image files in the directory
    image_files = sorted([os.path.join(images_path, f)
                         for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])

    if not image_files:
        print("No images found in the directory.")
        return

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 900, 900)

    print("Instructions:")
    print("Press 'd' (next), 'a' (previous), 'q' (quit), 's' (save patches)")
    print("Left click (add square), middle click (remove square)\n")

    # Start at the first image
    index = 0
    squares = []
    display_image(image_files[index], patch_size, squares, index, len(image_files))

    while cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) > 0:
        key = cv2.waitKey(1000)

        if key == ord('q'):  # Quit
            break

        elif key == ord('d') and index < len(image_files) - 1:  # Next image
            index += 1
            squares = []
            display_image(image_files[index], patch_size, squares, index, len(image_files))

        elif key == ord('a') and index > 0:  # Previous image
            index -= 1
            display_image(image_files[index], patch_size, squares, index, len(image_files))

        elif key == ord('s'):  # Save the patches
            save_crops(image_files[index], squares, output_path)

    # Destroy all windows
    cv2.destroyAllWindows()


def main():
    """
    Parse command-line arguments and start the patch cropping tool.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images-path", type=str, required=True, help="Path to the input images")
    parser.add_argument("-o", "--output-path", type=str, default="./crops",
                        help="Path where to save the crops (default: ./crops)")
    parser.add_argument("-s", "--size", type=int, default=512, help="Size of the patches (default: 512)")
    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)
    if os.listdir(args.output_path):
        print("Warning: The output directory is not empty. Files may be overwritten.")
        confirm = input("Do you want to continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

    navigate_images(args.images_path, args.output_path, args.size)


if __name__ == "__main__":
    main()
