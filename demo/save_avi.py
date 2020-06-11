import cv2
import pickle

def frames_to_video(FILE_NAME):
    """Code to stitch a video based on frames saved in a pickle file"""
    
    print("stiching colour frames into video")
    
    #Load first colour frame, to get colour frame properties
    datafile = open("COLOUR." + FILE_NAME + ".pickle", "rb")
    # datafile = open("DEPTH." + FILE_NAME + ".pickle", "rb")
    frame = pickle.load(datafile)
    height, width, channels = frame.shape
    
    #define video properties
    out = cv2.VideoWriter(FILE_NAME + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (int(width), int(height))) 
    
    #display first frame on a screen for progress (some duplication of later code as first frame needs to be loaded seperately to the rest so we can get the frame dimensions from it)
    out.write(frame)
    cv2.imshow('Stiching Video',frame)

    #Cycle through the rest of the colour frames, stiching them together
    while True:
        try:
            frame = pickle.load(datafile)
            out.write(frame)
            cv2.imshow('Stiching Video',frame)
            if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
                break
        except EOFError:
            print("Video Stiching Finished")
            break

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__': 
    
    #replace name below with the corresponding section of the name of your saved depth data (for reference, the full name of my saved colour data file was COLOUR.test.1.29.13.17.pickle)
    frames_to_video('test.8.6.15.40')