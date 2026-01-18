<<<<<<< HEAD
import cv2 as cv
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import csv
video_path = "Video Project 4.mp4"
model_path = "parking_model.pth"
csv_files = ["empty_test.csv","occupied_test.csv"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

frame_skip=60
cap = cv.VideoCapture(video_path)
def get_model():
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(model_path , map_location=device))
    model.to(device)
    model.eval()
    return model

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

all_spots = []
for file in csv_files:
    with open(file, 'r') as f:
        data = list(csv.reader(f))
        for i in range(0, len(data), 2):
            if i+1 < len(data):
                p1 = tuple(map(int, data[i]))
                p2 = tuple(map(int, data[i+1]))
                all_spots.append((p1, p2))

model = get_model()
cap = cv.VideoCapture(video_path)
frame_count = 0
change_threshold = 4.0
# Store the last crop for each spot to compare against
last_analyzed_crops = {i: None for i in range(len(all_spots))}
# Store the last known prediction so we don't lose it
last_known_preds = {i: 0 for i in range(len(all_spots))}

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx=.5,fy=.5)
    if not ret: break

    

    if frame_count % frame_skip == 0:
        
        for i, (p1, p2) in enumerate(all_spots):
            x1,y1=p1
            x2,y2=p2
            crop = frame[min(y1,y2): max(y1,y2), min(x1, x2):max(x1,x2)]

            should_run_ai = False
            if last_analyzed_crops[i] is None:
                should_run_ai = True # First time seeing this spot
            else:
                # Calculate average pixel difference
                # We resize both to the same small size for a fast comparison
                diff = cv.absdiff(
                    cv.resize(crop, (50, 50)), 
                    cv.resize(last_analyzed_crops[i], (50, 50))
                )
                change_value = np.mean(diff)

                if change_value > change_threshold:
                    should_run_ai = True
            
            if should_run_ai:
                img_pil = Image.fromarray(cv.cvtColor(crop, cv.COLOR_BGR2RGB))
                input_tensor = preprocess(img_pil).unsqueeze(0).to(device)
                
                with torch.no_grad():
                    output = model(input_tensor)
                    _, pred = torch.max(output, 1)
                    last_known_preds[i]=pred.item()
                last_analyzed_crops[i] = crop.copy()

    # DRAW RESULTS (on every frame for smooth visuals)
    empty_count = 0
    for i, (p1, p2) in enumerate(all_spots):
        is_occupied = last_known_preds[i]
        # Label 0 is usually 'empty' and 1 is 'occupied' based on alphabetical folders
        color = (0, 0, 255) if is_occupied == 1 else (0, 255, 0)
        if is_occupied == 0: empty_count += 1
        
        cv.rectangle(frame, p1, p2, color, 2)

    # Display HUD
    cv.putText(frame, f"Available Spots: {empty_count}/{len(all_spots)}", 
                (30, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.putText(frame, f"Current Frame: {frame_count}", (50,50), cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)

    cv.imshow('Parking AI Monitor', frame)
    frame_count += 1

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
=======
import cv2 as cv
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import csv
video_path = "Video Project 4.mp4"
model_path = "parking_model.pth"
csv_files = ["empty_test.csv","occupied_test.csv"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

frame_skip=60
cap = cv.VideoCapture(video_path)
def get_model():
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(model_path , map_location=device))
    model.to(device)
    model.eval()
    return model

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

all_spots = []
for file in csv_files:
    with open(file, 'r') as f:
        data = list(csv.reader(f))
        for i in range(0, len(data), 2):
            if i+1 < len(data):
                p1 = tuple(map(int, data[i]))
                p2 = tuple(map(int, data[i+1]))
                all_spots.append((p1, p2))

model = get_model()
cap = cv.VideoCapture(video_path)
frame_count = 0
change_threshold = 4.0
# Store the last crop for each spot to compare against
last_analyzed_crops = {i: None for i in range(len(all_spots))}
# Store the last known prediction so we don't lose it
last_known_preds = {i: 0 for i in range(len(all_spots))}

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv.resize(frame, None, fx=.5,fy=.5)
    if not ret: break

    

    if frame_count % frame_skip == 0:
        
        for i, (p1, p2) in enumerate(all_spots):
            x1,y1=p1
            x2,y2=p2
            crop = frame[min(y1,y2): max(y1,y2), min(x1, x2):max(x1,x2)]

            should_run_ai = False
            if last_analyzed_crops[i] is None:
                should_run_ai = True # First time seeing this spot
            else:
                # Calculate average pixel difference
                # We resize both to the same small size for a fast comparison
                diff = cv.absdiff(
                    cv.resize(crop, (50, 50)), 
                    cv.resize(last_analyzed_crops[i], (50, 50))
                )
                change_value = np.mean(diff)

                if change_value > change_threshold:
                    should_run_ai = True
            
            if should_run_ai:
                img_pil = Image.fromarray(cv.cvtColor(crop, cv.COLOR_BGR2RGB))
                input_tensor = preprocess(img_pil).unsqueeze(0).to(device)
                
                with torch.no_grad():
                    output = model(input_tensor)
                    _, pred = torch.max(output, 1)
                    last_known_preds[i]=pred.item()
                last_analyzed_crops[i] = crop.copy()

    # DRAW RESULTS (on every frame for smooth visuals)
    empty_count = 0
    for i, (p1, p2) in enumerate(all_spots):
        is_occupied = last_known_preds[i]
        # Label 0 is usually 'empty' and 1 is 'occupied' based on alphabetical folders
        color = (0, 0, 255) if is_occupied == 1 else (0, 255, 0)
        if is_occupied == 0: empty_count += 1
        
        cv.rectangle(frame, p1, p2, color, 2)

    # Display HUD
    cv.putText(frame, f"Available Spots: {empty_count}/{len(all_spots)}", 
                (30, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.putText(frame, f"Current Frame: {frame_count}", (50,50), cv.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)

    cv.imshow('Parking AI Monitor', frame)
    frame_count += 1

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
>>>>>>> ba34fcc6b10f808adbb79bbf31433af76b00ad4c
cv.destroyAllWindows()