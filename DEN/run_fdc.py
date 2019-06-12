import torch
from torch.utils import data
from torchvision.transforms import Compose
from torchvision.models import resnet152
import os
import fdc
import transforms_nyu
from dataset import NyuV2, KITTIdataset
from den import DEN



data_path = '/data/nyu_v2/'

seed = 2
torch.manual_seed(seed)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
torch.cuda.set_device(4)
print(device)

depth_size = (25, 32)
model_input = 224
test_crop = (427, 561)
crop_ratios = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

transform = Compose([
    transforms_nyu.Normalize(),
    transforms_nyu.FDCPreprocess(crop_ratios)
])

transformKITTI = Compose([
    transforms_nyu.NormalizeKITTI(),
    transforms_nyu.FDCPreprocessKITTI(crop_ratios)
])

nyu = NyuV2(os.path.join(data_path, 'train'), transform=transform)
kitti = KITTIdataset(transform=transformKITTI)

# dataloader = data.DataLoader(nyu, batch_size=1, shuffle=True, num_workers=6)
dataloader = data.DataLoader(kitti, batch_size=1, shuffle=True, num_workers=0)

#wts = './models/temp_v3/042_model.pt'
resnet_wts = './models/resnet152-b121ed2d.pth'
resnet_152 = resnet152(pretrained=True)
den = DEN()
#den.load_state_dict(torch.load(wts))
den = den.to(device)
den.eval()
print('DEN has been loaded')


# fdc initialize with model den.
fdc_model = fdc.FDC(den)
f_m_hat, f = fdc_model.forward(dataloader)
fdc_model.fit(f_m_hat, f)
fdc_model.save_weights('./models/FDC/den_dbe/')

