#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Unicode font rendering & scrolling.
"""

import os
import random
import time
from luma.core.virtual import viewport, snapshot, range_overlap, terminal
from luma.core.sprite_system import framerate_regulator
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306


welcome = [ 
    u"Бзиала шәаабеит",
    u"Къеблагъ",
    u"Welkom",
    u"Bienvenue",
    u"Maayong pag-abot",
    u"Mayad-ayad nga pad-abot",
    u"Mir se vjên",
    u"እንኳን ደህና መጣህ።",
    u"Willkumme",
    u"أهلاً و سهل",
    u"مرحابة",
    u"Bienvenius",
    u"Բարի գալուստ!",
    u"আদৰণি",
    u"歡迎光臨",
    u"ᑕᑕᐊᐧᐤ",
    u"Woé zɔ",
    u"Bula",
    u"Vælkomin",
    u"Buiti achüluruni",
    u"પધારો",
    u"ברוך הבא",
    u"Üdvözlet",
    u"ಸುಸ್ವಾಗತ",
    u"Приємаєме"
    u"Xoş gəlmişsiniz!",
    u"Salamat datang",
    u"Сәләм бирем!",
    u"Ongi etorri",
    u"Menjuah-juah!",
    u"স্বাগতম",
    u"Добре дошли",
    u"வாருங்கள்",
    u"Kíimak 'oolal",
    u"Märr-ŋamathirri",
    u"Benvinguts",
    u"Марша дагIийла шу",
    u"歡迎",
    u"Velkommen",
    u"Welcome",
    u"Wäljkiimen",
    u"კეთილი იყოს თქვენი",
    u"Καλώς Όρισες",
    u"Eguahé porá",
    u"Sannu da zuwa",
    u"Aloha",
    u"सवागत हैं",
    u"Selamat datang",
    u"Fáilte",
    u"ようこそ",
    u"Ирхитн эрҗәнәвидн",
    u"Witôj",
    u"សូម​ស្វាគមន៍",
    u"환영합니다",
    u"ຍິນດີຕ້ອນຮັບ",
    u"Swagatam",
    u"Haere mai",
    u"Тавтай морилогтун",
    u"خوش آمدید",
    u"Witam Cię",
    u"ਜੀ ਆਇਆ ਨੂੰ।",
    u"Bon vinuti",
    u"ยินดีต้อนรับ",
    u"Hoş geldiniz",
    u"Croeso",
    u"Bonvenon"
]

colors = [
    "lightpink", "pink", "crimson", "lavenderblush", "palevioletred", "hotpink",
    "deeppink", "mediumvioletred", "orchid", "thistle", "plum", "violet",
    "magenta", "fuchsia", "darkmagenta", "purple", "mediumorchid", "darkviolet",
    "darkorchid", "indigo", "blueviolet", "mediumpurple", "mediumslateblue",
    "slateblue", "darkslateblue", "lavender", "ghostwhite", "blue", "mediumblue",
    "midnightblue", "darkblue", "navy", "royalblue", "cornflowerblue",
    "lightsteelblue", "lightslategray", "slategray", "dodgerblue", "aliceblue",
    "steelblue", "lightskyblue", "skyblue", "deepskyblue", "lightblue",
    "powderblue", "cadetblue", "azure", "lightcyan", "paleturquoise", "cyan",
    "aqua", "darkturquoise", "darkslategray", "darkcyan", "teal",
    "mediumturquoise", "lightseagreen", "turquoise", "aquamarine",
    "mediumaquamarine", "mediumspringgreen", "mintcream", "springgreen",
    "mediumseagreen", "seagreen", "honeydew", "lightgreen", "palegreen",
    "darkseagreen", "limegreen", "lime", "forestgreen", "green", "darkgreen",
    "chartreuse", "lawngreen", "greenyellow", "darkolivegreen", "yellowgreen",
    "olivedrab", "beige", "lightgoldenrodyellow", "ivory", "lightyellow",
    "yellow", "olive", "darkkhaki", "lemonchiffon", "palegoldenrod", "khaki",
    "gold", "cornsilk", "goldenrod", "darkgoldenrod", "floralwhite", "oldlace",
    "wheat", "moccasin", "orange", "papayawhip", "blanchedalmond", "navajowhite",
    "antiquewhite", "tan", "burlywood", "bisque", "darkorange", "linen", "peru",
    "peachpuff", "sandybrown", "chocolate", "saddlebrown", "seashell", "sienna",
    "lightsalmon", "coral", "orangered", "darksalmon", "tomato", "mistyrose",
    "salmon", "snow", "lightcoral", "rosybrown", "indianred", "red", "brown",
    "firebrick", "darkred", "maroon", "white", "whitesmoke", "gainsboro",
    "lightgrey", "silver", "darkgray", "gray", "dimgray", "black"
]


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), name))
    return ImageFont.truetype(font_path, size)


def lerp_1d(start, end, n):
    delta = float(end - start) / float(n)
    for i in range(n):
        yield int(round(start + (i * delta)))
    yield end


def lerp_2d(start, end, n):
    x = lerp_1d(start[0], end[0], n)
    y = lerp_1d(start[1], end[1], n)

    try:
        while True:
            yield next(x), next(y)
    except StopIteration:
        pass


def pairs(generator):
    try:
        last = next(generator)
        while True:
            curr = next(generator)
            yield last, curr
            last = curr
    except StopIteration:
        pass


def infinite_shuffle(arr):
    copy = list(arr)
    while True:
        random.shuffle(copy)
        for elem in copy:
            yield elem


def make_snapshot(width, height, text, fonts, color="white"):

    def render(draw, width, height):
        t = text

        for font in fonts:
            size = draw.multiline_textsize(t, font)
            if size[0] > width:
                t = text.replace(" ", "\n")
                size = draw.multiline_textsize(t, font)
            else:
                break

        left = (width - size[0]) // 2
        top = (height - size[1]) // 2
        draw.multiline_text((left, top), text=t, font=font, fill=color,
                            align="center", spacing=-2)

    return snapshot(width, height, render, interval=10)


def random_point(maxx, maxy):
    return random.randint(0, maxx), random.randint(0, maxy)


def overlapping(pt_a, pt_b, w, h):
    la, ta = pt_a
    ra, ba = la + w, ta + h
    lb, tb = pt_b
    rb, bb = lb + w, tb + h
    return range_overlap(la, ra, lb, rb) and range_overlap(ta, ba, tb, bb)


def welcome_fn():
    regulator = framerate_regulator(fps=30)
    fonts = [make_font("code2000.ttf", sz) for sz in range(24, 8, -2)]
    sq = device.width * 2
    virtual = viewport(device, sq, sq)

    color_gen = pairs(infinite_shuffle(colors))

    for welcome_a, welcome_b in pairs(infinite_shuffle(welcome)):
        color_a, color_b = next(color_gen)
        widget_a = make_snapshot(device.width, device.height, welcome_a, fonts, color_a)
        widget_b = make_snapshot(device.width, device.height, welcome_b, fonts, color_b)

        posn_a = random_point(virtual.width - device.width, virtual.height - device.height)
        posn_b = random_point(virtual.width - device.width, virtual.height - device.height)

        while overlapping(posn_a, posn_b, device.width, device.height):
            posn_b = random_point(virtual.width - device.width, virtual.height - device.height)

        virtual.add_hotspot(widget_a, posn_a)
        virtual.add_hotspot(widget_b, posn_b)

        for _ in range(30):
            with regulator:
                virtual.set_position(posn_a)

        for posn in lerp_2d(posn_a, posn_b, device.width // 4):
            with regulator:
                virtual.set_position(posn)

        virtual.remove_hotspot(widget_a, posn_a)
        virtual.remove_hotspot(widget_b, posn_b)

def terminal_fn():
    while True:
        for fontname, size in [("THSarabunNew.ttf", 15)]:
            font = make_font(fontname, size) if fontname else None
            term = terminal(device, font)

            term.println("ทดสอบภาษาไทย")
            term.println("------------------")
            term.println("Uses any font to output text using a number of different print methods.")
            term.println()
            time.sleep(2)
            term.println("The '{0}' font supports a terminal size of {1}x{2} characters.".format(fontname, term.width, term.height))
            term.println()
            time.sleep(2)
            term.println("An animation effect is defaulted to give the appearance of spooling to a teletype device.")
            term.println()
            time.sleep(2)

            term.println("".join(chr(i) for i in range(32, 127)))
            time.sleep(2)

            term.clear()
            for i in range(30):
                term.println("Line {0:03d}".format(i))

            term.animate = False
            time.sleep(2)
            term.clear()

            term.println("Progress bar")
            term.println("------------")
            for mill in range(0, 10001, 25):
                term.puts("\rPercent: {0:0.1f} %".format(mill / 100.0))
                term.flush()

            time.sleep(2)
            term.clear()
            term.puts("Backspace test.")
            term.flush()
            time.sleep(2)
            for _ in range(17):
                term.backspace()
                time.sleep(0.2)

            time.sleep(2)
            term.clear()
            term.animate = True
            term.println("Tabs test")
            term.println("|...|...|...|...|...|")
            term.println("1\t2\t4\t11")
            term.println("992\t43\t9\t12")
            term.println("\t3\t99\t1")
            term.flush()
            time.sleep(2)

if __name__ == "__main__":
    try:
        serial = i2c(port=0, address=0x3C)
        device = ssd1306(serial)
        device.clear()
        welcome_fn()
    except KeyboardInterrupt:
        pass