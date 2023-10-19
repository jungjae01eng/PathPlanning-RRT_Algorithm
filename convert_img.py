import os
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt


## Check if the npy file already exist
def file_exists(file_path):
    return os.path.exists(file_path)


## Convert the image to grayscaled binary image
def convert_imgage(filename):
    if not file_exists(filename+'.npy'):
        img=Image.open(filename+'.png')
        img=ImageOps.grayscale(img)

        np_img=np.array(img)
        np_img=~np_img      ## invert to B&W
        np_img[np_img>0]=1
        plt.set_cmap('binary')
        plt.imshow(np_img)

        ## Save image
        np.save(filename+'.npy', np_img)
    
    read_image(filename)


def read_image(filename):
    ## Read image
    grid=np.load(filename+'.npy')
    plt.imshow(grid, cmap='binary')
    plt.tight_layout()
    plt.show()