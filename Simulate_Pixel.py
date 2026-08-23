from PIL import Image
from math import floor
import numpy as np
import os

os.system(" ")

file_types = ("png","jpeg","jpg")
file_list = os.listdir(".")
file_list = [file for file in file_list if file.split(".")[-1] in file_types]

[print(f"{number}: {file_name}") for number,file_name in enumerate(file_list)]
j = input("choose an image:")
filename = file_list[int(j)]


img = Image.open(filename)


height = img.size[0]
width = img.size[1]
img = [[img.getpixel((x,y)) for x in range(width)]for y in range(height)]

new_img = []
for line in img:
    new_line = []
    for value in line:
        
        r = [value[0],0,0]
        g = [0,value[1],0]
        b = [0,0,value[2]]
        
        new_line.append(r)
        new_line.append(g)
        new_line.append(b)
    [new_img.append(new_line) for f in range(3)]
    

def save_from_matrix(matrix,nome):
    
    matrix = np.array(matrix)
    matrix = Image.fromarray(matrix.astype(np.uint8))
    matrix.save(f"{nome}")

save_from_matrix(new_img, f"{filename.split(".")[0]} simulated_pixel.png")
