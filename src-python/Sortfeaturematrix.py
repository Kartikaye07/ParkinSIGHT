# -*- coding: utf-8 -*-
"""SortFeatureMatrix.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dr3pKuma4XhKEKb92_AyTn541QR-_niL
"""

import random
import math

def get_polar_angle(point):
    x, y = point
    return math.atan2(-y, x) % (2 * math.pi)separate

def sort_points_clockwise(points):
    # Find the starting point in the 3rd quadrant
    start_point = points[0]
    # Rearrange the points list starting from the 3rd quadrant point
    start_index = points.index(start_point)
    ordered_points = points[start_index:] + points[:start_index]

    center_x = sum(point[0] for point in ordered_points) / len(ordered_points)
    center_y = sum(point[1] for point in ordered_points) / len(ordered_points)
    center_point = (center_x, center_y)

    sorted_points = sorted(ordered_points, key=lambda point: get_polar_angle((point[0] - center_point[0], point[1] - center_point[1])))

    return sorted_points

import pandas as pd
import numpy as np

df = pd.read_csv('/content/fm_pd_and_swedd_v3.csv')

df = df[['Patient_No', 'Point1_x', 'Point1_y', 'Point2_x',
       'Point2_y', 'Point3_x', 'Point3_y', 'Point4_x', 'Point4_y',
       'Point5_x', 'Point5_y', 'Point6_x', 'Point6_y', 'Point7_x',
       'Point7_y', 'Point8_x', 'Point8_y', 'Point9_x', 'Point9_y',
       'Point10_x', 'Point10_y', 'Point11_x', 'Point11_y', 'Point12_x',
       'Point12_y', 'Class']]

df

# CHECKING 0 MEAN OR NOT

l = df.iloc[0].values

sumx = 0
sumy = 0

for i in range(1, 13):
  if(i%2==0):
    sumx+=l[i]
  else:
    sumy+=l[i]

sumy

for it in range(len(df)):
    l = df.iloc[it].values

    # Creating a new list to store the modified row
    new_l = [l[0]]

    part1 = l[1:13]
    left = []

    # Iterating over the range from 0 to 6 (exclusive) and Each iteration processes two consecutive elements
    i = 0
    for idx in range(6):
        # Appending pairs of points to 'left'
        left.append((part1[i], part1[i+1]))
        i += 2

    left_y_anti = sort_points_clockwise(left)

    low = 1000
    for i in left_y_anti:
        low = min(low, i[0])

    # Reordering 'left_y_anti' so that the point with the minimum y-coordinate is first
    while(left_y_anti[0][0] != low):
        left_y_anti = left_y_anti[-1:] + left_y_anti[:-1]

    # Creating a new list to store the sorted values of 'part1'
    part1_sorted = []
    for i in left_y_anti:
        part1_sorted.append(i[0])
        part1_sorted.append(i[1])

    # Extracting the second part of the row from index 13 to 24
    part2 = l[13:25]
    right = []

    i = 0
    for idx in range(6):
        right.append((part2[i], part2[i+1]))
        i += 2

    right_y_anti = sort_points_clockwise(right)

    low = 1000
    for i in right_y_anti:
        low = min(low, i[0])

    while(right_y_anti[0][0] != low):
        right_y_anti = right_y_anti[-1:] + right_y_anti[:-1]

    # Creating a new list to store the sorted values of 'part2'
    part2_sorted = []
    for i in right_y_anti:
        part2_sorted.append(i[0])
        part2_sorted.append(i[1])

    # Extracting the third part of the row at index 25
    part3 = [l[25]]

    new_l = new_l + part1_sorted + part2_sorted + part3

    # Updating the current row in the DataFrame with the modified row
    df.loc[it] = new_l



"""# Visualize it"""

import matplotlib.pyplot as plt

# Choose what points to visualize
idx = 0
# The values of the row 'idx' from columns 1 to 12 are extracted
points = df.iloc[idx].tolist()[1:13]

# 'left' will store pairs of points
left = []

# Iterating over the range from 0 to 6 (exclusive) & Each iteration processes two consecutive points
i = 0
for idx in range(6):
    # Extracting two consecutive points and appending them to 'left' as a tuple
    left.append((points[i], points[i+1]))
    i += 2

plt.figure()

# Extracting x-coordinates (xs) and y-coordinates (ys) from 'left'
xs, ys = zip(*left)

# Plotting a line connecting the points in 'left'
plt.plot(xs, ys)

# Adding a scatter plot marker for the first point in 'left'
plt.scatter(xs[0], ys[0])

plt.show()