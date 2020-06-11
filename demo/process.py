import numpy as np
import pickle
import cv2
import ctypes
import os
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

#REMEBER TO HAVE A KINECT CONNECTED (OR KINECT STUDIO REPLAYING A RECORDING) WHEN RUNNING, EVEN THOUGH WE ARE OPERATING OFF SAVED DATA!
def get_3D_coordinates(filename, show_each_frame = False):
    """saves the 3D positions of a list of 2D pixel positions in the colour image. Correspodning depth data stored in DEPTH.filename.pickle"""
    
    #Define a list of 2D coordinates you want to locate
    colour_image_pixels_to_locate_list = [[880,555], [1440,200]]
    
    #Start a kinect (NEED TO CONNECT A KINECT or run a recording in kinect studio to make this command work,  even though we are reading saved depth values)
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)

    #Do a bunch of defines required for matching the colour coordinates to their depth later
    color2depth_points_type = _DepthSpacePoint* np.int(1920 * 1080)
    color2depth_points = ctypes.cast(color2depth_points_type(), ctypes.POINTER(_DepthSpacePoint))
    S = 1080*1920
    TYPE_CameraSpacePointArray = PyKinectV2._CameraSpacePoint * S
    csps1 = TYPE_CameraSpacePointArray()
    
    #load your saved depth data
    depthdatafile = open("DEPTH." + filename + ".pickle", "rb")
    
    #make list to store the 3D positions in
    pixel_positions_3D_list = []
    
    #Iterate over each saved frame of depth data
    depth_file_not_finished = True
    while depth_file_not_finished == True:
        try:
            depthframe = pickle.load(depthdatafile) #each call loads a sucessive frame from a pickle file, so we need to do this once per frame
            
            three_D_pixel_positions_in_frame =[] # list to store the 3D pixel positions from one frame
            
            #Defines to allow colour pixel mapping to 3D coords to work correctly     
            ctypes_depth_frame = np.ctypeslib.as_ctypes(depthframe.flatten())
            L = depthframe.size
            kinect._mapper.MapColorFrameToCameraSpace(L, ctypes_depth_frame, S, csps1)
            
            #Carry out certain actions if you want an image of where all the tracked points are in the depth data (makes program 20x slower)
            if show_each_frame == True:
                
                #Note the method on the line below, for finding the corrsponding depth pixel of a single tracked pixel in the colour image, is NOT what I am using to find the 3D position of a colour pixel
                kinect._mapper.MapColorFrameToDepthSpace(ctypes.c_uint(512 * 424), ctypes_depth_frame, ctypes.c_uint(1920 * 1080), color2depth_points)
    
                cut_down_depth_frame = depthframe.astype(np.uint8)
                cut_down_depth_frame = np.reshape(cut_down_depth_frame, (424, 512))
               
            #Iterate over the lists of pixel positions in the 2D colour image to locate
            for pixel in colour_image_pixels_to_locate_list:
                
                #find x and y in pixel position in the 2D colour image
                x = pixel[0]
                y = pixel[1]
                
                #Find 3D position of each pixel (relative to camera) using Colour_to_camera method, all measurements (x, y and z) in m
                x_3D = csps1[y*1920 + x].x
                y_3D = csps1[y*1920 + x].y
                z_3D = csps1[y*1920 + x].z
                pixel_position_3D = [x_3D, y_3D, z_3D]
                
                #if show_each_frame flag set,  display the depth data and corresponding points you are reading
                if show_each_frame == True:
                    
                    try:
                        
                        #method below finds 2D depth pixel that corresponds to a 2D colour pixel, for use in the pop up images, to show you what points you are tracking. While it could be used to find 3D joint positions, IT IS NOT THE METHOD I USE OR RECOMMEND FOR FINDING 3D JOINT POSITIONS, as it gives you x and y in pixels not m (z is in mm)
                        read_pos = x+y*1920 -1
                        depth_image_corresponding_x = int(color2depth_points[read_pos].x)
                        depth_image_corresponding_y = int(color2depth_points[read_pos].y)
                        
                        #plot a circle at the pixel in the depth frame that matches the corresponding pixel in the image frame
                        cv2.circle(cut_down_depth_frame, (depth_image_corresponding_x,depth_image_corresponding_y), 5, (255, 0, 255), -1)
                        
                        #note that the value below is NOT used in this code, included just for reference
                        corresponding_depth = depthframe[((depth_image_corresponding_y * 512) + depth_image_corresponding_x)]
                        
                    except OverflowError:
                        #the SDK returns infinity for the depth of some positions, so we need to handle that
                        #I choose to not find the corresponding pixel in the depth image, and so dont plot a circle there, in this case
                        pass
        
                #Display annotated depth image if flag is set
                if show_each_frame == True:
                    cv2.imshow('KINECT Video Stream', cut_down_depth_frame)
                    
                    #code to close window if escape is pressed, doesnt do anything in this program (as we keep calling for data to be displayed in the window) but included for reference
                    key = cv2.waitKey(1)
                    if key == 27: 
                        pass
                
                #add 3D positions found in this frame to an intermediate list
                three_D_pixel_positions_in_frame.append(pixel_position_3D)
                
            #add per frame lists of 3D position into a results list
            pixel_positions_3D_list.append(three_D_pixel_positions_in_frame)
                
       #close loop at end of file
        except EOFError:
            cv2.destroyAllWindows()
            depth_file_not_finished = False
            
    #return 3D joint position lists 
    return pixel_positions_3D_list
     
    

if __name__ == '__main__': 
    
    #replace name below with the corresponding section of the name of your saved depth data (for reference, the full name of my saved depth data file was DEPTH.test.1.29.13.17.pickle)
    three_dimensionsal_positions = get_3D_coordinates('test.8.6.15.40', show_each_frame =  True)
    print(three_dimensionsal_positions)