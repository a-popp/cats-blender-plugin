# MIT License
#
# Copyright (c) 2017 GiveMeAllYourCats
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Code author: Shotariya
# Repo: https://github.com/Grim-es/shotariya
# Edits by: GiveMeAllYourCats, Hotox
# Repo: https://github.com/michaeldegroot/cats-blender-plugin

# Bone names that are never deleted by the zero-weight-bone cleanup.
dont_delete_these_bones = [
    'Hips', 'Spine', 'Chest', 'Upper Chest', 'Neck', 'Head',
    'Left leg', 'Left knee', 'Left ankle', 'Left toe',
    'Right leg', 'Right knee', 'Right ankle', 'Right toe',
    'Left shoulder', 'Left arm', 'Left elbow', 'Left wrist',
    'Right shoulder', 'Right arm', 'Right elbow', 'Right wrist',
    'OldRightEye', 'OldLeftEye', 'LeftEye', 'RightEye', 'Eye_L', 'Eye_R',
    'Left leg 2', 'Right leg 2',

    'Thumb0_L', 'Thumb1_L', 'Thumb2_L',
    'IndexFinger1_L', 'IndexFinger2_L', 'IndexFinger3_L',
    'MiddleFinger1_L', 'MiddleFinger2_L', 'MiddleFinger3_L',
    'RingFinger1_L', 'RingFinger2_L', 'RingFinger3_L',
    'LittleFinger1_L', 'LittleFinger2_L', 'LittleFinger3_L',

    'Thumb0_R', 'Thumb1_R', 'Thumb2_R',
    'IndexFinger1_R', 'IndexFinger2_R', 'IndexFinger3_R',
    'MiddleFinger1_R', 'MiddleFinger2_R', 'MiddleFinger3_R',
    'RingFinger1_R', 'RingFinger2_R', 'RingFinger3_R',
    'LittleFinger1_R', 'LittleFinger2_R', 'LittleFinger3_R',

    'Breast_L', 'Breast_R',
]
dont_delete_these_main_bones = [
    'Hips', 'Spine', 'Chest', 'Upper Chest', 'Neck', 'Head',
    'Left leg', 'Left knee', 'Left ankle', 'Left toe',
    'Right leg', 'Right knee', 'Right ankle', 'Right toe',
    'Left shoulder', 'Left arm', 'Left elbow', 'Left wrist',
    'Right shoulder', 'Right arm', 'Right elbow', 'Right wrist',
    'LeftEye', 'RightEye', 'Eye_L', 'Eye_R',
    'Left leg 2', 'Right leg 2',

    'Thumb0_L', 'Thumb1_L', 'Thumb2_L',
    'IndexFinger1_L', 'IndexFinger2_L', 'IndexFinger3_L',
    'MiddleFinger1_L', 'MiddleFinger2_L', 'MiddleFinger3_L',
    'RingFinger1_L', 'RingFinger2_L', 'RingFinger3_L',
    'LittleFinger1_L', 'LittleFinger2_L', 'LittleFinger3_L',

    'Thumb0_R', 'Thumb1_R', 'Thumb2_R',
    'IndexFinger1_R', 'IndexFinger2_R', 'IndexFinger3_R',
    'MiddleFinger1_R', 'MiddleFinger2_R', 'MiddleFinger3_R',
    'RingFinger1_R', 'RingFinger2_R', 'RingFinger3_R',
    'LittleFinger1_R', 'LittleFinger2_R', 'LittleFinger3_R',
]
bone_finger_list = [
    'Thumb0_',
    'IndexFinger1_',
    'MiddleFinger1_',
    'RingFinger1_',
    'LittleFinger1_',

    'Thumb1_',
    'IndexFinger2_',
    'MiddleFinger2_',
    'RingFinger2_',
    'LittleFinger2_',

    'Thumb2_',
    'IndexFinger3_',
    'MiddleFinger3_',
    'RingFinger3_',
    'LittleFinger3_',
]
