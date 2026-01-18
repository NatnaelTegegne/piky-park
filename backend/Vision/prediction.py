<<<<<<< HEAD
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import csv

# --- CONFIGURATION ---
MODEL_PATH = 'parking_model.pth'
IMAGE_PATH = 'vlcsnap-2026-01-18-00h46m52s266.png'  # The image you want to check
# List all CSVs you want to monitor. Usually, you want to monitor ALL spots.
CSV_FILES = ['empty_test.csv', 'occupied_test.csv'] 
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- 1. LOAD THE MODEL ---
def load_model():
    # We must redefine the model structure exactly as we did in training
    model = models.resnet50(weights='DEFAULT') # Pretrained doesn't matter here, we are loading weights
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2) # Output layer (Empty vs Full)
    
    # Load the trained weights
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval() # Set to evaluation mode (important!)
    return model

# --- 2. DEFINE TRANSFORM ---
# Must match the transform used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- 3. PREDICTION FUNCTION ---
def predict_spot(model, crop_img):
    # Convert OpenCV image (BGR) to PIL Image (RGB)
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(crop_img)
    
    # Prepare image for model
    input_tensor = transform(pil_img).unsqueeze(0).to(DEVICE) # Add batch dimension
    
    with torch.no_grad(): # Disable gradient calculation for speed
        outputs = model(input_tensor)
        # Get the index of the highest score (0 or 1)
        _, predicted = torch.max(outputs, 1)
        
    return predicted.item()

# --- 4. MAIN LOOP ---
def main():
    model = load_model()
    image = cv2.imread(IMAGE_PATH)
    image = cv2.resize(image, None, fx=.5,fy=.5)
    
    # Combine coordinates from all CSVs into one list
    all_spots = []
    for csv_file in CSV_FILES:
        with open(csv_file, 'r') as f:
            reader = list(csv.reader(f))
            for i in range(0, len(reader), 2):
                if i+1 < len(reader):
                    p1 = tuple(map(int, reader[i]))
                    p2 = tuple(map(int, reader[i+1]))
                    all_spots.append((p1, p2))

    print(f"Checking {len(all_spots)} parking spots...")

    # Iterate over every spot
    for p1, p2 in all_spots:
        x1, y1 = p1
        x2, y2 = p2
        
        # Ensure coordinates are ordered correctly for slicing
        x_start, x_end = sorted([x1, x2])
        y_start, y_end = sorted([y1, y2])
        
        # Crop the spot
        spot_crop = image[y_start:y_end, x_start:x_end]
        
        # Check if crop is valid (not 0 size)
        if spot_crop.size == 0: continue

        # Predict
        prediction = predict_spot(model, spot_crop)
        
        # Draw Result
        # Assumption: 0 = Empty, 1 = Occupied (Check your training class_to_idx to be sure!)
        # Usually ImageFolder sorts alphabetically: Empty=0, Occupied=1
        if prediction == 0: 
            color = (0, 255, 0) # Green for Empty
            label = "Empty"
        else:
            color = (0, 0, 255) # Red for Occupied
            label = "Occupied"
            
        cv2.rectangle(image, p1, p2, color, 2)

    # Show the final result
    print("done")
    cv2.imshow("Parking Prediction", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
=======
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import csv

# --- CONFIGURATION ---
MODEL_PATH = 'parking_model.pth'
IMAGE_PATH = 'vlcsnap-2026-01-18-00h46m52s266.png'  # The image you want to check
# List all CSVs you want to monitor. Usually, you want to monitor ALL spots.
CSV_FILES = ['empty_test.csv', 'occupied_test.csv'] 
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- 1. LOAD THE MODEL ---
def load_model():
    # We must redefine the model structure exactly as we did in training
    model = models.resnet50(weights='DEFAULT') # Pretrained doesn't matter here, we are loading weights
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2) # Output layer (Empty vs Full)
    
    # Load the trained weights
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval() # Set to evaluation mode (important!)
    return model

# --- 2. DEFINE TRANSFORM ---
# Must match the transform used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- 3. PREDICTION FUNCTION ---
def predict_spot(model, crop_img):
    # Convert OpenCV image (BGR) to PIL Image (RGB)
    crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(crop_img)
    
    # Prepare image for model
    input_tensor = transform(pil_img).unsqueeze(0).to(DEVICE) # Add batch dimension
    
    with torch.no_grad(): # Disable gradient calculation for speed
        outputs = model(input_tensor)
        # Get the index of the highest score (0 or 1)
        _, predicted = torch.max(outputs, 1)
        
    return predicted.item()

# --- 4. MAIN LOOP ---
def main():
    model = load_model()
    image = cv2.imread(IMAGE_PATH)
    image = cv2.resize(image, None, fx=.5,fy=.5)
    
    # Combine coordinates from all CSVs into one list
    all_spots = []
    for csv_file in CSV_FILES:
        with open(csv_file, 'r') as f:
            reader = list(csv.reader(f))
            for i in range(0, len(reader), 2):
                if i+1 < len(reader):
                    p1 = tuple(map(int, reader[i]))
                    p2 = tuple(map(int, reader[i+1]))
                    all_spots.append((p1, p2))

    print(f"Checking {len(all_spots)} parking spots...")

    # Iterate over every spot
    for p1, p2 in all_spots:
        x1, y1 = p1
        x2, y2 = p2
        
        # Ensure coordinates are ordered correctly for slicing
        x_start, x_end = sorted([x1, x2])
        y_start, y_end = sorted([y1, y2])
        
        # Crop the spot
        spot_crop = image[y_start:y_end, x_start:x_end]
        
        # Check if crop is valid (not 0 size)
        if spot_crop.size == 0: continue

        # Predict
        prediction = predict_spot(model, spot_crop)
        
        # Draw Result
        # Assumption: 0 = Empty, 1 = Occupied (Check your training class_to_idx to be sure!)
        # Usually ImageFolder sorts alphabetically: Empty=0, Occupied=1
        if prediction == 0: 
            color = (0, 255, 0) # Green for Empty
            label = "Empty"
        else:
            color = (0, 0, 255) # Red for Occupied
            label = "Occupied"
            
        cv2.rectangle(image, p1, p2, color, 2)

    # Show the final result
    print("done")
    cv2.imshow("Parking Prediction", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
>>>>>>> ba34fcc6b10f808adbb79bbf31433af76b00ad4c
    main()