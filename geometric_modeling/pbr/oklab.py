from math import sin, cos, atan2

def rgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l = l ** (1./3.)
    m = m ** (1./3.)
    s = s ** (1./3.)

    L =   0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a =   1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    b =   0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s

    return (L, a, b)


def oklab_to_rgb(L, a, b):
    l = L + 0.3963377774 * a + 0.2158037573 * b;
    m = L - 0.1055613458 * a - 0.0638541728 * b;
    s = L - 0.0894841775 * a - 1.2914855480 * b;

    l = l ** 3
    m = m ** 3
    s = s ** 3

    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    return (r, g, b)


def oklab_to_lch(lightness, greenred, blueyellow):
    chroma = (greenred**2 + blueyellow**2) ** 0.5
    hue = atan2(blueyellow, greenred)
    return (lightness, chroma, hue)


def lch_to_oklab(lightness, chroma, hue):
    greenred = chroma * cos(hue)
    blueyellow = chroma * sin(hue)
    return (lightness, greenred, blueyellow)


#for r, g, b in [(0.95, 1, 1.089), (1, 0, 0), (0, 1, 0), (0, 0, 1)]:
#    print(rgb_to_oklab(r, g, b))
#print(oklab_to_rgb(0.5, 0.1, 0.))
#print(f"sRGB (0, 1, 0a)  Lab: {rgb_to_oklab(1, 0, 0)}")
#print(f"Green Lab: {rgb_to_oklab(0, 1, 0)}")
#print(f"Blue  Lab: {rgb_to_oklab(0, 0, 1)}")
#L, a, b = rgb_to_oklab(0,0,1)
#print(L**2 + a**2 + b**2)

#print(rgb_to_oklab(1,0,0))
#print(rgb_to_oklab(0,1,1))
#print()
#print(rgb_to_oklab(0,1,0))
#print(rgb_to_oklab(1,0,1))
#print()
#print(rgb_to_oklab(0,0,1))
#print(rgb_to_oklab(1,1,0))

# for r, g, b in [(1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1)]:
#     l, c, h = oklab_to_lch(*rgb_to_oklab(r, g, b))
#     print(f"RGB: {r}, {g}, {b} -> LCh: {l}, {c}, {h}")
# from math import pi
# for l, c, h in [(0.5, 0.25, -pi + 2 * pi * (h/10.))
#                 for h in range(10)]:
#     r, g, b = oklab_to_rgb(*lch_to_oklab(l, c, h))
#     print(f"RGB: {r: 1.2f}, {g: 1.2f}, {b: 1.2f} <-> LCh: {l: 1.2f}, {c: 1.2f}, {h: 1.2f}")
