# Day 8: Space Image Format
import matplotlib.pyplot as plt
import numpy as np


IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
TRANSPARENT_PIXEL = 2


def read_images(image_path, width, height):
    with open(image_path, 'r') as file:
        pixels = [int(d) for d in file.read().strip()]
        images = np.array(pixels).reshape((-1, height, width))
        return images


def show_image(image, *args, **kwargs):
    plt.imshow(image, *args, **kwargs)
    plt.show()


def show_images(images,):
    for image in images:
        show_image(image)


def part_one(images):
    image_with_fewest_zeros = images[np.argmax(np.count_nonzero(images, axis=(1, 2)))]
    answer = np.count_nonzero(image_with_fewest_zeros == 1) * np.count_nonzero(image_with_fewest_zeros == 2)
    print("Part one answer: {}".format(answer))


def part_two(images):
    merged_image = np.full(images.shape[1:], TRANSPARENT_PIXEL)
    for img in images:
        unfilled_pixels_in_destination = merged_image == TRANSPARENT_PIXEL
        filled_pixels_in_source = img != TRANSPARENT_PIXEL
        pixels_to_fill = np.logical_and(unfilled_pixels_in_destination, filled_pixels_in_source)
        merged_image[pixels_to_fill] = img[pixels_to_fill]
    show_image(merged_image, cmap=plt.get_cmap('binary'))


def main():
    images = read_images('8.txt', IMAGE_WIDTH, IMAGE_HEIGHT)
    # show_images(images)
    part_one(images.copy())
    part_two(images.copy())


if __name__ == "__main__":
    main()
