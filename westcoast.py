#/usr/bin/pxthon3
# -*- coding: utf-8 -*-
import colorama
import math

from colorama import Fore
from random import randint

SEA=0
COAST=1
LAND=2
FRACTAL_MAX_HEIGHT = 0

def generate_coast_map(x_size, y_size, pcnt_water, pcnt_coast):
    coast_start = int(x_size * pcnt_water)
    coast_end = int(x_size * (pcnt_water + pcnt_coast))
    step = 1 / (coast_end - coast_start)
    current_step = step
    coast_map = []

    # Fill map
    for x in range(0,x_size):
        coast_map.append([])
        item = 0
        if x > coast_end:
            item = LAND
        elif x > coast_start:
            item = 0.0 + current_step
            current_step += step
        else:
            item = SEA
        for y in range(0,y_size):
            coast_map[x].append(item)
    return coast_map

def generate_fractal_map(x_size, y_size, octaves, cutoff):
    """
    Takes boundries (x_size, y_size) for the noise, and the number of octaves
    to generate.

    Returns a two-dimensional matrix.
    """
    # Get a zeroed map to begin with
    fractal_map = initialize_map(x_size, y_size)

    # Get a fractal map
    height = add_octaves(fractal_map, octaves)
    print("Max height: " + str(height))
    print("Cutoff amount: " + str(cutoff))
    print("Cutoff: " + str(height * cutoff))

    # Cut map down
    cutoff_map(fractal_map, height * cutoff)

    return fractal_map

def initialize_map(x_size, y_size):
    """
    Returns an map full of 0's
    """
    fractal_map = []

    # Fill map with 0's
    for x in range(0,x_size):
        fractal_map.append([])
        for y in range(0,y_size):
            fractal_map[x].append(0)
    return fractal_map

def add_octaves(fractal_map, octaves):
    """
    Recursively adds octaves to the fractal
    """
    step = int(math.pow(2,(octaves - 1)))
    scale = step
    current_height = FRACTAL_MAX_HEIGHT + scale
    for x in range(0, len(fractal_map), step):
        for y in range(0, len(fractal_map[x]), step):
            # Add random values
            fractal_map[x][y] += fractal_map[x][y] + randint(0,scale)

            # If we aren't on the last octave, interpolate values
            if step > 1:
                if x > 1:
                    val = (fractal_map[x][y - step] + fractal_map[x][y]) / 2
                    fractal_map[int(x - step / 2)][y] = val
                if y > 1:
                    val = (fractal_map[x - step][y] + fractal_map[x][y]) / 2
                    fractal_map[int(x - step / 2)][y] = val
                if x > 1 and y > 1:
                    tmp1 = fractal_map[x - step][int(y - step / 2)]
                    tmp2 = fractal_map[x][int(y - step / 2)]
                    val = (tmp1 + tmp2) / 2
                    fractal_map[int(x - step / 2)][int(y - step / 2)] = val
    if octaves > 1:
        add_octaves(fractal_map, octaves-1)
    return current_height

def interpolate_maps(fractal_map, base_map):
    base_width = len(base_map)
    base_height = len(base_map[0])
    new_map = []
    for x in range(base_width):
        new_map.append([])
        for y in range(base_height):
            item = base_map[x][y]
            if type(item) is float and fractal_map[x][y] == 1:
                floor = math.floor(item)
                ceil = math.ceil(item)
                item_pcnt = int(100 * (item % 1))
                rnd_pcnt = randint(1, 100 + 1)
                if y == 1:
                    print("floor=" + str(floor))
                    print("ceil=" + str(ceil))
                    print("item_pcnt=" + str(item_pcnt))
                    print("rnd_pct=" + str(rnd_pct))
                if item_pcnt > rnd_pcnt:
                    new_map[x].append(ceil)
                else:
                    new_map[x].append(floor)
            else:
                new_map[x].append(item)
    return new_map


def cutoff_map(map, cutoff, lower=0, upper=1):
    for x in range(0,len(map)):
        for y in range(0,len(map[x])):
            if map[x][y] > cutoff:
                map[x][y] = upper
            else:
                map[x][y] = lower

def print_map(map):
    colorama.init()
    map_string = ""
    for y in range(0,len(map)):
        row = ""
        for x in range(0, len(map[y])):
            item = map[x][y]
            if item == SEA:
                row += Fore.BLUE + "～"
            elif item > SEA and item < LAND:
                row += Fore.YELLOW + "＃"
            elif item == LAND:
                row += Fore.GREEN + "＝"
        map_string += row + "\n"
    print(map_string)
    colorama.deinit()

def main():
    Y_SIZE=126
    X_SIZE=126
    OCTAVES=8
    CUTOFF=.05
    PCNT_WATER=.1
    PCNT_COAST=.25
    base_map = generate_coast_map(X_SIZE, Y_SIZE, PCNT_WATER, PCNT_COAST)
    fractal_map = generate_fractal_map(X_SIZE, Y_SIZE, OCTAVES, CUTOFF)
    new_map = interpolate_maps(fractal_map, base_map)
    print_map(new_map)

if __name__ == "__main__":
    main()
