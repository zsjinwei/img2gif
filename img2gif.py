#!/bin/sh/env python3
# -*- coding: utf-8 -*-
'''
Created on 2018-11-22
@author: Huang Jinwei
'''
import imageio
import os
import cv2 as cv
import numpy as np

def getImgFileList(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
          for file in files:
              if os.path.splitext(file)[1] == '.jpg':
                   L.append(os.path.join(root, file))
    return L

def mergeFramesToGif(frames):
    pass

if __name__ == '__main__':
    outGifFileName = "./out/out.gif"
    imgFiles = getImgFileList("./images")
    # print(imgFiles)

    #frames = []  
    #for image_name in imgFiles:  
    #    frames.append(imageio.imread(image_name))

    # 提取模板
    # 定位模板位置百分比参数
    sXp = 0.29  # 左上角X坐标位置百分比
    sYp = 0.27  # 左上角Y坐标位置百分比
    Wp = 0.07   # 宽度百分比
    Hp = 0.1    # 高度百分比
    tplSource = cv.imread("./images/1.jpg")
    tplSize = tplSource.shape
    sX = int(tplSize[0] * sXp)
    sY = int(tplSize[1] * sYp)
    tX = int(sX + tplSize[0] * Wp)
    tY = int(sY + tplSize[1] * Hp)

    # 显示模板框
    #cv.namedWindow('template image', cv.WINDOW_NORMAL)
    #cv.rectangle(tplSource, (sX, sY), (tX, tY), (0, 0, 255), 2)
    #cv.imshow("template image", tplSource)

    tpl = tplSource[sY:tY,sX:tX]
    cv.imwrite('./out/tpl.jpg', tpl)
    
    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]   #3种模板匹配方法
    th, tw = tpl.shape[:2]

    for image_name in imgFiles:  
        target = cv.imread(image_name)

        md = methods[2] # 选择匹配方法

        result = cv.matchTemplate(target, tpl, md)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0]+tw, tl[1]+th)   #br是矩形右下角的点的坐标
        cv.rectangle(target, tl, br, (0, 0, 255), 2)
        cv.namedWindow("match-" + image_name, cv.WINDOW_NORMAL)
        cv.imshow("match-" + image_name, target)

    cv.waitKey(0)
    cv.destroyAllWindows()
    # Save them as frames into a gif   
    # imageio.mimsave(outGifFileName, frames, 'GIF', duration = 0.8) 

