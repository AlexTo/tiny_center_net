from pycocotools.coco import COCO

import argparse
import json

from utils.split_and_merge_image import COCOSplitImage


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotation_file", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/tiny_set_test_nobox.json",
                        required=False)
    parser.add_argument("--dst_dir", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/", required=False)
    parser.add_argument("--w", type=int, default=512, required=False)
    parser.add_argument("--h", type=int, default=640, required=False)

    return parser.parse_args()


def main():
    args = init_args()
    splitter = COCOSplitImage(sub_image_size=(args.w, args.h))
    splitter.cut_image_for_coco_json_dataset(
        src_annotation_path=args.annotation_file,
        dst_annotation_path=args.dst_dir)


if __name__ == '__main__':
    main()
