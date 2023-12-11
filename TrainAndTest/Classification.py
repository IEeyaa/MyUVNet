# -*- coding:utf-8 -*-
# @Author: IEeya
import json
import os
import re

import dgl
import torch
from torch import FloatTensor
from torch.utils.data import Dataset, DataLoader

from UVGraph.modelToGraph import load_from_dgl_file

CHAR2LABEL = {
        'Bearnings': 0,
        'Bolts': 1,
        'Boxes': 2,
        'Brackets': 3,
        'Bushing': 4,
        'Bushing_Damping_Liners': 5,
        'Collets': 6,
        'Cotter_Pin': 7,
        'External Retaining Rings': 8,
        'Eyesbolts With Shoulders': 9,
        'Gasket': 10,
        'Gear Rod Stock': 11,
        'Gears': 12,
        'Grommets': 13,
        'HeadlessScrews': 14,
        'Hex_Head_Screws': 15,
        'Holebolts With Shoulders': 16,
        'Idler Sprocket': 17,
        'Keyway_Shaft': 18,
        'Machine_Key': 19,
        'Miter Gear Set Screw': 20,
        'Nuts': 21,
        'O_Rings': 22,
        'Pipes': 23,
        'Pipe_fittings': 24,
        'Pipe_Joints': 25,
        'Rectangular Gear Rack': 26,
        'Rollers': 27,
        'Rotary_Shaft': 28,
        'Routing EyeBolts Bent Closed Eye': 29,
        'Shaft_Collar': 30,
        'Sleeve Washers': 31,
        'Slotted_Flat_Head_Screws': 32,
        'Socket-Connect Flanges': 33,
        'Socket_Head_Screws': 34,
        'Sprocket Taper-Lock Bushing': 35,
        'Strut Channel Floor Mount': 36,
        'Strut Channel Side-Side': 37,
        'Tag Holder': 38,
        'Thumb_Screws': 39,
        'Washers': 40,
        'Webbing Guide': 41,
        'Wide Grip External Retaining Ring': 42,
        }


def get_all_graph_files(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list


def load_one_graph(file_name, bin_path):
    data = load_from_dgl_file(file_name, bin_path)[0]
    data.ndata["x"] = data.ndata["x"].type(FloatTensor)
    data.edata["x"] = data.edata["x"].type(FloatTensor)
    return data


def _collate(batch):
    batched_graph = dgl.batch([sample["graph"] for sample in batch])
    batched_filenames = [sample["filename"] for sample in batch]
    batched_labels = torch.cat([sample["label"] for sample in batch], dim=0)
    return {"graph": batched_graph, "filename": batched_filenames, "label": batched_labels}


class ClassificationLoading(Dataset):
    def __init__(
            self,
            folder_path,
            json_path,
            method="train",
    ):
        self.method = method
        self.datas = []
        self.load_all_graphs(folder_path, json_path),

    def __len__(self):
        return len(self.datas)


    def __getitem__(self, idx):
        sample = self.datas[idx]
        return sample

    def load_all_graphs(self, folder_path, json_path):

        with open(json_path, "r") as json_file:
            graph_file_names = (json.load(json_file))[self.method]

        graphs = [load_one_graph(graph_file_name + ".bin", folder_path) for graph_file_name in graph_file_names]
        labels = [re.match(r'([a-zA-Z_]+)_\d+', graph_file_name).group(1) for graph_file_name in graph_file_names]
        for i in range(0, len(graphs)):
            self.datas.append({
                "graph": graphs[i],
                "filename": graph_file_names[i],
                "label": torch.tensor([CHAR2LABEL.get(labels[i], -1)])
            })

    def get_dataloader(self, batch_size=64, shuffle=True, num_workers=0):
        return DataLoader(
            self,
            batch_size=batch_size,
            shuffle=shuffle,
            collate_fn=_collate,
            num_workers=num_workers,  # Can be set to non-zero on Linux
            drop_last=True,
        )


# 指定文件夹路径
if __name__ == '__main__':
    # 生成目录文件
    folder_path_test = "../RawFiles"
    for _, names, _ in os.walk(folder_path_test):
        for index, item in enumerate(names):
            print("'{}': {},".format(item, index))
        break
