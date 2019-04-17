# Generated with SMOP  0.41
from libsmop import *
# get_projection_mask.m

    # Gets a mask for the projected images that is most conservative with
# respect to the regions that maintain the kinect depth signal following
# projection.
    
    # Returns: 
#   mask - HxW binary image where the projection falls.
#   sz - the size of the valid region.
    
@function
def get_projection_mask(*args,**kwargs):
    # varargin = get_projection_mask.varargin
    # nargin = get_projection_mask.nargin

    mask=false(480,640)
# get_projection_mask.m:9
    mask[arange(45,471),arange(41,601)]=1
# get_projection_mask.m:10
    sz=concat([427,561])
# get_projection_mask.m:12
    return mask,sz
    
if __name__ == '__main__':
    pass
    