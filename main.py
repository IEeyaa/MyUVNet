# -*- coding:utf-8 -*-
# @Author: IEeya
import pathlib
import time

from pytorch_lightning.callbacks import RichProgressBar

from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

from Net.Model import Classification
from TrainAndTest.Classification import ClassificationLoading

num_class = 26
train_root_dir = "TrainFiles1"
batch_size = 64
num_workers = 0
checkpoint = "./checkpoints/epoch=44-step=675.ckpt"
result_path = (
    pathlib.Path(__file__).parent.joinpath("results")
)

month_day = time.strftime("%m%d")
hour_min_second = time.strftime("%H%M%S")
checkpoint_callback = ModelCheckpoint(
    monitor="val_loss",
    dirpath=str(result_path.joinpath(month_day, hour_min_second)),
    filename="best",
    save_last=True,
)


def classification(method="train", max_epoch=50):
    if method == "train":
        model = Classification(num_classes=num_class)

        train_data = ClassificationLoading(folder_path=train_root_dir, json_path="./split.json", method="train")

        val_data = ClassificationLoading(folder_path=train_root_dir, json_path="./split.json", method="val")

        train_loader = train_data.get_dataloader(
            batch_size=batch_size, shuffle=True, num_workers=num_workers
        )
        val_loader = val_data.get_dataloader(
            batch_size=batch_size, shuffle=False, num_workers=num_workers
        )
        trainer = Trainer(callbacks=RichProgressBar(), max_epochs=max_epoch, logger=False)
        trainer.fit(model, train_loader, val_loader)

    elif method == "test":
        test_data = ClassificationLoading(folder_path=train_root_dir, json_path="./split.json", method="test")
        test_loader = test_data.get_dataloader(
            batch_size=batch_size, shuffle=False, num_workers=num_workers
        )
        model = Classification.load_from_checkpoint(checkpoint)
        trainer = Trainer(callbacks=checkpoint_callback)
        results = trainer.test(model=model, dataloaders=test_loader, verbose=False)
        print(
            f"Classification accuracy (%) on test set: {results[0]['test_acc'] * 100.0}"
        )


if __name__ == '__main__':
    classification("train", 1)

    # classification("test")
