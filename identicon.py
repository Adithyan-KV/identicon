import colorsys
import hashlib
import numpy as np
import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt


def generate_identicon(username, size=256, path=os.getcwd(), file_format='png'):
    """Generate an identicon and save as image

    Args:
        username (str): The username for which to generate identicon
        size (int) [optional, default = 256]:
            The dimension of the side of the square image in pixels
        path (str) [optional, default = current working directory]:
            The path to the folder in which the image is to be saved
        file_format(str) [optional, default = JPEG format]:
            'png': save as PNG
    """
    # sha1 hash used over default hash in python as default hash is salted
    # and determinism is lost
    hash_hex = hashlib.sha1(username.encode('utf8')).hexdigest()
    hash_value = int(hash_hex, 16)
    image_data = generate_image_data(hash_value)
    image = Image.fromarray(image_data.astype(np.uint8), 'RGB')
    padding = round(size*0.1)
    content = size-padding
    resized_image = image.resize((content, content), resample=Image.NEAREST)
    padded_image = ImageOps.expand(resized_image, padding, (220, 220, 220))
    plt.imshow(padded_image)
    plt.show()
    save_image(padded_image, path, username, file_format)


def save_image(image, path, filename, format):
    """Saves the image file in the specified format to the specified path

    Args:
        image (np.array): The image data
        path (str): The path to the folder in which to save
        filename (str): the name of the image file
        format (str): The format in which to save the image
    """
    supported_extensions = ['jpeg', 'jpg', 'png']
    if format.lower() in supported_extensions:
        if os.path.exists(path):
            path_to_file = os.path.join(path, f'{filename}.{format}')
            try:
                image.save(path_to_file)
            except Exception:
                raise Exception("Couldn't write to image")
        else:
            raise OSError(f"the path {path} doesn't exist")
    else:
        raise Exception(f'Invalid file extension {format}')


def generate_image_data(hash_value):
    """Generates the pixel data for the image

    Args:
        hash_value (int): The hash value of the username of user

    Returns:
        img_colored (np.array): The matrix with pixel data
        of fully colored image
    """
    pixel_matrix = pixel_matrix_from_hash(hash_value)
    color = random_color_from_hash(hash_value)
    bg_color = np.array([220, 220, 220])  # RGB values
    bw_img = np.repeat(pixel_matrix[:,:,np.newaxis],3,axis=2)
    fg_img = bw_img*color*255
    bg_img = (bw_img==0)*bg_color
    final_img = fg_img+bg_img
    return final_img

def pixel_matrix_from_hash(hash_value):
    """Sets pixels of the image to on or off based on hash value.

    Args:
        hash_value (int): The hash value of the username of user

    Returns:
        np.array: A symmetric black and white pixel map matrix
    """
    pixel_matrix = np.zeros((5,5))
    # first 25 characters of the hash to enumerate over
    hash_string = str(hash_value).strip('-')[:14]
    for index, digit in enumerate(hash_string):
        row = index//3
        column = index % 3
        mirror_column = 4-column
        if int(digit) % 2 == 0:
            # mirror values about y axis at center
            pixel_matrix[row,column] = 1
            pixel_matrix[row,mirror_column] = 1
        else:
            pixel_matrix[row,column] = 0
            pixel_matrix[row,mirror_column] = 0

    return pixel_matrix


def random_color_from_hash(hash_value):
    """Take a hash and return a color value corresponding to it

    Args:
        hash_value (int): The hash of a username

    Returns:
        tuple: color corresponding to hash as R,G,B
    """
    # set a random hue value between 0 and 100 based on the hash
    hue = (hash_value % 100)/100
    # saturation, value hardcoded for consistency in palette
    saturation = 0.78
    value = 0.92
    color_rgb = np.array(colorsys.hsv_to_rgb(hue, saturation, value))
    return color_rgb


if __name__ == "__main__":
    generate_identicon('phoney badger')
