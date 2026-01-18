<<<<<<< HEAD
import torch
import torchvision.transforms as T
from PIL import Image
import cv2 as cv
import csv
import os
#os.chdir("..")
print(os.getcwd())

# transform = T.Compose([
#     T.Resize((256,256)),
#     T.ToTensor() # Scaled to [0, 1]
# ])

# img1=transform(Image.open("fullSpot.jpg"))
# img2=transform(Image.open("emptySpot.jpg"))

test=input("Is this a test? (y/n)")=='y'
#list for spot coordinates
spots = []
# spots_visual=[]
#load image
img = cv.imread('vlcsnap-2026-01-17-23h54m15s078.png')
img = cv.resize(img, None, fx=.5,fy=.5)
cv.imshow("Parking Lot", img)

def click_event(event, x, y, flags, params):
    
    if event == cv.EVENT_LBUTTONDOWN:
        spots.append((x,y))
        # spots_visual.append((x,y))
        print("point captured: ",x,y)

        if len(spots)%2==0:
            cv.rectangle(img, spots[-2], spots[-1], (0,255,0), 2)
            cv.imshow("Parking Lot", img)

cv.setMouseCallback("Parking Lot", click_event)

print("Insturctions: Click Top left the bottom right of desired spot. Press 's' to save")

while True: 
    key=cv.waitKey(1)
    if key==ord('s'):
        if test:
            with open('occupied_test.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(spots)
        else:
            with open('occupied_train.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(spots)
        break 
    elif key == 27:
        break
spots = []
while True: 
    key=cv.waitKey(1)
    if key==ord('s'):
        if test:
            with open('empty_test.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(spots)
        else:
            with open('empty_train.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(spots)
        break 
    elif key == 27:
        break
cv.destroyAllWindows()



=======
import torch
import torchvision.transforms as T
from PIL import Image
import cv2 as cv
import csv
import os
#os.chdir("..")
print(os.getcwd())

# transform = T.Compose([
#     T.Resize((256,256)),
#     T.ToTensor() # Scaled to [0, 1]
# ])

# img1=transform(Image.open("fullSpot.jpg"))
# img2=transform(Image.open("emptySpot.jpg"))

test=input("Is this a test? (y/n)")=='y'
#list for spot coordinates
spots = []
# spots_visual=[]
#load image
img = cv.imread('vlcsnap-2026-01-17-23h54m15s078.png')
img = cv.resize(img, None, fx=.5,fy=.5)
cv.imshow("Parking Lot", img)

def click_event(event, x, y, flags, params):
    
    if event == cv.EVENT_LBUTTONDOWN:
        spots.append((x,y))
        # spots_visual.append((x,y))
        print("point captured: ",x,y)

        if len(spots)%2==0:
            cv.rectangle(img, spots[-2], spots[-1], (0,255,0), 2)
            cv.imshow("Parking Lot", img)

cv.setMouseCallback("Parking Lot", click_event)

print("Insturctions: Click Top left the bottom right of desired spot. Press 's' to save")

while True: 
    key=cv.waitKey(1)
    if key==ord('s'):
        if test:
            with open('occupied_test.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(spots)
        else:
            with open('occupied_train.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(spots)
        break 
    elif key == 27:
        break
spots = []
while True: 
    key=cv.waitKey(1)
    if key==ord('s'):
        if test:
            with open('empty_test.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(spots)
        else:
            with open('empty_train.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(spots)
        break 
    elif key == 27:
        break
cv.destroyAllWindows()



>>>>>>> ba34fcc6b10f808adbb79bbf31433af76b00ad4c
