import numpy as np
import cv2
import pickle
import time 
import datetime

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime


def save_frames(FILE_NAME):
    #records and saves colour and depth frames from the Kinect
    
    print("Saving colour and depth frames")
    
    # define file names
    depthfilename = "DEPTH." + FILE_NAME +".pickle"
    colourfilename = "COLOUR." + FILE_NAME +".pickle"
    depthfile = open(depthfilename, 'wb')
    colourfile = open(colourfilename, 'wb')
    
    #initialise kinect recording, and some time variables for tracking the framerate of the recordings
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
    starttime = time.time()
    oldtime = 0
    i = 0
    fpsmax = 0
    fpsmin = 100
    
    # display_type = "COLOUR"
    display_type = "DEPTH"
    
    # Actual recording loop, exit by pressing escape to close the pop-up window
    while True:
        
        if kinect.has_new_depth_frame() and kinect.has_new_color_frame() :
            elapsedtime = time.time()- starttime
            if(elapsedtime> i/10):
                
                #Only for high i try evalutaing FPS or else you get some divide by 0 errors
                if i >10:
                    try:
                        fps =  1/(elapsedtime - oldtime)
                        print(fps)
                        if fps> fpsmax:
                            fpsmax= fps
                        if fps < fpsmin:
                            fpsmin = fps
    
                    except ZeroDivisionError:
                        print("Divide by zero error")
                        pass
                    
                oldtime = elapsedtime
                
                #read kinect colour and depth data (somehow the two formats below differ, think one is and one isnt ctypes)
                depthframe = kinect.get_last_depth_frame() #data for display
                depthframeD = kinect._depth_frame_data
                colourframe = kinect.get_last_color_frame()
                colourframeD = kinect._color_frame_data
                
                #convert depth frame from ctypes to an array so that I can save it
                depthframesaveformat = np.copy(np.ctypeslib.as_array(depthframeD, shape=(kinect._depth_frame_data_capacity.value,))) # TODO FIgure out how to solve intermittent up to 3cm differences
                pickle.dump(depthframesaveformat, depthfile)
                
                #reformat the other depth frame format for it to be displayed on screen
                depthframe = depthframe.astype(np.uint8)
                depthframe = np.reshape(depthframe, (424, 512))
                depthframe = cv2.cvtColor(depthframe, cv2.COLOR_GRAY2RGB)
    
                #Reslice to remove every 4th colour value, which is superfluous
                colourframe = np.reshape(colourframe, (2073600, 4))
                colourframe = colourframe[:,0:3] 
                
                #extract then combine the RBG data
                colourframeR = colourframe[:,0]
                colourframeR = np.reshape(colourframeR, (1080, 1920))
                colourframeG = colourframe[:,1]
                colourframeG = np.reshape(colourframeG, (1080, 1920))        
                colourframeB = colourframe[:,2]
                colourframeB = np.reshape(colourframeB, (1080, 1920))
                framefullcolour = cv2.merge([colourframeR, colourframeG, colourframeB])
                pickle.dump(framefullcolour, colourfile)
                
                if display_type == "COLOUR":
                    
                    #Show colour frames as they are recorded
                    cv2.imshow('Recording KINECT Video Stream', framefullcolour)
                
                if display_type == "DEPTH":
                    
                    #show depth frames as they are recorded
                    cv2.imshow('Recording KINECT Video Stream', depthframe)
                
                i = i+1
    
        #end recording if the escape key (key 27) is pressed
        key = cv2.waitKey(1)
        if key == 27: break
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    currentdate = datetime.datetime.now()
    custom_name = input("Enter a file name: ")
    file_name = custom_name + "." + str(currentdate.day) + "." + str(currentdate.month) + "."+ str(currentdate.hour) + "."+ str(currentdate.minute)
    
    #Save colour and depth frames
    save_frames(file_name)