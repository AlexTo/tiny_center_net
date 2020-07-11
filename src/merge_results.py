import argparse

from utils.split_and_merge_image import COCOMergeResult


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotation_file", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/tiny_set_test_nobox_sw512_sh640.json",
                        required=False)

    parser.add_argument("--result_file", type=str,
                        default="exp/ctdet_tiny/default/bbox.json", required=False)

    parser.add_argument("--dst_dir", type=str,
                        default="exp/ctdet_tiny/default/", required=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = init_args()
    merger = COCOMergeResult(use_nms=True)
    merger(args.annotation_file,
           args.result_file,
           args.dst_dir)
