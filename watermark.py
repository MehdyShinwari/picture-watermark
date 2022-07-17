import cv2
import numpy as np
from utils import CFEVideoConf, image_resize
import os
import blend_modes.blending_functions as bm
from pathlib import Path
import pathlib
import sys
import math

def watermarker():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "images")
    processed_dir = os.path.join(BASE_DIR, "watermarked_images")
    pathlib.Path(processed_dir).mkdir(exist_ok=True)
    if (len(sys.argv) < 1):
        print("Error no watermark size given")
        sys.exit(0)

    height = int(sys.argv[1])
    cropfactor1 = 0
    cropfactor2 = math.ceil(height/8)
    cropfactor3 = math.ceil(height/30)
    watermark_path = os.path.join(BASE_DIR, "watermark.png")
    logo = cv2.imread(watermark_path, 0)
    #watermark = image_resize(logo, height=int(sys.argv[1]))
    watermark = image_resize(logo, height=height)
    watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png"):
                frame = cv2.imread(os.path.join(image_dir, file), 1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                frame_h, frame_w, frame_c = frame.shape
                overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
                watermark_h, watermark_w, watermark_c = watermark.shape
                for i in range(cropfactor2, watermark_h-cropfactor1-15):
                    for j in range(cropfactor1, watermark_w-cropfactor3):
                        if watermark[i,j][3] != 0:
                            h_offset = round(frame_h/2) - watermark_h
                            w_offset = round(frame_w*0.8) - watermark_w
                            overlay[h_offset + i, w_offset+ j] = watermark[i,j]

                #cv2.imshow("Watermark", overlay)
                #cv2.waitKey(0)
                #frame = frame.astype(float)
                #overlay = overlay.astype(float)
                #frame = bm.addition(frame, overlay, 0.3)
                cv2.addWeighted(overlay, 0.3, frame, 1.0, 0, frame)     
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                cv2.imwrite(os.path.join(processed_dir, file),frame)
    print("Finished watermarking ^-^")

watermarker()