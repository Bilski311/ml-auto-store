from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # Input size: [1, 256, 256]
        self.conv_stack = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),  # Output size: [16, 256, 256]
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # Output size: [16, 128, 128]
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),  # Output size: [32, 128, 128]
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # Output size: [32, 64, 64]
        )
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(32 * 64 * 64, 1024),  # Adjusted according to the final conv output size
            nn.ReLU(),
            nn.Linear(1024, 4)
        )

    def forward(self, x):
        x = self.conv_stack(x)
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits