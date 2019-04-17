# Generated with SMOP  0.41
from libsmop import *
from get_projection_mask import *
# crop_image.m

    # Crops the given image to use only the portion where the projected depth
# image exists.

    # Args:
#   img - either a HxW image or a HxWxD image.

    # Returns:
#   img - a cropped version of the image.

@function
def crop_image(img=None,*args,**kwargs):
    # varargin = crop_image.varargin
    # nargin = crop_image.nargin

    mask,sz=get_projection_mask(nargout=2)
# crop_image.m:10
    if 2 == ndims(img):
        img=reshape(img(mask),sz)
# crop_image.m:13
    else:
        D=size(img,3)
# crop_image.m:15
        img=reshape(img,concat([dot(480,640),D]))
# crop_image.m:16
        img=reshape(img(mask,arange()),concat([sz,D]))
# crop_image.m:17

    return img

if __name__ == '__main__':
    pass
