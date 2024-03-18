import torch
import torch.nn.functional as F
from torch import nn


class BarcodeDecoderNeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.flatten = torch.flatten
        self.classifier = nn.Sequential(
            nn.Linear(in_features=32 * 64 * 64, out_features=512),
            nn.ReLU(),
            nn.Linear(in_features=512, out_features=130)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.flatten(x, start_dim=1)
        x = self.classification(x)
        x = x.view(-1, 13, 10)

        return x
