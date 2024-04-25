import cv2
import os
from natsort import natsorted

# Make video from the images
vidFolder='video'
video_name = 'lensing.mp4'
fps = 8


images = [img for img in os.listdir(vidFolder) if img.endswith(".png")]
images = natsorted(images)
frame = cv2.imread(os.path.join(vidFolder, images[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, 0, fps, (width,height))
for image in images:
    video.write(cv2.imread(os.path.join(vidFolder, image)))

cv2.destroyAllWindows()
video.release()

print("Finished.")