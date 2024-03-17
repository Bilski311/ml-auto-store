import os

import torch

from torch import nn
from rotation_dataset import RotationDataset
from transforms import transform_image
from torch.utils.data import random_split, DataLoader

from neural_network import NeuralNetwork
batch_size = 64
learning_rate = 1e-3
epochs = 40


def train_loop(dataloader, model, loss_function, optimizer, device):
    size = len(dataloader.dataset)

    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        prediction = model(X)
        loss = loss_function(prediction, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if is_last_batch(batch, dataloader):
            loss = loss.item()
            current = batch * batch_size + len(X)
            print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")


def is_last_batch(batch, dataloader):
    return batch == len(dataloader) - 1

def validation_loop(dataloader, model, loss_function, device):
    model.eval()
    size = len(dataloader.dataset)
    number_of_batches = len(dataloader)
    test_loss, accuracy = 0, 0

    for X, y in dataloader:

        X, y = X.to(device), y.to(device)
        prediction = model(X)
        test_loss += loss_function(prediction, y).item()
        accuracy += (prediction.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= number_of_batches
    accuracy /= size

    print(f"Test Error: \n Accuracy: {(100 * accuracy):>0.1f}%, Avg loss: {test_loss:>8f} \n")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    annotations_file = os.path.join(script_dir, '../detected_barcodes/annotation/annotations.csv')
    img_dir = os.path.join(script_dir, '../detected_barcodes/img')

    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f'Using device: {device}')

    dataset = RotationDataset(
        annotations_file=annotations_file,
        img_dir=img_dir,
        transform=transform_image
    )
    torch.manual_seed(42)
    dataset_size = len(dataset)
    print(int(dataset_size * 0.8))
    train_data, test_data = random_split(dataset, [int(dataset_size * 0.8), int(dataset_size * 0.2) + 1])
    print(f'Training data size: {len(train_data)}')
    print(f'Test data size: {len(test_data)}')
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)
    model = NeuralNetwork().to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    for epoch in range(1, epochs + 1):
        print(f'Epoch: {epoch}')
        train_loop(train_dataloader, model, loss_function, optimizer, device)
        validation_loop(test_dataloader, model, loss_function, device)

    print('Done!')
    print("Saving the model...")
    torch.save(model, 'model.pth')
