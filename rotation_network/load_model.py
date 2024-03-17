import torch
import neural_network

def load_rotation_model():
    return torch.load('model.pth')