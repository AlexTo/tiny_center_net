import argparse


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_file", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/tiny_set_test_nobox.json",
                        required=False)
    parser.add_argument("--dst_dir", type=str,
                        default="data/tiny_set/erase_with_uncertain_dataset/annotations/", required=False)
    parser.add_argument("--w", type=int, default=512, required=False)
    parser.add_argument("--h", type=int, default=640, required=False)

    return parser.parse_args()