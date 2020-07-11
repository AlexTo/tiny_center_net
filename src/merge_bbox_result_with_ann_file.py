import argparse
import json


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_file", type=str,
                        default="exp/ctdet_tiny/default/FreeAnchorNms0.5.json",
                        required=False)
    parser.add_argument("--annotation_file", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/tiny_set_test_nobox.json",
                        required=False)

    parser.add_argument("--dst_file", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/tiny_set_test_yesbox.json",
                        required=False)

    return parser.parse_args()


if __name__ == '__main__':
    args = init_args()

    with open(args.result_file, 'r') as f:
        result = json.load(f)

    with open(args.annotation_file, 'r') as f:
        annotation = json.load(f)

    annotation['annotations'] = result

    with open(args.dst_file, 'w') as f:
        json.dump(annotation, f)
