from __future__ import division
import numpy as np
from glob import glob
import os
import scipy.misc

class kitti_gt_loader(object):
    def __init__(self, 
                 dataset_dir,
                 split,
                 img_height=256,
                 img_width=256,
                 seq_length=5):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # static_frames_file = dir_path + '/static_frames.txt'
        # test_scene_file = dir_path + '/test_scenes_' + split + '.txt'
        # with open(test_scene_file, 'r') as f:
        #     test_scenes = f.readlines()
        # self.test_scenes = [t[:-1] for t in test_scenes]
        self.dataset_dir = dataset_dir
        self.img_height = img_height
        self.img_width = img_width
        self.seq_length = seq_length
        self.cam_ids = ['02', '03']
        self.date_list = ['2011_09_26', '2011_09_28', '2011_09_29', 
                          '2011_09_30', '2011_10_03']
        # self.collect_static_frames(static_frames_file)
        self.collect_train_frames()

    # def collect_static_frames(self, static_frames_file):
    #     with open(static_frames_file, 'r') as f:
    #         frames = f.readlines()
    #     self.static_frames = []
    #     for fr in frames:
    #         if fr == '\n':
    #             continue
    #         date, drive, frame_id = fr.split(' ')
    #         curr_fid = '%.10d' % (np.int(frame_id[:-1]))
    #         for cid in self.cam_ids:
    #             self.static_frames.append(drive + ' ' + cid + ' ' + curr_fid)
        
    def collect_train_frames(self):
        all_frames = []
        # for date in self.date_list:
        drive_set = os.listdir(self.dataset_dir + "train/")
        for dr in drive_set:
            drive_dir = os.path.join(self.dataset_dir, "train", dr)
            if os.path.isdir(drive_dir):
                for cam in self.cam_ids:
                    img_dir = os.path.join(drive_dir,'proj_depth','groundtruth', 'image_' + cam)
                    N = len(glob(img_dir + '/*.png'))
                    for n in range(N):
                        frame_id = '%.10d' % n
                        all_frames.append(dr + ' ' + cam + ' ' + frame_id)

        self.train_frames = all_frames
        self.num_train = len(self.train_frames)

    def is_valid_sample(self, frames, tgt_idx):
        N = len(frames)
        tgt_drive, cid, _ = frames[tgt_idx].split(' ')
        half_offset = int((self.seq_length - 1)/2)
        min_src_idx = tgt_idx - half_offset
        max_src_idx = tgt_idx + half_offset
        if min_src_idx < 0 or max_src_idx >= N:
            return False
        min_src_drive, min_src_cid, _ = frames[min_src_idx].split(' ')
        max_src_drive, max_src_cid, _ = frames[max_src_idx].split(' ')
        if tgt_drive == min_src_drive and tgt_drive == max_src_drive and cid == min_src_cid and cid == max_src_cid:
            return True
        return False

    def get_train_example_with_idx(self, tgt_idx):
        if not self.is_valid_sample(self.train_frames, tgt_idx):
            return False
        example = self.load_example(self.train_frames, tgt_idx)
        if example is None:
            raise Exception
        return example

    def load_image_sequence(self, frames, tgt_idx, seq_length):
        half_offset = int((seq_length - 1)/2)
        image_seq = []
        zoom_x = zoom_y = None
        for o in range(-half_offset, half_offset + 1):
            curr_idx = tgt_idx + o
            curr_drive, curr_cid, curr_frame_id = frames[curr_idx].split(' ')
            curr_img = self.load_image_raw(curr_drive, curr_cid, curr_frame_id)
            if curr_img is None:
                continue
            if o == 0:
                zoom_y = self.img_height/curr_img.shape[0]
                zoom_x = self.img_width/curr_img.shape[1]
            curr_img = scipy.misc.imresize(curr_img, (self.img_height, self.img_width), interp = 'lanczos')
            image_seq.append(curr_img)
        return image_seq, zoom_x, zoom_y

    def load_example(self, frames, tgt_idx):
        image_seq, _, _ = self.load_image_sequence(frames, tgt_idx, self.seq_length)
        tgt_drive, tgt_cid, tgt_frame_id = frames[tgt_idx].split(' ')
        # intrinsics = self.load_intrinsics_raw(tgt_drive, tgt_cid, tgt_frame_id)
        # intrinsics = self.scale_intrinsics(intrinsics, zoom_x, zoom_y)
        example = {}
        #example['intrinsics'] = intrinsics
        example['image_seq'] = image_seq
        example['folder_name'] = tgt_drive + '_' + tgt_cid + '/'
        example['file_name'] = tgt_frame_id
        return example

    def load_image_raw(self, drive, cid, frame_id):
        date = drive[:10]
        # img_file = os.path.join(self.dataset_dir, date, drive, 'image_' + cid,  frame_id + '.png')
        img_file = os.path.join(self.dataset_dir, "train", drive , "proj_depth", "groundtruth", "image_"+cid, frame_id + '.png')
        try:
            img = scipy.misc.imread(img_file)
            return img
        except:
            print("There is no", img_file)



