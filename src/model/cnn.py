import torch
import torch.nn as nn
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = self._make_layer(1,64)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.layer2 = self._make_layer(64,128)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2,stride=2)
        self.layer3 = self._make_layer(128,256)
        self.avgpool = nn.AdaptiveAvgPool2d((1,1))

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256,64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64,36)
        )

    def forward(self,x):
        x = self.layer1(x)   # B 64 28 28
        x = self.maxpool1(x) # B 64 14 14
        x = self.layer2(x)   # B 128 14 14
        x = self.maxpool2(x) # B 128 7 7
        x = self.layer3(x)   # B 256 7 7
        x = self.avgpool(x)  # B 256 1 1
        x = self.fc(x)       # B 26
        return x

    def _make_layer(self,in_channels,out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels=in_channels,out_channels=out_channels,kernel_size=3,stride=1,padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Dropout(0.2)
        )