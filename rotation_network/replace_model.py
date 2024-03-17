import torch
if __name__ == '__main__':
    model = torch.load('model.pth')
    torch.save(model.state_dict(), 'model_state_dict.pth')