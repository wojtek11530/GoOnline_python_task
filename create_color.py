#!/usr/bin/python
import argparse
import re
from typing import List

from color import Color

AVAILABLE_MODES = ['mix', 'lowest', 'highest', 'mix-saturate']
DEFAULT_MODE = 'mix'
FILE_NAME = 'colors.txt'


def create_color():
    parser = argparse.ArgumentParser(
        description='Program for creating a new color from colors encoded in colors.txt and' +
                    'colors given by user as arguments.'
    )
    parser.add_argument('-m', '--mode', type=str, default='mix', metavar='MODE',
                        help="Mode for creating a new color, default: mix")
    parser.add_argument('color_codes', metavar='COLOR_CODES', type=str, nargs='*')

    args = parser.parse_args()
    color_codes = args.color_codes

    color_codes_from_file = get_colors_code_from_file()

    color_codes += color_codes_from_file
    colors = get_colors_from_codes(color_codes)

    if len(colors) > 0:
        mode = args.mode
        if mode not in AVAILABLE_MODES:
            mode = DEFAULT_MODE

        new_color = None
        if mode == 'mix':
            new_color = create_mix_color(colors)
        elif mode == 'lowest':
            new_color = create_lowest_color(colors)
        elif mode == 'highest':
            new_color = create_highest_color(colors)
        elif mode == 'mix-saturate':
            if len(colors) <= 1:
                print('Only one color in list. Cannot change the last color to have saturation '
                      'equal to average of the rest one')
            else:
                mix_saturate_color(colors)

        print('All colors:')
        for c in colors:
            print(c)

        if new_color is not None:
            print('New color:')
            print(new_color)
    else:
        print('No color found. New color cannot be created.')


def get_colors_from_codes(color_codes: List[str]) -> List[Color]:
    colors = []
    for cs in color_codes:
        if re.search("^([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$", cs):
            color = Color.from_hex_string(cs)
            colors.append(color)
        elif re.search("^([0-9]{1,3},){3}[0-9]{1,3}$", cs):
            color = Color.from_rgb_string(cs)
            colors.append(color)
        else:
            print(f"'{cs}' in wrong format. Cannot load color from it.")
    return colors


def get_colors_code_from_file() -> List[str]:
    color_strings_from_file = []
    try:
        with open(FILE_NAME) as f:
            lines = f.read().splitlines()
            for line in lines:
                if len(line) != 0:
                    color_strings_from_file.append(line)
    except FileNotFoundError:
        f'No file {FILE_NAME}. Cannot read colors from it.'

    return color_strings_from_file


def create_mix_color(colors: List[Color]) -> Color:
    colors_num = len(colors)
    new_red = int(sum(c.red for c in colors) / colors_num)
    new_blue = int(sum(c.blue for c in colors) / colors_num)
    new_green = int(sum(c.green for c in colors) / colors_num)
    new_alpha = int(sum(c.alpha for c in colors) / colors_num)
    return Color(red=new_red, green=new_green, blue=new_blue, alpha=new_alpha)


def create_lowest_color(colors: List[Color]) -> Color:
    new_red = min([c.red for c in colors])
    new_blue = min([c.blue for c in colors])
    new_green = min([c.green for c in colors])
    new_alpha = min([c.alpha for c in colors])
    return Color(red=new_red, green=new_green, blue=new_blue, alpha=new_alpha)


def create_highest_color(colors: List[Color]) -> Color:
    new_red = max([c.red for c in colors])
    new_blue = max([c.blue for c in colors])
    new_green = max([c.green for c in colors])
    new_alpha = max([c.alpha for c in colors])
    return Color(red=new_red, green=new_green, blue=new_blue, alpha=new_alpha)


def mix_saturate_color(colors: List[Color]) -> None:
    colors_num = len(colors[:-1])

    average_saturation = 0
    for c in colors[:-1]:
        H, S, L = c.get_HSL()
        average_saturation += S

    average_saturation = average_saturation / colors_num
    colors[-1].set_new_saturation(average_saturation)


if __name__ == '__main__':
    create_color()
