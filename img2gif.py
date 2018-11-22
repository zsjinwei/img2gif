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

def getTpl(imgPath, sXp, sYp, Wp, Hp):
    tplSource = cv.imread(imgPath)
    tplSize = tplSource.shape
    sX = int(tplSize[0] * sXp)
    sY = int(tplSize[1] * sYp)
    tX = int(sX + tplSize[0] * Wp)
    tY = int(sY + tplSize[1] * Hp)

    # 显示模板框
    #cv.namedWindow('template image', cv.WINDOW_NORMAL)
    #cv.rectangle(tplSource, (sX, sY), (tX, tY), (0, 0, 255), 2)
    #cv.imshow(imgPath, tplSource)

    tpl = tplSource[sY:tY,sX:tX]
    return tpl

def matchTpl(target, tpl):
    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]   #3种模板匹配方法
    md = methods[2] # 选择匹配方法

    th, tw = tpl.shape[:2]

    result = cv.matchTemplate(target, tpl, md)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if md == cv.TM_SQDIFF_NORMED:
        tl = min_loc
    else:
        tl = max_loc
    
    br = (tl[0]+tw, tl[1]+th)   #br是矩形右下角的点的坐标
    
    # 记录图像宽高和匹配坐标中心点
    cpX = int(tl[0]+tw/2)
    cpY = int(tl[1]+th/2)

    return cpX, cpY, tl, br

if __name__ == '__main__':
    outGifFileName = "./out/out.gif"
    imgFiles = getImgFileList("./images")
    imgFiles.sort()
    # print(imgFiles)

    # 提取模板
    # 定位模板位置百分比参数
    sXp = 0.25  # 左上角X坐标位置百分比
    sYp = 0.06  # 左上角Y坐标位置百分比
    Wp = 0.11   # 宽度百分比
    Hp = 0.1    # 高度百分比
    tpl = getTpl("./images/6.jpg", sXp, sYp, Wp, Hp)

    cv.imwrite('./out/tpl.jpg', tpl)

    # 提取另一个模板, 用于计算缩放/旋转系数
    tpl2 = getTpl("./images/6.jpg", 0.285, 0.49, 0.040, 0.062)
    #tpl2 = getTpl("./images/6.jpg", 0.70, 0.68, 0.045, 0.08)

    cv.imwrite('./out/tp2.jpg', tpl2)
    #exit()
    cpMap = {}

    # 匹配模板并获取模板匹配中心坐标
    for imageName in imgFiles:  
        target = cv.imread(imageName)
        targetH, targetW = target.shape[:2]

        cpX, cpY, tl, br = matchTpl(target, tpl)
        cpX2, cpY2, tl2, br2 = matchTpl(target, tpl2)

        cpMap[imageName] = [targetW, targetH, cpX, cpY, cpX2, cpY2]

        cv.rectangle(target, tl, br, (0, 0, 255), 4)
        cv.rectangle(target, tl2, br2, (0, 255, 255), 4)
        cv.namedWindow("match-" + imageName, cv.WINDOW_NORMAL)
        cv.imshow("match-" + imageName, target)
    #print(cpMap)

    minTopSize = float("inf")
    minBottomSize = float("inf")
    minLeftSize = float("inf")
    minRightSize = float("inf")
    
    for key, item in cpMap.items():
        #print(item)
        if item[2] < minLeftSize:
            minLeftSize = int(item[2])

        if (item[0] - item[2]) < minRightSize:
            minRightSize = int(item[0] - item[2])

        if item[3] < minTopSize:
            minTopSize = int(item[3])

        if (item[1] - item[3]) < minBottomSize:
            minBottomSize = int(item[1] - item[3])
    

    # 裁剪图片, 生成gif
    frames = []  
    for img, item in cpMap.items():
        currentImg= imageio.imread(img)

        print(minLeftSize, minRightSize, minTopSize, minBottomSize, item[0], item[1], item[2], item[3])

        stripImg = currentImg[int(item[3] - minTopSize):int(item[3] + minBottomSize), int(item[2] - minLeftSize):int(item[2] + minRightSize)]
        frames.append(stripImg)

        #tt = cv.imread(img)
        #cv.rectangle(tt, (int(item[2] - minLeftSize), int(item[3] - minTopSize)), (int(item[2] + minRightSize), int(item[3] + minBottomSize)), (0, 0, 255), 2)
        #cv.namedWindow("match-" + img, cv.WINDOW_NORMAL)
        #cv.imshow("match-" + img, tt)

    # Save them as frames into a gif   
    imageio.mimsave(outGifFileName, frames, 'GIF', duration = 0.4)

    #cv.waitKey(0)
    cv.destroyAllWindows()

