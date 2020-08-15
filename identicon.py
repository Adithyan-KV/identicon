import hashlib
import colorsys
import colors


def main():
    image_data = ImageDataGenerator('how to')


def get_color_from_hash(hash_value, bitdepth=8):
    bits_per_channel = 2**bitdepth
    # generate deterministic values for each channel from the random hash
    red_value = hash_value % bits_per_channel
    blue_value = (hash_value % 1000) % bits_per_channel
    green_value = ((hash_value % 1000000)//1000) % bits_per_channel
    hex_color_code = rgb_to_hex(red_value, green_value, blue_value)

    print(hex_color_code)


def rgb_to_hex(r, g, b):
    hex_r = f'{hex(r)}'.strip('0x')
    hex_g = f'{hex(g)}'.strip('0x')
    hex_b = f'{hex(b)}'.strip('0x')

    hex_code = f'#{hex_r}{hex_g}{hex_b}'

    return hex_code


class ImageDataGenerator():
    def __init__(self, username):
        # sha1 hash used over default hash in python as default hash is salted
        # and determinism is lost
        hash_hex = hashlib.sha1(username.encode('utf8')).hexdigest()
        self.hash_value = int(hash_hex, 16)
        self.pixel_matrix = self.pixel_matrix_from_hash(self.hash_value)
        self.color = self.random_color_from_hash(self.hash_value)

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
                    pixel_matrix[x_index][y_index] = 0
                    pixel_matrix[x_index][y_mirror_index] = 0
                else:
                    pixel_matrix[x_index][y_index] = 1
                    pixel_matrix[x_index][y_mirror_index] = 1

        return pixel_matrix

    def random_color_from_hash(self, hash_value):
        # set a random hue value between 0 and 1 based on the hash
        hue = (hash_value % 100)/100
        # saturation, value hardcoded for consistency in palette
        saturation = 0.78
        value = 0.92
        color_rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_code = colors.rgb_to_hex(
            color_rgb[0], color_rgb[1], color_rgb[2], 'normalized')
        return hex_code


if __name__ == "__main__":
    main()
