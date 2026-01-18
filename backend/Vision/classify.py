<<<<<<< HEAD
import cv2
import csv
import os

# 1. SETUP: Define file paths
# Change 'parking_lot.jpg' to your actual image filename
source_image_path = 'vlcsnap-2026-01-17-23h54m15s078.png'
empty_csv = 'empty_train.csv'
occupied_csv = 'occupied_train.csv'

# Create the folder structure PyTorch needs
os.makedirs('dataset_train/empty', exist_ok=True)
os.makedirs('dataset_train/occupied', exist_ok=True)

# Load the big image
img = cv2.imread(source_image_path)
img = cv2.resize(img, None, fx=.5,fy=.5)

if img is None:
    print("Error: Could not find the image file!")
    exit()

def create_crops(csv_path, save_folder):
    with open(csv_path, 'r') as f:
        reader = list(csv.reader(f))
        
        # We assume the CSV format from the previous step:
        # Row 1: Top-Left (x, y)
        # Row 2: Bottom-Right (x, y)
        # Row 3: Top-Left (x, y)... etc.
        
        count = 0
        # Iterate through the list in steps of 2 (Coordinate pairs)
        for i in range(0, len(reader), 2):
            if i+1 >= len(reader): break # Safety check
            
            # Parse coordinates
            x1, y1 = map(int, reader[i])
            x2, y2 = map(int, reader[i+1])
            if y1==y2:
                y1+=1
            if x1==x2:
                x1+=1
            # 2. CROP: Slice the image array
            # Ensure coordinates are in the right order (min to max)
            x_start, x_end = sorted([x1, x2])
            y_start, y_end = sorted([y1, y2])
            
            
            crop = img[y_start:y_end, x_start:x_end]
            
            # 3. SAVE: Write the crop to the specific folder
            filename = f"{save_folder}/spot_{count}.jpg"
            print(y_start,y_end,x_start,x_end)
            cv2.imwrite(filename, crop)
            count += 1
            
    print(f"Finished! Created {count} images in {save_folder}")

# Run the function for both CSVs
print("Processing Empty spots...")
create_crops(empty_csv, 'dataset_train/empty')

print("Processing Occupied spots...")
create_crops(occupied_csv, 'dataset_train/occupied')
=======
import cv2
import csv
import os

# 1. SETUP: Define file paths
# Change 'parking_lot.jpg' to your actual image filename
source_image_path = 'vlcsnap-2026-01-17-23h54m15s078.png'
empty_csv = 'empty_train.csv'
occupied_csv = 'occupied_train.csv'

# Create the folder structure PyTorch needs
os.makedirs('dataset_train/empty', exist_ok=True)
os.makedirs('dataset_train/occupied', exist_ok=True)

# Load the big image
img = cv2.imread(source_image_path)
img = cv2.resize(img, None, fx=.5,fy=.5)

if img is None:
    print("Error: Could not find the image file!")
    exit()

def create_crops(csv_path, save_folder):
    with open(csv_path, 'r') as f:
        reader = list(csv.reader(f))
        
        # We assume the CSV format from the previous step:
        # Row 1: Top-Left (x, y)
        # Row 2: Bottom-Right (x, y)
        # Row 3: Top-Left (x, y)... etc.
        
        count = 0
        # Iterate through the list in steps of 2 (Coordinate pairs)
        for i in range(0, len(reader), 2):
            if i+1 >= len(reader): break # Safety check
            
            # Parse coordinates
            x1, y1 = map(int, reader[i])
            x2, y2 = map(int, reader[i+1])
            if y1==y2:
                y1+=1
            if x1==x2:
                x1+=1
            # 2. CROP: Slice the image array
            # Ensure coordinates are in the right order (min to max)
            x_start, x_end = sorted([x1, x2])
            y_start, y_end = sorted([y1, y2])
            
            
            crop = img[y_start:y_end, x_start:x_end]
            
            # 3. SAVE: Write the crop to the specific folder
            filename = f"{save_folder}/spot_{count}.jpg"
            print(y_start,y_end,x_start,x_end)
            cv2.imwrite(filename, crop)
            count += 1
            
    print(f"Finished! Created {count} images in {save_folder}")

# Run the function for both CSVs
print("Processing Empty spots...")
create_crops(empty_csv, 'dataset_train/empty')

print("Processing Occupied spots...")
create_crops(occupied_csv, 'dataset_train/occupied')
>>>>>>> ba34fcc6b10f808adbb79bbf31433af76b00ad4c
