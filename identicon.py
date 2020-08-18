import hashlib
import colorsys
import numpy as np
from PIL import Image


def generate_identicon(username):
    image_data = ImageDataGenerator(username)
    img_bw_2d = image_data.image_matrix
    img_bw_3d = np.array([img_bw_2d for i in range(3)])
    color = image_data.color
    img_color = add_color_to_matrix(img_bw_3d, color)
    for i in range(5):
        for j in range(5):
            if img_color[i, j, 0] == 0:
                img_color[i, j] = image_data.bgcolor
    image = Image.fromarray(img_color.astype(np.uint8), 'RGB')
    image = image.resize((256, 256), resample=Image.NEAREST)
    image.save(f'{username}.png')


def add_color_to_matrix(matrix, color):
    """Takes in a 3d matrix with on or off pixel values and applies the color


    Args:
        matrix (nparray): 3D np array showing on and off pixel values
        color (tuple): the (R,G,B) tuple

    Returns:
        nparray: returns a 3D nparray that represents an image file, with the
        3 dimensions representing the RGB channels
    """
    for i in range(3):
        matrix[i, :, :] = np.round(matrix[i, :, :]*color[i]*255)

    reshaped_matrix = np.transpose(matrix, (1, 2, 0))

    return reshaped_matrix


class ImageDataGenerator():
    def __init__(self, username):
        # sha1 hash used over default hash in python as default hash is salted
        # and determinism is lost
        hash_hex = hashlib.sha1(username.encode('utf8')).hexdigest()
        self.hash_value = int(hash_hex, 16)
        self.pixel_matrix = self.pixel_matrix_from_hash(self.hash_value)
        self.color = self.random_color_from_hash(self.hash_value)
        self.bgcolor = [220, 220, 220]
        self.image_matrix = np.array(self.pixel_matrix)

    def pixel_matrix_from_hash(self, hash_value):
        """ iterate through the hash and set individual pixels to on or off
         depending on whether has value at index is odd or even"""
        pixel_matrix = [[0 for i in range(5)] for j in range(5)]
        # first 25 characters of the hash to enumerate over
        hash_string = str(hash_value).strip('-')[:24]
        for index, digit in enumerate(hash_string):
            x_index = index % 5
            y_index = index//5
            if y_index % 5 < 3:
                y_mirror_index = 4-y_index
                if int(digit) % 2 == 0:
                    # mirror values about y axis at center
                    pixel_matrix[x_index][y_index] = 1
                    pixel_matrix[x_index][y_mirror_index] = 1
                else:
                    pixel_matrix[x_index][y_index] = 0
                    pixel_matrix[x_index][y_mirror_index] = 0

        return pixel_matrix

    def random_color_from_hash(self, hash_value):
        # set a random hue value between 0 and 1 based on the hash
        hue = (hash_value % 100)/100
        # saturation, value hardcoded for consistency in palette
        saturation = 0.78
        value = 0.92
        color_rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return color_rgb


if __name__ == "__main__":
    generate_identicon('frillon')
