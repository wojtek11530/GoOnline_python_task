import re
from typing import Tuple

MIN_BOUND = 0
MAX_BOUND = 255


class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int):
        for name, value in {"red": red, "green": green, "blue": blue, "alpha": alpha}.items():
            if not MIN_BOUND <= value <= MAX_BOUND:
                raise ValueError(f'{name} value must be within range [{MIN_BOUND}, {MAX_BOUND}]')

        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __str__(self):
        H, S, L = self.get_HSL()
        return 'Color:\n' + \
               f'\tRGBA: ({self.red},{self.green},{self.blue},{self.alpha})\n' + \
               f'\tHEX: {self.to_hex_format()}\n' + \
               f'\tHue: {H:.2f}\n' + \
               f'\tSaturation: {S:.4f}\n' + \
               f'\tLightness: {L:.4f}'

    @classmethod
    def from_hex_string(cls, hex_string: str) -> "Color":
        match_hash = re.search("^#", hex_string)
        if match_hash is not None:
            hex_string = hex_string[match_hash.span()[1]:]

        if not re.search("^([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$", hex_string):
            raise ValueError(f'{hex_string} is not correct hex format.')

        if re.search("^[0-9a-f]{3}$", hex_string):
            match_digits = re.findall("[0-9a-f]", hex_string)
            hex_string = ''.join([2 * d for d in match_digits])

        match_components = re.findall("[0-9a-f]{2}", hex_string)
        assert len(match_components) in [3, 4]

        red = int(match_components[0], 16)
        green = int(match_components[1], 16)
        blue = int(match_components[2], 16)
        if len(match_components) == 4:
            alpha = int(match_components[3], 16)
        else:
            alpha = 255

        return Color(red=red, green=green, blue=blue, alpha=alpha)

    @classmethod
    def from_rgb_string(cls, rgb_string: str) -> "Color":
        if not re.search("^([0-9]{1,3},){3}[0-9]{1,3}$", rgb_string):
            raise ValueError(f'{rgb_string} is not correct RGB format.')

        match_components = re.findall("[0-9]{1,3}", rgb_string)
        assert len(match_components) == 4

        red = int(match_components[0])
        green = int(match_components[1])
        blue = int(match_components[2])
        alpha = int(match_components[3])
        return Color(red=red, green=green, blue=blue, alpha=alpha)

    def to_hex_format(self) -> str:
        hex_string = '#'
        hex_string += self._get_hexadecimal_format(self.red)
        hex_string += self._get_hexadecimal_format(self.green)
        hex_string += self._get_hexadecimal_format(self.blue)
        hex_string += self._get_hexadecimal_format(self.alpha)
        return hex_string

    def get_HSL(self) -> Tuple[float, float, float]:
        red_prime = self.red / MAX_BOUND
        green_prime = self.green / MAX_BOUND
        blue_prime = self.blue / MAX_BOUND

        max_rgb = max(red_prime, green_prime, blue_prime)
        min_rgb = min(red_prime, green_prime, blue_prime)

        lightness = 0.5 * (max_rgb + min_rgb)
        range = max_rgb - min_rgb

        if lightness in [0, 1]:
            saturation = 0
        elif lightness <= 0.5:
            saturation = 0.5 * range / lightness
        else:
            saturation = 0.5 * range / (1 - lightness)

        if range == 0:
            hue = 0
        elif max_rgb == red_prime:
            hue = ((green_prime - blue_prime) / range) % 6
        elif max_rgb == green_prime:
            hue = (blue_prime - red_prime) / range + 2
        else:
            hue = (red_prime - green_prime) / range + 4

        hue = hue * 60
        return hue, saturation, lightness

    def set_new_saturation(self, new_S: float) -> None:
        H, S, L = self.get_HSL()
        C = (1 - abs(2 * L - 1)) * new_S
        X = C * (1 - abs((H / 60) % 2 - 1))

        if 0 <= H < 60:
            new_r_prime = C
            new_g_prime = X
            new_b_prime = 0
        elif 60 <= H < 120:
            new_r_prime = X
            new_g_prime = C
            new_b_prime = 0
        elif 120 <= H < 180:
            new_r_prime = 0
            new_g_prime = C
            new_b_prime = X
        elif 180 <= H < 240:
            new_r_prime = 0
            new_g_prime = X
            new_b_prime = C
        elif 240 <= H < 300:
            new_r_prime = X
            new_g_prime = 0
            new_b_prime = C
        else:
            new_r_prime = C
            new_g_prime = 0
            new_b_prime = X

        m = L - C / 2

        self.red = int(MAX_BOUND * (new_r_prime + m))
        self.green = int(MAX_BOUND * (new_g_prime + m))
        self.blue = int(MAX_BOUND * (new_b_prime + m))

    @staticmethod
    def _get_hexadecimal_format(number: int) -> str:
        hex_format = hex(number).replace("0x", "")
        if len(hex_format) == 1:
            hex_format = '0' + hex_format

        return hex_format
