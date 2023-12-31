import dl_project
import torch.nn as nn
import torch
import pytorch_lightning as pl
from sklearn.metrics import f1_score


class ASLModel(pl.LightningModule):
    def __init__(
        self,
        model: str = "resnet",
        lr: float = 2e-4
    ):
        super().__init__()
        if model == "resnet":
            self.model = dl_project.ResNet()
        elif model == "cnn":
            self.model = dl_project.CNN()
        elif model == "vit":
            self.model = dl_project.VisionTransformer()
        elif model == "mobilenetv1":
            self.model = dl_project.MobileNetV1()
        elif model == "mobilenetv2":
            self.model = dl_project.MobileNetV2()
        elif model == "swin":
            self.model = dl_project.SwinTransformerBackbone()

        self.train_loss = dl_project.RunningMean()
        self.val_loss = dl_project.RunningMean()
        self.train_acc = dl_project.RunningMean()
        self.val_acc = dl_project.RunningMean()
        self.train_f1 = dl_project.RunningMean()
        self.val_f1 = dl_project.RunningMean()

        self.loss = nn.CrossEntropyLoss()
        self.lr = lr

    def forward(self, x):
        return self.model(x)

    def _cal_loss_and_acc(self, batch):
        x, y = batch
        y_hat = self(x)
        loss = self.loss(y_hat, y)
        with torch.no_grad():
            acc = (y_hat.argmax(dim=1) == y).float().mean()
            f1 = float(f1_score(y.cpu(), y_hat.argmax(dim=1).cpu(), average="macro"))
        return loss, acc, f1

    def training_step(self, batch, batch_idx):
        loss, acc, f1 = self._cal_loss_and_acc(batch)
        self.train_loss.update(loss.item(), batch[0].shape[0])
        self.train_acc.update(acc.item(), batch[0].shape[0])
        self.train_f1.update(f1, batch[0].shape[0])
        return loss

    def validation_step(self, batch, batch_idx):
        loss, acc, f1 = self._cal_loss_and_acc(batch)
        self.val_loss.update(loss.item(), batch[0].shape[0])
        self.val_acc.update(acc.item(), batch[0].shape[0])
        self.val_f1.update(f1, batch[0].shape[0])
        return loss

    def on_train_epoch_end(self):
        self.log("train_loss", self.train_loss(), sync_dist=True)
        self.log("train_acc", self.train_acc(), sync_dist=True)
        self.log("train_f1", self.train_f1(), sync_dist=True)
        self.train_loss.reset()
        self.train_acc.reset()
        self.train_f1.reset()

    def on_validation_epoch_end(self):
        self.log("val_loss", self.val_loss(), sync_dist=True)
        self.log("val_acc", self.val_acc(), sync_dist=True)
        self.log("val_f1", self.val_f1(), sync_dist=True)
        self.val_loss.reset()
        self.val_acc.reset()
        self.val_f1.reset()

    def test_step(self, batch, batch_idx):
        loss, acc, f1 = self._cal_loss_and_acc(batch)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)
