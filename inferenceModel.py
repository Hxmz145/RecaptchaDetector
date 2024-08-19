import cv2

# Splits the image into 9 images


def split_image(image_path):
    img = cv2.imread(image_path)

    height, width, _ = img.shape

    section_width = width // 3
    section_height = height // 3

    coordinates = []
    for y in range(3):
        for x in range(3):
            left = x * section_width
            upper = y * section_height
            right = left + section_width
            lower = upper + section_height
            coordinates.append((left, upper, right, lower))

    sections = [img[y:z, x:w] for x, y, w, z in coordinates]

    return sections
