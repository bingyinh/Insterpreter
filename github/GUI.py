# eventBasedAnimation is from 112 course notes
import eventBasedAnimation
import math
import Tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
import OpenCVtransModuleAuto as OCVa
import OpenCVtransModuleManual as OCVm

# rgbString comes from 112 course notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class Insterpreter(eventBasedAnimation.Animation):
    def onInit(self):
        # init the settings.txt file
        with open('settings.txt','wt') as f:
            f.write('0,0')
        self.windowTitle = "Insterpreter"
        self.Pages = [MainMenu(), Option(), Instruction(), Translation()]
        self.currentPage = 0
    def onMouse(self, event):
        # depends on the page that user is browsing, trigger the mouse function
        self.Pages[self.currentPage].Mouse(event.x, event.y)
        if (self.currentPage == 0):
            if (450 <= event.x <= 750 and 130 <= event.y <= 170):
                self.currentPage = 3 # "Translation"
            elif (120 <= event.x <= 280 and 480 <= event.y <= 520):
                self.currentPage = 1 # "Option"
            elif (450 <= event.x <= 750 and 480 <= event.y <= 520):
                self.currentPage = 2 # "Instruction"
        # if click on Back, always switch back to MainMenu
        if (670 <= event.x <= 790 and 550 <= event.y <= 590):
            self.currentPage = 0
        
        
    def onDraw(self, canvas):
        # depends on the page that user is browsing, trigger the mouse function
        self.Pages[self.currentPage].Draw(canvas, self.step)
    def onQuit(self):
        cv2.VideoCapture(0).release() # turn off the webcam when quitting

class Page(object):
    def __init__(self):
        self.bgc = rgbString(12, 20, 31) # background color
        self.btnColor = rgbString(111, 195, 223) # color theme of Tron Legacy
        self.btnShading1 = rgbString(66, 176, 213) # color theme of Tron Legacy
        self.btnShading2 = rgbString(31, 113, 139) # color theme of Tron Legacy
        self.btnShading3 = rgbString(16, 60, 73) # color theme of Tron Legacy
        self.btnActive = rgbString(230, 255, 255)# color theme of Tron Legacy
        self.sourceLang = ['auto', 'en', 'es', 'de', 'fr', 'nl']
        self.targetLang = ['zh-CN', 'zh-TW', 'ru', 'hi', 'ja',
                           'ko', 'en', 'es', 'de', 'fr', 'nl']
        self.readOptions()
        self.counter = -1
    # method for text drawing
    def drawText(self, canvas):
        for piece in self.textInPage:
            text, font, posx, posy = piece[0], piece[1], piece[2], piece[3]
            if (piece[4] == True): # change color when mouse moves onto button
                canvas.create_text(posx, posy, text = text,
                                   fill = self.btnColor,
                                   font = "Tron " + str(font),
                                   activefill = self.btnActive)
            else: # static color when mouse moves onto non-button text
                canvas.create_text(posx, posy, text = text,
                                   fill = self.btnColor,
                                   font = "Tron " + str(font), width = 650)
    def Draw(self, canvas, step):
        canvas.create_rectangle(-10, -10, 810, 610, fill = self.bgc)
        self.drawText(canvas)
    def Mouse(self, mouseX, mouseY):
        pass
    def roundedCorner(self, canvas, x0, y0, x1, y1):
        r = abs(x0 - x1)
        deg = 10. / 180 * math.pi
        if (x0 < x1 and y0 > y1): # bottom left to top right
            for i in xrange(9): # draw a line every 10 degree
                self.drawShading(canvas, x0 + r - math.cos(deg * i) * r,
                                   y0 - math.sin(deg * i) * r ,
                                   x0 + r - math.cos(deg * (i + 1)) * r,
                                   y0 - math.sin(deg * (i + 1)) * r)
                canvas.create_line(x0 + r - math.cos(deg * i) * r,
                                   y0 - math.sin(deg * i) * r ,
                                   x0 + r - math.cos(deg * (i + 1)) * r,
                                   y0 - math.sin(deg * (i + 1)) * r,
                                   fill = self.btnColor, width = 4)
        elif (x0 < x1 and y0 < y1): # top left to bottom right
            for i in xrange(9):
                self.drawShading(canvas, x0 + r - math.cos(deg * i) * r,
                                   y0 + math.sin(deg * i) * r ,
                                   x0 + r - math.cos(deg * (i + 1)) * r,
                                   y0 + math.sin(deg * (i + 1)) * r)
                canvas.create_line(x0 + r - math.cos(deg * i) * r,
                                   y0 + math.sin(deg * i) * r ,
                                   x0 + r - math.cos(deg * (i + 1)) * r,
                                   y0 + math.sin(deg * (i + 1)) * r,
                                   fill = self.btnColor, width = 4)
        elif (x0 > x1 and y0 > y1): # bottom right to top left
            for i in xrange(9):
                self.drawShading(canvas, x0 - r + math.cos(deg * i) * r,
                                   y0 - math.sin(deg * i) * r ,
                                   x0 - r + math.cos(deg * (i + 1)) * r,
                                   y0 - math.sin(deg * (i + 1)) * r)
                canvas.create_line(x0 - r + math.cos(deg * i) * r,
                                   y0 - math.sin(deg * i) * r ,
                                   x0 - r + math.cos(deg * (i + 1)) * r,
                                   y0 - math.sin(deg * (i + 1)) * r,
                                   fill = self.btnColor, width = 4)
        elif (x0 > x1 and y0 < y1): # top right to bottom left
            for i in xrange(9):
                self.drawShading(canvas, x0 - r + math.cos(deg * i) * r,
                                   y0 + math.sin(deg * i) * r ,
                                   x0 - r + math.cos(deg * (i + 1)) * r,
                                   y0 + math.sin(deg * (i + 1)) * r)
                canvas.create_line(x0 - r + math.cos(deg * i) * r,
                                   y0 + math.sin(deg * i) * r ,
                                   x0 - r + math.cos(deg * (i + 1)) * r,
                                   y0 + math.sin(deg * (i + 1)) * r,
                                   fill = self.btnColor, width = 4)
    # use stipple to mimic semi-transparency, get idea from 112 course notes
    def drawShading(self, canvas, x0, y0, x1, y1):
        canvas.create_line(x0, y0, x1, y1, fill = self.btnShading1, width = 10,
                           stipple = "gray50")
        canvas.create_line(x0, y0, x1, y1, fill = self.btnShading2, width = 10,
                           stipple = "gray25")
        canvas.create_line(x0, y0, x1, y1, fill = self.btnShading3, width = 12,
                           stipple = "gray12")
    def drawArrow(self, canvas, direction, x0, y0, x1, y1):
        ratio = 0.25
        if (direction == "left"):
            tri1x, tri1y = x0 + ratio * (x1 - x0), (y0 + y1) * 0.5
            tri2x, tri2y = x1 - ratio * (x1 - x0), y0 + ratio * (y1 - y0)
            tri3x, tri3y = x1 - ratio * (x1 - x0), y1 - ratio * (y1 - y0)
        elif (direction == "right"):
            tri1x, tri1y = x1 - ratio * (x1 - x0), (y0 + y1) * 0.5
            tri2x, tri2y = x0 + ratio * (x1 - x0), y0 + ratio * (y1 - y0)
            tri3x, tri3y = x0 + ratio * (x1 - x0), y1 - ratio * (y1 - y0)
        # shading idea comes from 112 course notes
        canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 6,
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(x0, y0, x1, y1, fill = self.bgc,
                                outline = self.btnColor)
        canvas.create_rectangle(x0, y0, x1, y1, fill = self.bgc,
                                outline = self.btnColor)
        canvas.create_polygon(tri1x, tri1y, tri2x, tri2y, tri3x, tri3y,
                              fill = self.bgc, outline = self.btnColor,
                              activefill = self.btnActive)
    # this function is based on file I/O from course 112 notes, I am using a
    # txt file to save the user options
    def saveOptions(self):
        with open('settings.txt', 'wt') as fout:
            fout.write(str(self.currentSL) + ',' + str(self.currentTL))
    # this function is based on file I/O from course 112 notes
    def readOptions(self):
        with open('settings.txt', 'rt') as fin:
            content = fin.read()
        settings = content.split(',')
        self.currentSL = int(settings[0])
        self.currentTL = int(settings[1])
                                   
    
class MainMenu(Page):
    def __init__(self):
        self.textInPage = [("INSTERPRETER", 40, 400, 40, False),
                           ("Translation", 25, 600, 150, True),
                           ("Option", 25, 200, 500, True),
                           ("Instruction", 25, 600, 500, True)]
        super(MainMenu, self).__init__()
    def Draw(self, canvas, step):
        super(MainMenu, self).Draw(canvas, step)
        self.drawRadar(canvas, step)
        self.drawCircuit(canvas, step)
    def drawRadar(self, canvas, step):
        canvas.create_oval(50, 100, 400, 450, outline = None,
                           fill = self.btnShading3)
        canvas.create_arc(50, 100, 400, 450, start = 90 + step * 3, extent = 240,
                          fill = self.btnActive, outline = None)
        canvas.create_oval(80, 130, 370, 420, outline = None, fill = self.bgc)
        canvas.create_oval(130, 180, 320, 370, outline = None, fill = 'grey18')
        canvas.create_arc(130, 180, 320, 370, start = -10 - step * 4, extent = 100,
                          fill = '#98f5ff', outline = None)
        canvas.create_oval(145, 195, 305, 355, outline = None,
                           fill = self.btnShading3)
        canvas.create_arc(145, 195, 305, 355, start = -80 + step * 4, extent = 170,
                           fill = '#a8a8a8', outline = None)
        canvas.create_oval(160, 210, 290, 340, outline = None, fill = 'grey18')
        canvas.create_arc(160, 210, 290, 340, start = 130 - step * 3, extent = 320,
                           fill = '#00868b', outline = None)
        canvas.create_oval(175, 225, 275, 325, fill = self.bgc,
                           outline = self.btnActive, outlinestipple = 'gray25',
                           width = 4)
        canvas.create_text(225, 275, text = 'T', font = 'Tron 34',
                           fill = self.btnActive)
        canvas.create_text(225, 275, text = 'T', font = 'Tron 32',
                           fill = self.btnShading1)
        canvas.create_text(225, 274, text = 'T', font = 'Tron 30',
                           fill = self.btnColor)
    def drawCircuit(self, canvas, step):
        # Vertical Circuit No.1
        canvas.create_rectangle(410, 305, 425, 345, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(417.5, 305, 417.5, 225, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(417.5, 225, 452.5, 190, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(452.5, 190, 520, 190, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(520, 182.5, 535, 197.5, fill = None,
                           outline = self.btnShading1, width = 3)
        canvas.create_line(417.5, 345, 417.5, 400, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(417.5, 400, 347.5, 470, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(347.5, 470, 100, 470, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(100, 470, 80, 490, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(80, 490, 80, 517.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(80, 517.5, 100, 537.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(100, 537.5, 382.5, 537.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(382.5, 537.5, 422.5, 577.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(422.5, 577.5, 720, 577.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_rectangle(720, 557.5, 750, 597.5, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(750, 577.5, 760, 577.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(760, 577.5, 767.5, 570, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(767.5, 570, 767.5, 565, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(760, 550, 775, 565, fill = None,
                           outline = self.btnShading1, width = 3)

        # Vertical Circuit No.2
        canvas.create_rectangle(435, 305, 450, 345, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(442.5, 345, 442.5, 400, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(442.5, 400, 512.5, 470, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(512.5, 470, 680, 470, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(680, 462.5, 695, 477.5, fill = None,
                           outline = self.btnShading1, width = 3)
        canvas.create_line(442.5, 305, 442.5, 287.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(442.5, 287.5, 485, 287.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(485, 287.5, 485, 275, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(485, 275, 542.5, 275, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(542.5, 275, 542.5, 197.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(542.5, 197.5, 560, 197.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_rectangle(560, 190, 600, 205, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        # Vertical Circuit No.3
        canvas.create_rectangle(460, 305, 475, 345, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(467.5, 345, 467.5, 390, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(467.5, 390, 517.5, 440, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(517.5, 440, 707.5, 440, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(707.5, 440, 732.5, 465, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(730, 462.5, 745, 477.5, fill = None,
                           outline = self.btnShading1, width = 3)
        # Vertical Circuit No.4
        canvas.create_rectangle(485, 305, 500, 345, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(492.5, 345, 492.5, 380, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(492.5, 380, 522.5, 410, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(522.5, 410, 740, 410, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(740, 402.5, 755, 417.5, fill = None,
                           outline = self.btnShading1, width = 3)
        
# Vertical Circuit No.5
        canvas.create_rectangle(510, 305, 525, 345, fill = '#FFE64D',
                                width = 2, outline = '#DF740C')
        canvas.create_line(517.5, 345, 517.5, 370, fill = '#DF740C', width = 3)
        canvas.create_line(517.5, 370, 527.5, 380, fill = '#DF740C', width = 3)
        canvas.create_line(527.5, 380, 770, 380, fill = '#DF740C', width = 3)
        canvas.create_line(770, 380, 780, 390, fill = '#DF740C', width = 3)
        canvas.create_line(780, 390, 780, 530, fill = '#DF740C', width = 3)
        canvas.create_oval(772.5, 530, 787.5, 545, fill = None,
                           outline = '#DF740C', width = 3)
        
        # Vertical Circuit No.6
        canvas.create_rectangle(535, 305, 550, 345, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(550, 325, 630, 325, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(630, 325, 655, 350, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(655, 350, 770, 350, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(770, 342.5, 785, 357.5, fill = None,
                           outline = self.btnShading1, width = 3)
        # Horizontal Circuit No.0
        canvas.create_oval(747.5, 530, 762.5, 545, fill = '#FFE64D',
                           outline = '#DF740C', width = 3)
        canvas.create_line(747.5, 537.5, 430, 537.5, fill = '#DF740C',
                           width = 3)
        canvas.create_line(430, 537.5, 410, 517.5, fill = '#DF740C', width = 3)
        canvas.create_line(410, 517.5, 410, 490, fill = '#DF740C', width = 3)
        canvas.create_line(410, 490, 430, 470, fill = '#DF740C', width = 3)
        canvas.create_line(430, 470, 435, 470, fill = '#DF740C', width = 3)
        canvas.create_rectangle(435, 462.5, 475, 477.5, fill = '#FFE64D',
                                outline = '#DF740C', width = 3)
        
        # Horizontal Circuit No.1
        canvas.create_rectangle(670, 310, 710, 325, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(710, 317.5, 715, 317.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(715, 317.5, 780, 252.5, fill = self.btnShading1,
                           width = 3)

        # Horizontal Circuit No.2
        canvas.create_rectangle(670, 280, 710, 295, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(710, 287.5, 715, 287.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(715, 287.5, 750, 252.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(750, 252.5, 750, 235, fill = self.btnShading1,
                           width = 3)
        
        # Horizontal Circuit No.3
        canvas.create_rectangle(670, 250, 710, 265, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_rectangle(560, 280, 600, 295, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(600, 287.5, 630, 287.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(630, 287.5, 660, 257.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(660, 257.5, 670, 257.5, fill = self.btnShading1,
                           width = 3)        
        # Horizontal Circuit No.3
        canvas.create_rectangle(670, 220, 710, 235, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(710, 227.5, 742.5, 227.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_oval(742.5, 220, 757.5, 235, fill = None,
                           outline = self.btnShading1, width = 3)
        # Horizontal Circuit No.4
        canvas.create_rectangle(560, 250, 600, 265, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(600, 257.5, 630, 257.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(630, 257.5, 645, 242.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(645, 242.5, 750, 242.5, fill = self.btnShading1,
                           width = 3)
        # Horizontal Circuit No.5
        canvas.create_rectangle(560, 220, 600, 235, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(600, 227.5, 615, 227.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(615, 227.5, 630, 212.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(630, 212.5, 780, 212.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(780, 212.5, 780, 252.5, fill = self.btnShading1,
                           width = 3)
        # Horizontal Circuit No.6
        canvas.create_rectangle(670, 190, 710, 205, fill = self.btnActive,
                                width = 2, outline = self.btnShading1)
        canvas.create_line(670, 197.5, 625, 197.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(625, 197.5, 612.5, 210, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(612.5, 210, 555, 210, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(555, 210, 555, 287.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(492.5, 287.5, 555, 287.5, fill = self.btnShading1,
                           width = 3)
        canvas.create_line(492.5, 287.5, 492.5, 305, fill = self.btnShading1,
                           width = 3)
        
        


class Option(Page):
    def __init__(self):
        # separate source language and target language dict because source
        # languages are displayed in its original language, while target
        # languages are displayed in English
        sLPairs = [('en', 'English'), ('es', 'Español'), ('de', 'Deutsch'),
                     ('fr', 'Français'), ('nl', 'Nederlands'),
                     ('auto', 'Auto-Detection')] # source language pairs
        self.sLDict = dict(sLPairs)
        tLPairs = [('zh-CN', 'Chinese (Simplified)'), ('ru', 'Russian'),
                   ('hi', 'Hindi'), ('ja', 'Japanese'), ('ko', 'Korean'),
                   ('en', 'English'), ('es', 'Spanish'), ('de', 'German'),
                   ('fr', 'French'), ('nl', 'Dutch'),
                   ('zh-TW', 'Chinese (Traditional)')]
        self.tLDict = dict(tLPairs)
        # read indexs of the current source and target language in the lists
        self.textInPage = [("Option", 25, 100, 30, False),
                           ("Source Language", 20, 400, 150, False),
                           ("Target Language", 20, 400, 300, False),
                           ("Set Default", 20, 400, 450, True),
                           ("Back", 20, 730, 570, True)]
        self.arrowPos = [("left", 250, 205, 290, 245),
                         ("right", 510, 205, 550, 245),
                         ("left", 250, 355, 290, 395),
                         ("right", 510, 355, 550, 395)]
        super(Option, self).__init__()

    def drawLanguage(self, canvas):
        SLtext = self.sLDict[self.sourceLang[self.currentSL]]
        TLtext = self.tLDict[self.targetLang[self.currentTL]]
        canvas.create_text(400, 225, font = "Arial 15", text = SLtext,
                           fill = self.btnActive)
        canvas.create_text(400, 375, font = "Arial 15", text = TLtext,
                           fill = self.btnActive)
    def Draw(self, canvas, step):
        super(Option, self).Draw(canvas, step)
        self.readOptions()
        # draw frame
        self.drawShading(canvas, 50, 470, 50, 130)
        canvas.create_line(50, 470, 50, 130, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 50, 130, 80, 100)
        self.drawShading(canvas, 80, 100, 720, 100)
        canvas.create_line(80, 100, 720, 100, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 750, 130, 720, 100)
        self.drawShading(canvas, 750, 130, 750, 470)
        canvas.create_line(750, 130, 750, 470, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 750, 470, 720, 500)
        self.drawShading(canvas, 720, 500, 80, 500)
        canvas.create_line(720, 500, 80, 500, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 50, 470, 80, 500)
        # draw textbox for options, shading idea comes from 112 course notes
        canvas.create_rectangle(300, 205, 500, 245, fill = None, width = 6,
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(300, 205, 500, 245, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(300, 205, 500, 245, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(300, 205, 500, 245, fill = None,
                                outline = self.btnShading1)
        canvas.create_rectangle(300, 355, 500, 395, fill = None, width = 6,
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(300, 355, 500, 395, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(300, 355, 500, 395, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(300, 355, 500, 395, fill = None,
                                outline = self.btnShading1)
        self.drawLanguage(canvas)
        for arrow in self.arrowPos:
            self.drawArrow(canvas, *arrow) # unpack position tuples here
    def Mouse(self, mouseX, mouseY):
        # change language when click on arrows
        sLeft, sRight = self.arrowPos[0], self.arrowPos[1]
        tLeft, tRight = self.arrowPos[2], self.arrowPos[3]
        if (sLeft[1] <= mouseX <= sLeft[3] and sLeft[2] <= mouseY <= sLeft[4]):
            self.currentSL = (self.currentSL - 1) % len(self.sourceLang)
        elif (sRight[1] <= mouseX <= sRight[3] and
              sRight[2] <= mouseY <= sRight[4]):
            self.currentSL = (self.currentSL + 1) % len(self.sourceLang)
        elif (tLeft[1] <= mouseX <= tLeft[3] and tLeft[2] <= mouseY<= tLeft[4]):
            self.currentTL = (self.currentTL - 1) % len(self.targetLang)
        elif (tRight[1] <= mouseX <= tRight[3] and
              tRight[2] <= mouseY <= tRight[4]):
            self.currentTL = (self.currentTL + 1) % len(self.targetLang)
        # set default
        elif (320 <= mouseX <= 480 and 425 <= mouseY <= 475):
            self.currentSL, self.currentTL = 0, 8
       # call self.saveOptions() to save options after every single click
        self.saveOptions()
        
        
class Instruction(Page):
    def __init__(self):
        self.textInPage = [("Instruction", 25, 190, 30, False),
                           ("Back", 20, 730, 570, True)]
        self.insText = '''Insterpreter\
 is a program to help you translate with your webcam. In auto mode, place the \
text you want to translate in front of the webcam, and the program will replace\
 the text with the translation on the screen automaticly. You can select the \
source language and the target language in the "Option" page or "Translation" \
page. The default source\
 language is set at the "Auto-detection" mode and the default target language \
is set to be "German". In Manual Mode, click three times on the center of each \
landmark, and click the fourth time on the edge of the third clicked landmark,\
then the translation will automatically replace the text. Click "Clear" to \
reset the manual mode.
P.S. Text can be rotated at any angle facing the webcam :)'''
        super(Instruction, self).__init__()
    def Draw(self, canvas, step):
        super(Instruction, self).Draw(canvas, step)
        # add some decorations
        # text frame with rounded corner
        self.drawShading(canvas, 50, 470, 50, 130)
        canvas.create_line(50, 470, 50, 130, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 50, 130, 80, 100)
        self.drawShading(canvas, 80, 100, 720, 100)
        canvas.create_line(80, 100, 720, 100, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 750, 130, 720, 100)
        self.drawShading(canvas, 750, 130, 750, 470)
        canvas.create_line(750, 130, 750, 470, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 750, 470, 720, 500)
        self.drawShading(canvas, 720, 500, 80, 500)
        canvas.create_line(720, 500, 80, 500, fill = self.btnColor, width = 4)
        self.roundedCorner(canvas, 50, 470, 80, 500)
        # draw instruction text
        canvas.create_text(400, 300, text = self.insText,
                   fill = self.btnColor,
                   font = "Arial 18", width = 650)
        
class Translation(Page):
    def __init__(self):
        self.textInPage = [("Translation", 25, 190, 30, False),
                           ("Back", 20, 730, 570, True)]
        self.cap = cv2.VideoCapture(0)
        self.auto = True # auto or manual detection
        self.circle = []
        super(Translation, self).__init__()
    def Draw(self, canvas, step):
        super(Translation, self).Draw(canvas, step)
        self.readOptions()
        # language selecton
        self.SL = self.sourceLang[self.currentSL]
        self.TL = self.targetLang[self.currentTL]
        # textbox with semi-transparency
        canvas.create_rectangle(40, 570, 140, 590, fill = None, width = 6,
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(40, 570, 140, 590, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(40, 570, 140, 590, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(40, 570, 140, 590, fill = None,
                                outline = self.btnShading1)
        canvas.create_rectangle(300, 570, 400, 590, fill = None, width = 6,
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(300, 570, 400, 590, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(300, 570, 400, 590, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(300, 570, 400, 590, fill = None,
                                outline = self.btnShading1)
        # text showing language selection
        canvas.create_text(90, 580, text = self.SL, font = 'Arial 12',
                           fill = self.btnActive)
        canvas.create_text(350, 580, text = self.TL, font = 'Arial 12',
                           fill = self.btnActive)
        # title of the textbox
        canvas.create_text(90, 550, text = "source", font = 'Tron 12',
                           fill = self.btnActive)
        canvas.create_text(350, 550, text = "target", font = 'Tron 12',
                           fill = self.btnActive)        
        # draw Arrows
        self.drawArrow(canvas, 'left', 20, 570, 40, 590)
        self.drawArrow(canvas, 'right', 140, 570, 160, 590)
        self.drawArrow(canvas, 'left', 280, 570, 300, 590)
        self.drawArrow(canvas, 'right', 400, 570, 420, 590)
        # draw auto-manual button
        if (self.auto == True):
            canvas.create_rectangle(770, 300, 790, 350, fill = self.bgc,
                                    activefill = self.btnActive,
                                    outline = self.btnShading1, width = 3)
            canvas.create_line(780, 300, 780, 80, fill = "#04080C", width = 3)
            canvas.create_line(780, 80, 740, 40, fill = "#04080C", width = 3)
            canvas.create_line(740, 40, 680, 40,fill = "#04080C", width = 3)
            canvas.create_oval(665, 32.5, 680, 47.5, fill = None,
                               outline = "#04080C", width = 3)
            canvas.create_line(780, 300, 780, 50, fill = self.btnShading1, width = 3)
            canvas.create_line(780, 50, 750, 20, fill = self.btnShading1, width = 3)
            canvas.create_line(750, 20, 680, 20, fill = self.btnShading1, width = 3)
            canvas.create_oval(665, 12.5, 680, 27.5, fill = None,
                               outline = self.btnShading1, width = 3)
            canvas.create_text(650, 20, font = "Tron 12", text = 'AUTO',
                               fill = self.btnActive, anchor = tk.E)
            canvas.create_text(650, 40, font = "Tron 12", text = 'MANUAL',
                               fill = "#04080C", anchor = tk.E)
        else:
            canvas.create_rectangle(770, 300, 790, 350, fill = self.bgc,
                                    activefill = '#FFE64D',
                                    outline = '#DF740C', width = 3)
            canvas.create_line(780, 300, 780, 50, fill = "#04080C", width = 3)
            canvas.create_line(780, 50, 750, 20, fill = "#04080C", width = 3)
            canvas.create_line(750, 20, 680, 20, fill = "#04080C", width = 3)
            canvas.create_oval(665, 12.5, 680, 27.5, fill = None,
                               outline = "#04080C", width = 3)
            canvas.create_line(780, 300, 780, 80, fill = '#DF740C', width = 3)
            canvas.create_line(780, 80, 740, 40, fill = '#DF740C', width = 3)
            canvas.create_line(740, 40, 680, 40,fill = '#DF740C', width = 3)
            canvas.create_oval(665, 32.5, 680, 47.5, fill = None,
                               outline = '#DF740C', width = 3)
            canvas.create_text(650, 20, font = "Tron 12", text = 'AUTO',
                               fill = "#04080C", anchor = tk.E)
            canvas.create_text(650, 40, font = "Tron 12", text = 'MANUAL',
                               fill = '#FFE64D', anchor = tk.E)
        # draw clear button
        canvas.create_rectangle(730, 400, 790, 450, fill = None, width = 6,
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(730, 400, 790, 450, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(730, 400, 790, 450, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(730, 400, 790, 450, fill = None,
                                outline = self.btnShading1)
        canvas.create_text(760, 425, font = "Arial 12 bold", text = 'CLEAR',
                               fill = self.btnActive)

        # webcam section
        ret, frame = self.cap.read()
        self.counter -= 1

        if (self.auto == True):
            frame, flag = OCVa.run(frame, self.TL, self.SL)
        else:
            frame, flag = OCVm.run(frame, self.TL, self.SL, self.circle)
        if flag == True:
            self.counter = 20
            cv2.imwrite('frame1.jpg', frame)
        else:
            cv2.imwrite('frame.jpg', frame)
        if (self.counter >= 0): # still display frame1.jpg
            self.PILim = Image.open('frame1.jpg')
        else:
            self.PILim = Image.open('frame.jpg')
        self.photo = ImageTk.PhotoImage(image = self.PILim)
        canvas.create_image(400, 300, image = self.photo)
        # draw dots
        for dot in self.circle:
            canvas.create_line(dot[0], dot[1], dot[0]+1, dot[1]+1, fill = 'red',
                               width = 8)
    def Mouse(self, mouseX, mouseY):
        if (20 <= mouseX <= 40 and 570 <= mouseY <= 590):
            self.currentSL = (self.currentSL - 1) % len(self.sourceLang)
        if (140 <= mouseX <= 160 and 570 <= mouseY <= 590):
            self.currentSL = (self.currentSL + 1) % len(self.sourceLang)
        if (280 <= mouseX <= 300 and 570 <= mouseY <= 590):
            self.currentTL = (self.currentTL - 1) % len(self.targetLang)
        if (400 <= mouseX <= 420 and 570 <= mouseY <= 590):
            self.currentTL = (self.currentTL + 1) % len(self.targetLang)
        if (770 <= mouseX <= 790 and 300 <= mouseY <= 350):
            self.auto = not self.auto
        if (self.auto == False): # Manual mode
            if (len(self.circle) <= 4 and 80 <= mouseX <= 720 and
                60 <= mouseY <= 540):
                self.circle.append([mouseX, mouseY])
        # make a clear button
        if (730 <= mouseX <= 790 and 400 <= mouseY <= 450):
            self.circle = []
            self.counter = -1
        self.saveOptions()
        
        
Insterpreter(width = 800, height = 600).run()
