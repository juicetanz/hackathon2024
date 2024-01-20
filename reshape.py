import torch
import torch.nn

def reshape_model(model, num_classes):
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    print("=> reshaped ResNet fully-connected layer with: " + str(model.fc))
    return model