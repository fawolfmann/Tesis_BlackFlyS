import PySpin
import os
import re
import time
# Get system
system = PySpin.System.GetInstance()

camera = True
print("waiting for camera ")
while(camera):
# Get camera list
    print(".")
    cam_list = system.GetCameras()
    if cam_list.GetSize() > 0 :
    # Figure out which is primary and secondary (usually webcam is primary and Flea3 is secondary)
        cam = cam_list.GetByIndex(0)
        camera = False
    time.sleep(2)

# Initialize camera
cam.Init()

# Set acquisition mode
cam.AcquisitionMode.SetValue(PySpin.AutoExposureControlPriority_ExposureTime)
#cam.AcquisitionMode.SetValue(PySpin.ExposureAuto_Continuous)
cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)


# Create folder for save images and find the count number
folder_path = 'flir_photos'
count = 0
if not folder_path in os.listdir('.'):
    os.mkdir(folder_path, 766)
else:
    p = re.compile('image(\d+).(\w+)')
    if os.listdir(folder_path) :
        m = p.match(max(os.listdir(folder_path)))
        count = int(m.group(1)) +1



for i in range(5):
    # Start acquisition
    cam.BeginAcquisition()
    # Acquire images
    image_primary = cam.GetNextImage()
    #width = image_primary.GetWidth()
    #height = image_primary.GetHeight()
    #print ("width: " + str(width) + ", height: " + str(height))

    # Pixel array
    time4 = time.time()
    image_converted = image_primary.Convert(PySpin.PixelFormat_RGB8 , PySpin.NO_COLOR_PROCESSING)
    # Save images
    image_converted.Save(folder_path +'/image' + '{:04d}'.format(count+i)+ '.jpeg')

    #image_primary.Save(folder_path +'/image' + '{:04d}'.format(count+i)+ '.jpeg' )

    print(time.time() - time4)
    # Stop acquisition
    cam.EndAcquisition()

# De-initialize
cam.DeInit()

# Clear references to images and cameras
del image_primary
del cam
del cam_list

