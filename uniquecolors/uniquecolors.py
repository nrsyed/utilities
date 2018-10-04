import colorsys
import numpy as np

def getUniqueColors(num_colors, max=1.0, color_space="rgb", type="float"):
    """
    Return a generator of unique colors.

    @param num_colors (int): Number (>0) of unique colors to return.
    @param max (float): Maximum value of color parameters (default 1.0).
    @param color_space (str): "rgb" (default), "hsv", "hls"
    @param type (str): "float" (default), "int"
    @return color (tuple): 3-tuple containing the three color values for the
        desired color space and scaled to a maximum value of @param max.
    """

    # Use HSV color space to generate unique colors.
    for H in np.linspace(0, 1, num_colors, endpoint=False):
        color = (H, 1.0, 1.0)
        if color_space == "rgb":
            color = colorsys.hsv_to_rgb(*color)
        elif color_space == "hls":
            color = colorsys.hsv_to_hls(*color)

        color = tuple([int(round(max * val)) if type == "int"
            else (max * val) for val in color])

        yield color
