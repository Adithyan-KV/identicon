import identicon


def main():
    with open('name_list.txt') as name_list:
        for name in name_list:
            print(name.strip())
            # identicon.generate_identicon(name.strip())


if __name__ == "__main__":
    main()
