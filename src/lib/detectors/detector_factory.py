from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from detectors.ctdet_tiny import CtdetTinyDetector

from .exdet import ExdetDetector
from .ddd import DddDetector
from .ctdet import CtdetDetector
from .multi_pose import MultiPoseDetector

detector_factory = {
    'exdet': ExdetDetector,
    'ddd': DddDetector,
    'ctdet': CtdetDetector,
    'ctdet_tiny': CtdetTinyDetector,
    'multi_pose': MultiPoseDetector,
}
