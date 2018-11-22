#!/bin/sh/env python3
# -*- coding: utf-8 -*-
'''
Created on 2018-11-22
@author: Huang Jinwei
'''
import imageio
import os

def getImgFileList(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
          for file in files:
              if os.path.splitext(file)[1] == '.jpg':
                   L.append(os.path.join(root, file))
    return L

if __name__ == '__main__':
    outGifFileName = "./out/out.gif"
    imgFiles = getImgFileList("./images")
    print(imgFiles)

    frames = []  
    for image_name in imgFiles:  
        frames.append(imageio.imread(image_name))

    # Save them as frames into a gif   
    imageio.mimsave(outGifFileName, frames, 'GIF', duration = 0.8) 

