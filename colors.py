def main():
    pass


def rgb_to_hex(r, g, b, range='8bit'):
    if range == 'normalized':
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)

    r_hex = str(hex(r)).strip('0x')
    g_hex = str(hex(g)).strip('0x')
    b_hex = str(hex(b)).strip('0x')

    hex_color_code = f'#{r_hex}{g_hex}{b_hex}'
    return hex_color_code


if __name__ == "__main__":
    main()
