from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pycocotools.coco as coco
from pycocotools.cocoeval import COCOeval
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
import torch.utils.data as data


class Tiny(data.Dataset):
    num_classes = 1
    default_resolution = [640, 512]

    mean = np.array([0.40789654, 0.44719302, 0.47026115],
                    dtype=np.float32).reshape(1, 1, 3)
    std = np.array([0.28863828, 0.27408164, 0.27809835],
                   dtype=np.float32).reshape(1, 1, 3)
    _eig_val = np.array([0.2141788, 0.01817699, 0.00341571],
                        dtype=np.float32)
    _eig_vec = np.array([
        [-0.58752847, -0.69563484, 0.41340352],
        [-0.5832747, 0.00994535, -0.81221408],
        [-0.56089297, 0.71832671, 0.41158938]
    ], dtype=np.float32)

    def __init__(self, opt, split):
        super(Tiny, self).__init__()
        self.data_dir = os.path.join(opt.data_dir, 'tiny_set/erase_with_uncertain_dataset')

        if split == 'train' or split == 'val':
            self.img_dir = os.path.join(self.data_dir, 'train')
            self.annot_path = os.path.join(self.data_dir,
                                           f'annotations/corner/task/tiny_set_train_sw640_sh512_all.json')

        elif split == 'test':
            self.img_dir = os.path.join(opt.data_dir, 'tiny_set/test')
            self.annot_path = os.path.join(self.data_dir, f'annotations/tiny_set_test_nobox.json')

        self.max_objs = 200
        self.class_name = ['person']
        self._valid_ids = [1]

        self.cat_ids = {v: i for i, v in enumerate(self._valid_ids)}

        self._data_rng = np.random.RandomState(123)

        self.split = split
        self.opt = opt

        print(f'==> initializing tiny-person {split} data.')
        self.coco = coco.COCO(self.annot_path)

        with open(os.path.join(opt.data_dir, 'tiny_set/erase_with_uncertain_dataset/val.txt'), 'r') as f:
            val_image_names = [
                line.replace('data/tiny_set/erase_with_uncertain_dataset/train/', '').strip()
                for line in f]

        imgs = [v for k, v in self.coco.imgs.items()]
        val_ids = list(map(lambda img: img['id'], list(filter(lambda img: img['file_name'] in val_image_names, imgs))))
        train_ids = list(
            map(lambda img: img['id'], list(filter(lambda img: img['file_name'] not in val_image_names, imgs))))

        img_ids = self.coco.getImgIds()
        # train_ids, val_ids = train_test_split(img_ids, test_size=0.1, random_state=123)
        # self.images = img_ids

        if split == 'train':
            self.images = train_ids
        elif split == 'val':
            self.images = val_ids
        else:
            self.images = img_ids

        self.num_samples = len(self.images)

        print('Loaded {} {} samples'.format(split, self.num_samples))

    def _to_float(self, x):
        return float("{:.2f}".format(x))

    def convert_eval_format(self, all_bboxes):
        # import pdb; pdb.set_trace()
        detections = []
        for image_id in all_bboxes:
            for cls_ind in all_bboxes[image_id]:
                category_id = self._valid_ids[cls_ind - 1]
                for bbox in all_bboxes[image_id][cls_ind]:
                    bbox[2] -= bbox[0]
                    bbox[3] -= bbox[1]
                    score = bbox[4]
                    bbox_out = list(map(self._to_float, bbox[0:4]))

                    detection = {
                        "image_id": int(image_id),
                        "category_id": int(category_id),
                        "bbox": bbox_out,
                        "score": float("{:.2f}".format(score))
                    }
                    if len(bbox) > 5:
                        extreme_points = list(map(self._to_float, bbox[5:13]))
                        detection["extreme_points"] = extreme_points
                    detections.append(detection)
        return detections

    def __len__(self):
        return self.num_samples

    def save_results(self, results, save_dir):
        json.dump(self.convert_eval_format(results),
                  open('{}/results.json'.format(save_dir), 'w'))

    def run_eval(self, results, save_dir):
        # result_json = os.path.join(save_dir, "results.json")
        # detections  = self.convert_eval_format(results)
        # json.dump(detections, open(result_json, "w"))
        self.save_results(results, save_dir)
        coco_dets = self.coco.loadRes('{}/results.json'.format(save_dir))
        coco_eval = COCOeval(self.coco, coco_dets, "bbox")
        coco_eval.evaluate()
        coco_eval.accumulate()
        coco_eval.summarize()
