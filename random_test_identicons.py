import identicon


def main():
    with open('name_list.txt') as name_list:
        for name in name_list:
            identicon.generate_identicon(name.strip(), 256)


if __name__ == "__main__":
    main()
