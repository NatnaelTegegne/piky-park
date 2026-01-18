import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models

first_train=False
# 1. SETUP: Define how to transform images for the model
# ResNet expects images to be 224x224 and normalized
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 2. DATA: Load the images from your folders
# CHANGE 'dataset' to the path where you saved your empty/occupied folders
dataset = datasets.ImageFolder('dataset_train', transform=transform)

# Split into training (80%) and validation (20%) sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_data, val_data = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)
if first_train:
    # 3. MODEL: Load a pre-trained ResNet and adjust the final layer
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

    # Freeze early layers (so we don't 'forget' basic shapes)
    for param in model.parameters():
        param.requires_grad = False

    # Replace the last layer (fc) to output only 2 classes (Empty vs Full)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2) 

    # 4. TRAINING SETUP
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()      # The "calculator" for error
    optimizer = optim.Adam(model.fc.parameters(), lr=0.001) # The "corrector"
else: 
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    num_features=model.fc.in_features
    model.fc=nn.Linear(num_features, 2)

    model.load_state_dict(torch.load("parking_model.pth"))
    model.train()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    for param in model.parameters():
        param.requires_grad = True

    optimizer = optim.Adam(model.parameters(), lr = 0.0001)
    criterion = nn.CrossEntropyLoss()
# 5. THE LOOP: Train for 5 epochs
num_epochs = 10
print(f"Training on {device}...")

for epoch in range(num_epochs):
    model.train() # Set model to training mode
    running_loss = 0.0
    
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        
        # A. Forward pass (Guess)
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # B. Backward pass (Learn)
        optimizer.zero_grad() # Clear previous calculations
        loss.backward()       # Calculate gradients
        optimizer.step()      # Update weights
        
        running_loss += loss.item()
    
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader):.4f}")

# 6. SAVE: Save the trained model for later use
torch.save(model.state_dict(), "parking_model.pth")
print("Model saved as parking_model.pth!")