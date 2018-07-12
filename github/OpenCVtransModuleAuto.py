import cv2
import numpy as np
import pytesser as pt
import webscrapingpath2url as ws
from PIL import Image, ImageDraw, ImageFont

def slopeAndIntercept(textRange):
    slope0 = (textRange[0][1] - textRange[1][1]) / float(textRange[0][0]
                                                         - textRange[1][0])
    slope1 = (textRange[2][1] - textRange[1][1]) / float(textRange[2][0]
                                                         - textRange[1][0])
    intercept0 = textRange[0][1] - textRange[0][0] * slope0
    intercept1 = textRange[1][1] - textRange[1][0] * slope1
    intercept2 = textRange[2][1] - textRange[2][0] * slope0
    intercept3 = textRange[3][1] - textRange[3][0] * slope1
    return [(slope0, slope1), (intercept0, intercept1, intercept2, intercept3)]

# examine whether the pixel is within the board boundary
def inBoundary(textRange, i, j, slope0, slope1, intercept0, intercept1,
               intercept2, intercept3):
    # calculate the limitation of j given i
    yLimitmax0 = max(i * slope0 + intercept0, i * slope0 + intercept2)
    yLimitmin0 = min(i * slope0 + intercept0, i * slope0 + intercept2)
    yLimitmax1 = max(i * slope1 + intercept1, i * slope1 + intercept3)
    yLimitmin1 = min(i * slope1 + intercept1, i * slope1 + intercept3)
    if (yLimitmin0 <= j <= yLimitmax0 and yLimitmin1 <= j <= yLimitmax1):
        return True
    return False

# mapping the possibly rotated image into a horizontally placed image
# so that translation module can recognize the characters and translate
def mapping2Horizontal(textRange, i, j, slope0, slope1, intercept0, intercept1,
                       intercept2, intercept3):
    # (0,0) in the Horizontal image should be textRange[0], all I need to
    # do is find the distance to the real x axis and y axis
    newi = int((abs(slope1 * i - j + intercept3) / (slope1 ** 2 + (-1) ** 2) ** 0.5))
    newj = int((abs(slope0 * i - j + intercept0) / (slope0 ** 2 + (-1) ** 2) ** 0.5))
    return newi, newj

# since houghcircle gives the coords of the center of the circle, we still
# need to eiminate a quarter of the landmark so that our word recognition
# module can work properly
def eliminateLandmark(textRange, radius):
    x0, y0 = textRange[0]
    x1, y1 = textRange[1]
    x2, y2 = textRange[2]
    x3, y3 = textRange[3]
    safeMargin = 5 # 5 pixel safety margin
    r = int(radius) + safeMargin
    diag02 = ((x2 - x0) ** 2 + (y2 - y0) ** 2) ** 0.5
    diag13 = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5
    x0n, y0n = (x2 - x0) * r / diag02 + x0, (y2 - y0) * r / diag02 + y0
    x1n, y1n = (x3 - x1) * r / diag13 + x1, (y3 - y1) * r / diag13 + y1
    x2n, y2n = (x0 - x2) * r / diag02 + x2, (y0 - y2) * r / diag02 + y2
    x3n, y3n = (x1 - x3) * r / diag13 + x3, (y1 - y3) * r / diag13 + y3
    width = int(((x1n - x0n) ** 2 + (y1n - y0n) ** 2) ** 0.5)
    height =int(((x1n - x2n) ** 2 + (y1n - y2n) ** 2) ** 0.5)
    return [(x0n, y0n), (x1n, y1n), (x2n, y2n), (x3n, y3n)], width, height

def run(frame, TL, SL):
    flag = False
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ##cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.GaussianBlur(img, (9,9), 0)
    circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT,1, 20)
##    cv2.imshow("greyed", img)
    if circles != None:
        circles = np.uint16(np.around(circles))
        print circles, len(circles[0,:]), type(circles)
        if len(circles[0,:]) == 3:# all three circles detected
            textRange = [(None, None), (None, None), (None, None), (None, None)]
            for i in circles[0,:]:
                # loop through the three circles to find what color it is
                circleFill = frame[i[1]][i[0]] # [B, G, R]
                # now check the color
                if (circleFill[0] == max(circleFill)): # blue
                    textRange[2] = int(i[1]), int(i[0])
                elif (circleFill[1] == max(circleFill)): # green
                    textRange[1] = int(i[1]), int(i[0])
                elif (circleFill[2] == max(circleFill)): # red
                    textRange[0] = int(i[1]), int(i[0])
            if (None, None) not in textRange[0:3]:
                textRange[3] = (textRange[0][0]-textRange[1][0]+textRange[2][0],
                                textRange[0][1]-textRange[1][1]+textRange[2][1])
            print textRange
            # eliminate landmark (circles) so that text recognition module would
            # not be confused by those dark chunks
            eliminate = eliminateLandmark(textRange, circles[0,:][0][2])
            textRange = eliminate[0]
##            print 'after eliminate landmark: ',textRange
            width, height = eliminate[1], eliminate[2]
            slope0, slope1 = slopeAndIntercept(textRange)[0]
            (intercept0, intercept1,
             intercept2, intercept3) = slopeAndIntercept(textRange)[1]
            empty = np.zeros((height + 1, width + 1, 3))# create an empty array
            empty.fill(255) # make pixels all white
            d = dict()
            # Now we have the corner coords of our text board
            # boundary function slope * i + intercept = j
            # test if it's within the board
            for i in xrange(len(img[0])):
                for j in xrange(len(img)):
                    if (inBoundary(textRange, i, j, slope0, slope1, intercept0,
                                   intercept1, intercept2, intercept3)):
                        # map it to the horizontal image
                        newi, newj = mapping2Horizontal(textRange, i, j, slope0,
                                                        slope1, intercept0,
                                                        intercept1, intercept2,
                                                        intercept3)
                        d[(newi, newj)] = (i, j)
                        empty[newj][newi] = frame[i][j] # save the new coords
                        frame[i][j].fill(255)# erase the original photo
            cv2.imwrite('empty.jpg', empty)
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
        try:
            text = pt.run('empty.jpg')
            result = ws.transmodule(text.strip(), TL, SL)
            multi = result.split('\n')
            template = Image.new("RGB", (int(width)+1, int(height)+1), "white")
            draw = ImageDraw.Draw(template)
            font = ImageFont.truetype("arial.ttf", 24)
            for line in xrange(len(multi)):
                draw.text((0, height/len(multi)*(line)),multi[line],(0,0,0),font=font)
                CVtemp = np.array(template)
                CVtemp = CVtemp[:,:,::-1].copy()
            flag = True
            # stick it back
            for newi in xrange(len(CVtemp[0])):
                for newj in xrange(len(CVtemp)):
                    if (newi, newj) not in d:
                        if (newi+1, newj+1) in d:
                            print newi + 1, newj + 1
                            frame[d[(newi+1, newj+1)][0]][d[(newi+1, newj+1)][1]] = CVtemp[newj][newi]
                            continue
                        elif (newi, newj+1) in d:
                            frame[d[(newi, newj+1)][0]][d[(newi, newj+1)][1]] = CVtemp[newj][newi]
                            continue
                    else:
                        frame[d[(newi, newj)][0]][d[(newi, newj)][1]] = CVtemp[newj][newi]
##            cv2.imwrite('success.jpg', frame)
        except: pass
    return frame, flag

