import colorsys
import hashlib
import numpy as np
from PIL import Image


def generate_identicon(username):
    """Generate an identicon and save as image

    Args:
        username (string): The username for which to generate identicon
    """
    # sha1 hash used over default hash in python as default hash is salted
    # and determinism is lost
    hash_hex = hashlib.sha1(username.encode('utf8')).hexdigest()
    hash_value = int(hash_hex, 16)
    image_data = generate_image_data(hash_value)
    image = Image.fromarray(image_data.astype(np.uint8), 'RGB')
    image = image.resize((256, 256), resample=Image.NEAREST)
    image.save(f'{username}.png')


def generate_image_data(hash_value):
    """Generates the pixel data for the image

    Args:
        hash_value (int): The hash value of the username of user

    Returns:
        img_colored (np.array): The matrix with pixel data
        of fully colored image
    """
    pixel_matrix = pixel_matrix_from_hash(hash_value)
    image_matrix = np.array(pixel_matrix)
    color = random_color_from_hash(hash_value)
    bgcolor = [220, 220, 220]  # RGB values
    img_bw_2d = image_matrix
    img_bw_3d = np.array([img_bw_2d for i in range(3)])
    img_fg_colored = add_color_to_matrix(img_bw_3d, color)
    img_colored = set_background_color(img_fg_colored, bgcolor)

    return img_colored


def set_background_color(image_matrix, color):
    """Sets the background pixels of the image to specified bg color

    Args:
        matrix (np.array): The image data with background pixels as 0
        color (array): The background color array in RGB format

    Returns:
        image_matrix (np.array): fully colorized image data with background 
        colors applied
    """
    for i in range(5):
        for j in range(5):
            if image_matrix[i, j, 0] == 0:
                image_matrix[i, j] = color

    return image_matrix


def add_color_to_matrix(matrix, color):
    """Takes in a 3d matrix with on or off pixel values and applies the color

    Args:
        matrix(nparray): 3D np array showing on and off pixel values
        color(tuple): the(R, G, B) tuple

    Returns:
        nparray: returns a 3D nparray that represents an image file, with the
        3 dimensions representing the RGB channels
    """
    for i in range(3):
        matrix[i, :, :] = np.round(matrix[i, :, :]*color[i]*255)

    reshaped_matrix = np.transpose(matrix, (1, 2, 0))

    return reshaped_matrix


def pixel_matrix_from_hash(hash_value):
    """Sets pixels of the image to on or off based on hash value.

    Args:
        hash_value (int): The hash value of the username of user

    Returns:
        np.array: A black and white pixel map matrix
    """
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


def random_color_from_hash(hash_value):
    # set a random hue value between 0 and 100 based on the hash
    hue = (hash_value % 100)/100
    # saturation, value hardcoded for consistency in palette
    saturation = 0.78
    value = 0.92
    color_rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return color_rgb


if __name__ == "__main__":
    generate_identicon('frillon')
