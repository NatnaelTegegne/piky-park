import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageStat    
import os

# --- CONFIGURATION ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- 1. LOAD THE MODEL ---
def load_model():
    print(f"🔄 Loading Model on {DEVICE}...")
    
    model = models.resnet50(weights='DEFAULT')
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2) 
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'parking_model.pth')
    
    try:
        model.load_state_dict(torch.load(model_path, map_location=DEVICE))
        model.to(DEVICE)
        model.eval() 
        print("✅ Model Loaded Successfully!")
        return model
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find model at {model_path}")
        return None

# --- 2. DEFINE TRANSFORM ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- 3. PREDICTION FUNCTION (Internal) ---
def predict_single_crop(model, pil_crop):
    input_tensor = transform(pil_crop).unsqueeze(0).to(DEVICE) 
    with torch.no_grad():
        outputs = model(input_tensor)
        # Apply Softmax to get probabilities (confidence)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        
        occupied_confidence = probs[0][1].item()
        # THRESHOLD = 0.95
        # if occupied_confidence > THRESHOLD:
        #     return 1 # Occupied
        # else:
        #     return 0 # Free
        # probs[0][0] = Confidence it's EMPTY
        # probs[0][1] = Confidence it's OCCUPIED
        
        # We can adjust threshold here if needed (e.g., > 0.7 to count as occupied)
        _, predicted = torch.max(outputs, 1)
        
    return predicted.item()
def is_flat_asphalt(pil_crop, threshold=40):
    """
    Returns True if the image is 'boring' (low contrast/variation).
    Cars have high variation (glass, metal, shadow).
    Asphalt has low variation.
    """
    # Convert to Grayscale
    gray_img = pil_crop.convert('L')
    # Calculate Standard Deviation (Variance of pixel brightness)
    stat = ImageStat.Stat(gray_img)
    std_dev = stat.stddev[0]
    
    # Debug print (Uncomment to tune!)
    # print(f"StdDev: {std_dev:.2f}")

    # If variation is LOW, it's likely just road.
    if std_dev < threshold:
        return True
    return False

# --- 4. PUBLIC API FUNCTION ---
def analyze_frame(image_file, spots_config, model):
    if not model:
        return {}

    # 1. Open Image
    try:
        full_image = Image.open(image_file).convert('RGB')
    except Exception as e:
        print(f"❌ Error opening image file: {e}")
        return {}

    results = {}

    # 2. Iterate through all spots
    for spot_id, spot_data in spots_config.items():
        try:
            # --- SAFETY CHECK ---
            if not isinstance(spot_data, dict): continue
            coords = spot_data.get('coords') 
            if not coords or len(coords) != 4: continue
            # --------------------

            # Map to Integers
            x1, y1, x2, y2 = map(int, coords)
            
            # We cut 15 pixels off every side to avoid "seeing" neighbor cars
            # This forces the AI to look at the center of the spot
            margin = 15 
            
            crop_x1 = x1 + margin
            crop_y1 = y1 + margin
            crop_x2 = x2 - margin
            crop_y2 = y2 - margin
            
            # Safety: If spot is too small, revert to original size
            if crop_x1 >= crop_x2 or crop_y1 >= crop_y2:
                crop_x1, crop_y1, crop_x2, crop_y2 = x1, y1, x2, y2

            # Crop using the shrunken coordinates
            spot_crop = full_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))
            
            if spot_crop.size == (0,0):
                results[spot_id] = "free"
                continue
            if is_flat_asphalt(spot_crop, threshold=25):
                results[spot_id] = "free"
                continue
            # Predict
            prediction = predict_single_crop(model, spot_crop)
            
            status = "free" if prediction == 0 else "occupied"
            results[spot_id] = status
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR processing {spot_id}: {e}")
            results[spot_id] = "free"

    return results