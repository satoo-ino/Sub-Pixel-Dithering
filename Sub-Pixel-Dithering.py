from PIL import Image
from math import floor
import numpy as np
import os

os.system(" ")
steps = 1
brightness = -0.5
bayer = 8 #2 4 8 or 16


def encode_srgb(value):
    if value <= 0.04045:
        value = value / 12.92
    else:
        value = ((value + 0.055) / 1.055) ** 2.4
    return value

def decode_srgb(value):
    if value <= 0.0031308:
        value = value * 12.92
    else:
        value = 1.055 * (value ** (1/2.4)) - 0.055
    return value

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

bayer2 = [[0, 2],
[3, 1]]

bayer4 = [[0, 8, 2, 10],
[12, 4, 14, 6],
[3, 11, 1, 9],
[15, 7, 13, 5]]

bayer8 = [[0, 32, 8, 40, 2, 34, 10, 42],
[48, 16, 56, 24, 50, 18, 58, 26],
[12, 44, 4, 36, 14, 46, 6, 38],
[60, 28, 52, 20, 62, 30, 54, 22],
[3, 35, 11, 43, 1, 33, 9, 41],
[51, 19, 59, 27, 49, 17, 57, 25], 
[15, 47, 7, 39, 13, 45, 5, 37],
[63, 31, 55, 23, 61, 29, 53, 21]]

bayer16 = [[0, 128, 32, 160, 8, 136, 40, 168, 2, 130, 34, 162, 10, 138, 42, 170],
[192, 64, 224, 96, 200, 72, 232, 104, 194, 66, 226, 98, 202, 74, 234, 106],
[48, 176, 16, 144, 56, 184, 24, 152, 50, 178, 18, 146, 58, 186, 26, 154],
[240, 112, 208, 80, 248, 120, 216, 88, 242, 114, 210, 82, 250, 122, 218, 90],
[12, 140, 44, 172, 4, 132, 36, 164, 14, 142, 46, 174, 6, 134, 38, 166],
[204, 76, 236, 108, 196, 68, 228, 100, 206, 78, 238, 110, 198, 70, 230, 102],
[60, 188, 28, 156, 52, 180, 20, 148, 62, 190, 30, 158, 54, 182, 22, 150],
[252, 124, 220, 92, 244, 116, 212, 84, 254, 126, 222, 94, 246, 118, 214, 86], 
[3, 131, 35, 163, 11, 139, 43, 171, 1, 129, 33, 161, 9, 137, 41, 169],
[195, 67, 227, 99, 203, 75, 235, 107, 193, 65, 225, 97, 201, 73, 233, 105],
[51, 179, 19, 147, 59, 187, 27, 155, 49, 177, 17, 145, 57, 185, 25, 153],
[243, 115, 211, 83, 251, 123, 219, 91, 241, 113, 209, 81, 249, 121, 217, 89],
[15, 143, 47, 175, 7, 135, 39, 167, 13, 141, 45, 173, 5, 133, 37, 165],
[207, 79, 239, 111, 199, 71, 231, 103, 205, 77, 237, 109, 197, 69, 229, 101],
[63, 191, 31, 159, 55, 183, 23, 151, 61, 189, 29, 157, 53, 181, 21, 149],
[255, 127, 223, 95, 247, 119, 215, 87, 253, 125, 221, 93, 245, 117, 213, 85]]




file_types = ("png","jpeg","jpg")

file_list = os.listdir(".")

file_list = [file for file in file_list if file.split(".")[-1] in file_types]



[print(f"{number}: {file_name}") for number,file_name in enumerate(file_list)]

print()
print("or press 'p' to open the options menu")
print()

while True:
    
    j = input("Choose an option: ").lower()
    
    if j == "p":
        while True:
            clear()
            print("OPTIONS:")
            print("1: change steps (default 1)")
            print("2: change bayer size (default 8 by 8)")
            
            k = input("Choose an option (or 'b' to go back): ").lower()
            
            match k:
                case "1":
                    while True:
                        try:
                            print()
                            print(f"old steps value: {steps}")
                            steps = int(input("new steps value: "))
                            break
                        except:
                            print("invalid value.")
            
                case "2":
                    while True:
                        try:
                            print()
                            print(f"old bayer value: {bayer} by {bayer}")
                            
                            print("1: 2 by 2")
                            print("2: 4 by 4")
                            print("3: 8 by 8")
                            print("4: 16 by 16")
                            
                            bayer = 2**int(input("new bayer value: "))
                            break
                        except:
                            print("invalid value.")
                
                case "b":
                    clear()
                    [print(f"{number}: {file_name}") for number,file_name in enumerate(file_list)]
                    print()
                    print("p: to open the options menu")
                    print()
                    break
            
        
    if j != "p":
        try:
            filename = file_list[int(j)] 
            break
        except:
            print("invalid option, choose an image by typing the corresponding number.")
            print()


clear()
print("----------------------------------------------------------------------------------------")
print(f"bayer: {bayer} / steps: {steps} / file: {filename}" )
print("----------------------------------------------------------------------------------------")


bayer = {2:bayer2, 4:bayer4, 8:bayer8, 16:bayer16}[bayer]

bayer = [[value+0.5 for value in row]for row in bayer] 
#removes the bias of the standard bayer matrix values
#(without this fix darker areas of the image gets much darker)


img = Image.open(filename)


height = img.size[0]
width = img.size[1]

print("(1/8)reading image")
img_matrix = [[img.getpixel((x,y)) for x in range(height)]for y in range(width)]
print("(2/8)separating rgb")
r_matrix = [[value[0] for value in line]for line in img_matrix] 
g_matrix = [[value[1] for value in line]for line in img_matrix] 
b_matrix = [[value[2] for value in line]for line in img_matrix] 
print("(3/8)applying shift to red and blue channel")
r_matrix = [[r_matrix[x][(y - 1) % len(img_matrix[0])] for y in range(len(img_matrix[0]))]for x in range(len(img_matrix))] 
b_matrix = [[b_matrix[x][(y + 1) % len(img_matrix[0])] for y in range(len(img_matrix[0]))]for x in range(len(img_matrix))] 

  



print("(4/8)downscaling and dithering red channel")

new_r = []
for x in range(0, width-1, 3):
    line = []
    for y in range(0, height-1, 3 ):
        raw_pixel = r_matrix[(x+1)%width][(y+1)%height] #sum([r_matrix[(x+a)%height][(y+b)%width] for a in range(3) for b in range(3)])/9)
        
        
        n_pixel = (raw_pixel/255)
        n_pixel = encode_srgb(n_pixel)
        
        n_bayer = bayer[int(x/3)%(len(bayer))][int(y/3) % len(bayer[0])]/(len(bayer)*len(bayer[0]))
 
        dithered_p = round(decode_srgb((floor((n_pixel*steps) + n_bayer))/steps)*255)
        
        line.append(dithered_p)
        
    new_r.append(line)

print("(5/8)downscaling and dithering green channel")
bayer = [[bayer[(x + 4) % len(bayer)][(y + 2) % len(bayer[0])] for y in range(len(bayer[0]))]for x in range(len(bayer))]

new_g = []
for x in range(0, width-1, 3):
    line = []
    for y in range(0, height-1, 3 ):
        raw_pixel = g_matrix[(x+1)%width][(y+1)%height] #sum([r_matrix[(x+a)%height][(y+b)%width] for a in range(3) for b in range(3)])/9)
        
        n_pixel = (raw_pixel/255)
        n_pixel = encode_srgb(n_pixel)
        
        n_bayer = bayer[int(x/3)%(len(bayer))][int(y/3) % len(bayer[0])]/(len(bayer)*len(bayer[0]))
        
        dithered_p = round(decode_srgb((floor((n_pixel*steps) + n_bayer))/steps)*255)
        
        line.append(dithered_p)
        
    new_g.append(line)

print("(6/8)downscaling and dithering blue channel")
bayer = [[bayer[(x - 4) % len(bayer)][(y + 2) % len(bayer[0])] for y in range(len(bayer[0]))]for x in range(len(bayer))]

new_b = []
for x in range(0, width-1, 3):
    line = []
    for y in range(0, height-1, 3 ):
        raw_pixel = b_matrix[(x+1)%width][(y+1)%height] #sum([r_matrix[(x+a)%height][(y+b)%width] for a in range(3) for b in range(3)])/9)
        
        n_pixel = (raw_pixel/255)
        n_pixel = encode_srgb(n_pixel)
        
        n_bayer = bayer[int(x/3)%(len(bayer))][int(y/3) % len(bayer[0])]/(len(bayer)*len(bayer[0]))
        
        dithered_p = round(decode_srgb((floor((n_pixel*steps) + n_bayer))/steps)*255)
        
        line.append(dithered_p)
       
    new_b.append(line)


print("(7/8)making the final image")
rgb_final = [[ (new_r[y][x],new_g[y][x],new_b[y][x]) for x in range(len(new_g[0]))]for y in range(len(new_g))]








    
print("(8/8)saving image")
def save_from_matrix(matrix,nome):
    
    matrix = np.array(matrix)
    matrix = Image.fromarray(matrix.astype(np.uint8))
    matrix.save(f"{nome}")

#save_from_matrix(r_matrix, "1r.png")
#save_from_matrix(g_matrix, "1g.png")
#save_from_matrix(b_matrix, "1b.png")
#save_from_matrix(new_r, "2r.png")
#save_from_matrix(new_b, "2b.png")
#save_from_matrix(new_g, "2g.png")
#save_from_matrix(img_matrix, "rgb.png")
save_from_matrix(rgb_final, f"{filename.split(".")[0]} processed.png")
input("image saved - enter to exit")
