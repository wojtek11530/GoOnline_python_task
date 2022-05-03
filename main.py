#!/usr/bin/python
from color import Color


def main():
    for hex_string in ['#ff00ff00', 'ff00ff11', 'f01', 'ff0011']:
        c = Color.from_hex_string(hex_string)
        print(c)

    for rgb_string in ['255,0,0,255', '3,0,0,1']:
        c = Color.from_rgb_string(rgb_string)
        print(c)


if __name__ == '__main__':
    main()
