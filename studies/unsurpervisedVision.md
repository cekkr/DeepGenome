Creating a PyTorch model from scratch that automatically categorizes features extracted from a series of images without using any pre-trained models involves unsupervised learning. One common approach to this problem is to use an autoencoder. An autoencoder learns to compress the image data into a lower-dimensional latent space and then reconstructs the image back from this space. The latent space representations can then be used to cluster the images, essentially categorizing them based on learned features.

Here's a step-by-step breakdown to build and train a simple convolutional autoencoder for this task:

### 1. Import Necessary Libraries
```python
import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
```

### 2. Define the Autoencoder
Here, we define a simple convolutional autoencoder. The encoder compresses the image, and the decoder tries to reconstruct it.

```python
class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),  # output: [16, 16, 16]
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),  # output: [32, 8, 8]
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),  # output: [64, 4, 4]
            nn.ReLU(),
            nn.Flatten(),  # output: 1024
            nn.Linear(64 * 4 * 4, 128),
            nn.ReLU()
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(128, 64 * 4 * 4),
            nn.ReLU(),
            nn.Unflatten(1, (64, 4, 4)),
            nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 3, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()  # Use sigmoid to scale the output to [0, 1]
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x
```

### 3. Data Loading
You'll need to set up your dataset. Assuming you have a folder with images:

```python
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Resize images
    transforms.ToTensor()
])

dataset = ImageFolder(root='path_to_images', transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

### 4. Model Training
Instantiate the model, define the loss function and optimizer, and start training:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Autoencoder().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 50
for epoch in range(epochs):
    for data, _ in dataloader:
        img = data.to(device)
        # Forward pass
        output = model(img)
        loss = criterion(output, img)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
```

### 5. Feature Extraction and Clustering
After training, you can use the encoder part of the model to extract features and apply clustering algorithms like K-means to categorize images based on the learned features.

This example provides a basic framework. You might need to tweak the architecture, training parameters, and possibly the complexity of the model depending on the specifics of your dataset and the level of feature abstraction required.
