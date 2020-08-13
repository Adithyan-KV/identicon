def main():
    get_color_from_hash(abs(hash("random_strin1")))


def get_color_from_hash(hash, bitdepth=8):
    bits_per_channel = 2**bitdepth
    # generate deterministic values for each channel from the random hash
    red_value = hash % bits_per_channel
    blue_value = (hash % 1000) % bits_per_channel
    green_value = ((hash % 1000000)//1000) % bits_per_channel
    hex_color_code = rgb_to_hex(red_value, green_value, blue_value)

    print(hex_color_code)


def rgb_to_hex(r, g, b):
    hex_r = f'{hex(r)}'.strip('0x')
    hex_g = f'{hex(g)}'.strip('0x')
    hex_b = f'{hex(b)}'.strip('0x')

    hex_code = f'#{hex_r}{hex_g}{hex_b}'

    return hex_code


if __name__ == "__main__":
    main()
