import os

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from barcode_dataset import BarcodeDataset

from transforms import transform_image, transform_target_barcode
from neural_network import BarcodeDecoderNeuralNetwork


def eval_loop(dataloader, model, loss_function, device):
    model.eval()

    size = len(dataloader.dataset)
    number_of_batches = len(dataloader)
    test_loss, accuracy = 0, 0

    for X, y in dataloader:

        X, y = X.to(device), y.to(device)
        prediction = model(X)
        loss = 0.0
        for i in range(13):  # Loop over each digit position
            # Compute loss for each digit. Note: y[:, i] selects the targets for the i-th digit.
            loss += loss_function(prediction[:, i, :], y[:, i])
        test_loss += loss.item()
        prediction_as_classes = prediction.argmax(2)

        correct_predictions = (prediction_as_classes == y).type(torch.float).all(1).type(torch.float).sum().item()
        accuracy += correct_predictions

    test_loss /= number_of_batches
    accuracy /= size

    print(f"Test Error: \n Accuracy: {(100 * accuracy):>0.1f}%, Avg loss: {test_loss:>8f} \n")


batch_size = 4
number_of_epochs = 5
learning_rate = 1e-3

if __name__ == '__main__':
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    print(f'Using device: {device}')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    annotations_file = os.path.join(script_dir, 'dataset/labels/annotations.csv')
    img_dir = os.path.join(script_dir, 'dataset/images')
    dataset = BarcodeDataset(
        annotations_file=annotations_file,
        img_dir=img_dir,
        transform=transform_image,
        target_transform=transform_target_barcode
    )

    torch.manual_seed(42)
    dataset_size = len(dataset)
    train_dataset_size = int(dataset_size * 0.8)
    test_dataset_size = dataset_size - train_dataset_size
    train_data, test_data = random_split(dataset, [train_dataset_size, test_dataset_size])

    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)

    model = BarcodeDecoderNeuralNetwork().to('mps')
    model.load_state_dict(torch.load('model_state_dict.pth'))
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), learning_rate)

    eval_loop(test_dataloader, model, loss_function, device)