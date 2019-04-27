from PIL import Image
import torch
import numpy as np
path = 'image/path'
depth = np.array(Image.open(path)).unsqueeze(0)
deptharr = torch.from_numpy((depth)).type('torch.DoubleTensor')

m = torch.nn.MaxPool2d(3,2)
output = m(deptharr)
output = output.squeeze()
img = Image.fromarray(output).convert('L').resize((416,128))
depth = np.asarray(img)