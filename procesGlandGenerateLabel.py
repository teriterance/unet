import numpy as np
import cv2
import sys
from os import listdir, mkdir
from os.path import isfile, join, exists
import matplotlib.pyplot as plt

def img_preprocessing(BaseDatasetFolderPath = "../data_base/", customDatasetFolderPath = "./data/gland", imgsize = 32):
    ##### Load Image #####
    intt = 0
    for patient in listdir(BaseDatasetFolderPath):
        if isfile(patient) or "xlsx" in patient:
            pass
        else:
            for fileName in listdir(join(BaseDatasetFolderPath, patient)):
                if not (".bmp" in fileName or ".jpg" in fileName and "_seg" not in fileName):
                    pass
                elif (".bmp" in fileName or ".jpg" in fileName) and "_seg" not in fileName and "_Elas" not in fileName :
                    img  = cv2.imread(join(BaseDatasetFolderPath, patient, fileName), 0)
                    
                    fileName2 = None
                    if "_val." in fileName:
                        fileName2 = fileName.replace("_val.","_seg.")
                    else :
                        fileName2 = fileName.split('.')[0] + "_seg." + fileName.split('.')[1]
                    
                    img_seg = cv2.imread(join(BaseDatasetFolderPath, patient, fileName2), 0)
                    try:
                        print(join(BaseDatasetFolderPath, patient, fileName2))

                        ##### Process image #####
                        # 1 extract the real image 
                        img2  = img[65:353, 203:715].copy()
                        img_seg2 = img_seg[65:353, 203:715].copy()
                        print(img_seg2.shape)
                        img2 = cv2.copyMakeBorder(img2, int((512-img2.shape[0])/2),int((512-img2.shape[0])/2), int((512-img2.shape[1])/2), int((512-img2.shape[1])/2), cv2.BORDER_CONSTANT)
                        img_seg2 = cv2.copyMakeBorder(img2, int((512-img2.shape[0])/2),int((512-img2.shape[0])/2), int((512-img2.shape[1])/2), int((512-img2.shape[1])/2), cv2.BORDER_CONSTANT)
                        print(img_seg2.shape)
                        print("\n")

                        img_seg2 = ~img_seg2
                        img_seg2 = (~(img_seg2 <= 15)*255).astype(np.uint8)
                        cv2.imwrite(join(customDatasetFolderPath, "train/image/"+str(intt)+".png"), img2)
                        cv2.imwrite(join(customDatasetFolderPath, "train/label/"+str(intt)+".png"), img_seg2)
                        intt = intt+1
                    except:
                        print("error ", join(BaseDatasetFolderPath, patient, fileName2))

if __name__ == "__main__":
    img_preprocessing()