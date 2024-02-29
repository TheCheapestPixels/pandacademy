# Obvious colors
sixth = 1.0/6.0
red    = (      0.0, 1.0, 1.0)
yellow = (1 * sixth, 1.0, 1.0)
green  = (2 * sixth, 1.0, 1.0)
cyan   = (3 * sixth, 1.0, 1.0)
blue   = (4 * sixth, 1.0, 1.0)
purple = (5 * sixth, 1.0, 1.0)

# Named colors
tyrian_purple = (0.903, 0.98, 0.400)
neon_cyan     = (0.499, 1.00, 0.996)

# My colors
bright_pink   = (0.833, 0.70, 0.800)


def gradient(gradient):
    def inner(value):
        if value in gradient:
            return gradient[value]
        sub_grad_start = max(v for v in gradient.keys() if v <= value)
        sub_grad_end = min(v for v in gradient.keys() if v >= value)
        blend_ratio = (value - sub_grad_start) / (sub_grad_end - sub_grad_start)
        start_hue, start_saturation, start_value = gradient[sub_grad_start]
        end_hue, end_saturation, end_value = gradient[sub_grad_end]
    
        if abs(end_hue - start_hue) < 0.5:  # We can use the basic lerp
            point_hue = start_hue + blend_ratio * (end_hue - start_hue)
        else: # We have to go through the wrap-around point
            delta = end_hue - start_hue
            if delta > 0.0:
                counter_vec = delta - 1
            else:
                counter_vec = delta + 1
            point_hue = (start_hue + blend_ratio * counter_vec) % 1.0
        point_saturation = start_saturation + blend_ratio * (end_saturation - start_saturation)
        point_value = start_value + blend_ratio * (end_value - start_value)
        return point_hue, point_saturation, point_value
    return inner

screaming_gradient = gradient(
    {
        0.00: tyrian_purple,
        0.20: tyrian_purple,
        0.40: bright_pink,
        0.60: bright_pink,
        0.80: neon_cyan,
        1.00: neon_cyan,
    }
)

rainbow_gradient = gradient(
    {
        0.00: red,
        0.33: green,
        0.66: blue,
        1.00: red,
    }
)

debug_gradient = gradient({1.00: red, 0.0: blue})
