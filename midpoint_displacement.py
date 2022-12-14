from math import cos, radians, sin
import os
import random
from PIL import Image, ImageDraw
import bisect

def interpolate(first_col, second_col, interval):
    det_co = [(t - f) / interval for f, t in zip(first_col, second_col)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(first_col, det_co)]

def midpoint_displacement(start, end, roughness, vertical_displacement = None, num_of_iterations = 16):

    if vertical_displacement is None:
        vertical_displacement = (start[1] + end[1]) / 2

    points = [start, end]
    iteration = 1

    while iteration <= num_of_iterations:
        points_tup = tuple(points)
        for i in range(len(points_tup) - 1):
            midpoint = list(
                map(lambda x: (points_tup[i][x] + points_tup[i + 1][x]) / 2, [0, 1])
            )
            midpoint[1] += random.choice(
                [-vertical_displacement, vertical_displacement]
            )

            bisect.insort(points, midpoint)

        vertical_displacement *= 2 ** (-roughness)
        iteration += 1

    return points

def draw_layers(layers, width, height, color_dict = None):
    if color_dict is None:
        color_dict = {
            '0': (246, 237, 205),   #white
            '1': (203, 129, 117),   #red
            '2': (226, 169, 126),   #orange
            '3': (240, 207, 142),   #yellow
            '4': (168, 200, 166),   #green
            '5': (109, 141, 138),   #blue
            '6': (101, 80, 87),  #brown
        }
    else:
        if len(color_dict) < len(layers) + 1:
            raise ValueError("Should have more colors than layers")

    gradient = Image.new('RGBA', (width, height), color = 0)
    gradient_draw = ImageDraw.Draw(gradient)

    second_col = (252, 66, 154)
    first_col = (252, 237, 112)

    for i, color in enumerate(interpolate(first_col, second_col, height)):
        gradient_draw.line([(0, i), (width, i)], tuple(color), width = 1)

    # (i, 0), (0, i) - from top left to bottom right
    # (0, i), (width, i) - from top to bottom
    # (i, width), (i, 0) - left to right

    angle = random.randint(-180, 0)
    radius = width / 2

    # circle radius * angle in radians then offset by
    # radius (x coordinate of circle center)
    # height (y coordinate of circle center)
    sun_pos_x = radius * cos(radians(angle)) + radius
    sun_pos_y = radius * sin(radians(angle)) + height

    gradient_draw.ellipse((sun_pos_x, sun_pos_y, sun_pos_x + 50, sun_pos_y + 50), fill = (255, 255, 255, 255))

    final_layers = []

    for layer in layers:
        sampled_layer = []

        for i in range(len(layer) - 1):
            sampled_layer += [layer[i]]
            if layer[i + 1][0] - layer[i][0] > 1:
                m = float(layer[i + 1][1] - layer[i][1]) / (layer[i + 1][0] - layer[i][0])
                n = layer[i][1] - m * layer[i][0]
                r = lambda x: m * x + n

                for j in range(int(layer[i][0] + 1), int(layer[i + 1][0])):
                    sampled_layer += [[j, r(j)]]

        final_layers += [sampled_layer]

    final_layers_enum = enumerate(final_layers)

    for final_layer in final_layers_enum:
        for x in range(len(final_layer[1]) - 1):
            gradient_draw.line((final_layer[1][x][0], height - final_layer[1][x][1], final_layer[1][x][0], height), color_dict[str(final_layer[0])])

    return gradient

def main():
    width = 1920
    height = 1080

    # start point[left-right, top-bottom] , end point[left-right, top-bottom] , roughness, displacement, iterations
    layer_1 = midpoint_displacement([0, random.randint(0, 130)], [width, random.randrange(0, 200)], 1.1, 80, 11)
    layer_2 = midpoint_displacement([0, random.randint(140, 200)], [width, random.randint(50, 200)], 1.2, 70, 12)
    layer_3 = midpoint_displacement([0, random.randint(250, 280)], [width, random.randint(200, 230)], 1, 120, 9)
    layer_4 = midpoint_displacement([0, random.randint(320, 350)], [width, random.randint(290, 350)], 0.9, 160, 10)
    # layer_5 = midpoint_displacement([0, random.randint(350, 400)], [width, random.randint(330, 370)], 1, 150, 9)

    # landscape = draw_layers(
    #     [], width, height
    # )

    landscape = draw_layers(
        [layer_4, layer_3, layer_2, layer_1], width, height
    )

    landscape.save(os.getcwd() + '\\testing.png')

if __name__ == "__main__":
    main()