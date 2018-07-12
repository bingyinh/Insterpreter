Project Readme File

##############################

##########Bingyin Hu##########

##############################


##############################

######Name of the Project#####

##############################


Insterpreter (Instant Interpreter)


##############################

########About Project#########

##############################


Insterpreter is a live webcam translator. There are two modes, auto mode and manual mode respectively. The GUI of Insterpreter is constructed based on eventBasedAnimation (15-112 course resource) and using a OOP structure. To use the app, a paper with three circle landmarks (red, green, blue respectively) is required. Printed text are to be located within the landmarks. Basically, the webcam (runned by OpenCV) captures the image lively, detects the landmark location, crops the text image and place it horizontally in a new blank image with the same size of the text image. Feed the text image into pytesser (http://code.google.com/p/pytesser/ by Michael J.T. O'Kelly), which is a text recognition module outputing text string given text image input. Then using PIL the draw the text on the webcam image and feed it back to out main pyfile running in the Tkinter. Users can simply stare at the text they want to translate, and wait for a little while, the translation will be stamped on the exact location of the original text. When you want it to translate into another language, simply click on the button either in the option page or in the translation page.

In the auto mode, once the three landmarks are detected at the same time, the translation modules will be triggered.
In the manual mode, click on the center of the three landmarks, and make another click on the edge of the last clicked landmark so that the radius of the landmark can be computed. (This is important! Otherwise the text image will contain 1/4 of the circle and thus causing text recognition module unable to output the right text string!). Click on "clear" in the manual mode if users want to clean the screen and translate another piece of paper.

An explanation video can be found at: https://www.youtube.com/watch?v=yBiqw4htpKA

##############################

##########How to Run##########

##############################


Just run the GUI.py!


##############################

############Modules###########

##############################

Since the module installation file varies on different computers, I will just list the modules I used and the website.
eventBasedAnimation (15-112 course resource)
pytesser (http://code.google.com/p/pytesser/ by Michael J.T. O'Kelly)
OpenCV (http://opencv.org/downloads.html)
PIL (http://www.pythonware.com/products/pil/)
numpy (http://sourceforge.net/projects/numpy/files/)
mechanize (http://wwwsearch.sourceforge.net/mechanize/download.html)
Tkinter, os, math, urllib are pre-installed

I will provide a package with modules that are used in my laptop, but please note it is not guaranteed to work well on other laptops.