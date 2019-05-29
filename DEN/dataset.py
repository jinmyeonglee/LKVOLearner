import os
import pickle
from torch.utils import data
import numpy as np
from PIL import Image
from skimage import transform

class NyuV2(data.Dataset):

    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
    
    def __len__(self):
        return len(os.listdir(os.path.join(self.root_dir, 'images')))
    
    def __getitem__(self, index):
        with open(os.path.join(self.root_dir, 'images', '{:05d}.p'.format(index)), 'rb') as f_img:
            img = pickle.load(f_img)

        with open(os.path.join(self.root_dir, 'depths', '{:05d}.p'.format(index)), 'rb') as f_depth:
            depth = pickle.load(f_depth)

        sample = {'image': img, 'depth': depth}

        if self.transform:
            sample = self.transform(sample)
        
        return sample


class KITTIdataset(data.Dataset):
    """KITTIdataset"""
    def __init__(self, list_file='train.txt', data_root_path='/data/raw_data_prepared', img_size=[128, 416], bundle_size=3, transform=None):
        self.gt_root_path='/data/gt_data_prepared'
        self.data_root_path = data_root_path
        self.img_size = img_size
        self.bundle_size = bundle_size
        self.frame_pathes = []
        self.transform = transform
        list_file = os.path.join(data_root_path, list_file)
        with open(list_file) as file:
            for line in file:
                frame_path = line.strip()
                seq_path, frame_name = frame_path.split(" ")
                # print(seq_path)
                if seq_path in ['2011_09_26_drive_0119_sync_02', '2011_09_28_drive_0225_sync_02',
                                '2011_09_29_drive_0108_sync_02', '2011_09_30_drive_0072_sync_02',
                                '2011_10_03_drive_0058_sync_02', '2011_09_29_drive_0108_sync_03']:
                    print(seq_path)
                    continue
                frame_path = os.path.join(seq_path, frame_name)
                self.frame_pathes.append(frame_path)

    def __len__(self):
        return len(self.frame_pathes)

    def __getitem__(self, item):
        # read camera intrinsics
        cam_file = os.path.join(self.data_root_path, self.frame_pathes[item]+'_cam.txt')
        with open(cam_file) as file:
            cam_intrinsics = [float(x) for x in next(file).split(',')]
        camparams = np.asarray(cam_intrinsics)

        # read image bundle
        img_file = os.path.join(self.data_root_path, self.frame_pathes[item]+'.jpg')
        seq, frame = self.frame_pathes[item].split("/")
        gt_file = os.path.join(self.gt_root_path,self.frame_pathes[item]+'.jpg')
        frames_cat = np.array(Image.open(img_file))
        depth_cat = np.array(Image.open(gt_file))
        depth_cat = transform.resize(depth_cat, frames_cat.shape, mode='reflect', anti_aliasing=True)

        # slice the image into #bundle_size number of images
        frame_list = []
        depth_list = []

        for i in range(self.bundle_size):
            frame_list.append(frames_cat[:,i*self.img_size[1]:(i+1)*self.img_size[1],:])  #crop image by (height * 416)*3
            depth_list.append(depth_cat[:,i*self.img_size[1]:(i+1)*self.img_size[1]])
            #print(frame_list[i].shape, depth_list[i].shape)
            
        frames = np.asarray(frame_list).astype(float).transpose(0, 3, 1, 2)
        
        depth = np.asarray(depth_list).astype(float)
        
        sample = {'frames': frames, 'depth':depth}

        if self.transform:
            sample = self.transform(sample)
    
        #frames : frame list, depth : depth list , camparams : cam_intrinsics
        return sample, camparams
