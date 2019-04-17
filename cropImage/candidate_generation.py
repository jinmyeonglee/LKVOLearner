# Generated with SMOP  0.41
from libsmop import *
# candidate_generation.m

    
@function
def candidate_generation(cropped_depths=None,*args,**kwargs):
    # varargin = candidate_generation.varargin
    # nargin = candidate_generation.nargin

    cropped_depths=- (225 - dot(20,cropped_depths)) ** 0.5 + 15
# candidate_generation.m:3
    
    im_size=concat([427,561])
# candidate_generation.m:5
    
    candidates=zeros(concat([im_size,18]))
# candidate_generation.m:6
    index_batch=0
# candidate_generation.m:8
    for index_candidate in arange(1,18).reshape(-1):
        temp_candidate=candidates(arange(),arange(),index_candidate)
# candidate_generation.m:10
        temp_weight=copy(temp_candidate)
# candidate_generation.m:11
        crop_ratio=1 - dot(0.05,(ceil(index_candidate / 2) - 1))
# candidate_generation.m:13
        crop_size=round(dot(im_size,crop_ratio))
# candidate_generation.m:14
        if crop_ratio == 1:
            index_batch=index_batch + 1
# candidate_generation.m:16
            temp_candidate=imresize(cropped_depths(arange(),arange(),index_batch),crop_size,'bilinear')
# candidate_generation.m:17
        else:
            if crop_ratio < 1:
                # left-up side
                index_batch=index_batch + 1
# candidate_generation.m:21
                temp_candidate[arange(1,crop_size(1)),arange(1,crop_size(2))]=temp_candidate(arange(1,crop_size(1)),arange(1,crop_size(2))) + imresize(cropped_depths(arange(),arange(),index_batch),crop_size,'bilinear')
# candidate_generation.m:23
                temp_weight[arange(1,crop_size(1)),arange(1,crop_size(2))]=temp_weight(arange(1,crop_size(1)),arange(1,crop_size(2))) + 1
# candidate_generation.m:26
                index_batch=index_batch + 1
# candidate_generation.m:28
                temp_candidate[arange(1,crop_size(1)),arange(end() - crop_size(2) + 1,end())]=temp_candidate(arange(1,crop_size(1)),arange(end() - crop_size(2) + 1,end())) + imresize(cropped_depths(arange(),arange(),index_batch),crop_size,'bilinear')
# candidate_generation.m:30
                temp_weight[arange(1,crop_size(1)),arange(end() - crop_size(2) + 1,end())]=temp_weight(arange(1,crop_size(1)),arange(end() - crop_size(2) + 1,end())) + 1
# candidate_generation.m:33
                index_batch=index_batch + 1
# candidate_generation.m:35
                temp_candidate[arange(end() - crop_size(1) + 1,end()),arange(1,crop_size(2))]=temp_candidate(arange(end() - crop_size(1) + 1,end()),arange(1,crop_size(2))) + imresize(cropped_depths(arange(),arange(),index_batch),crop_size,'bilinear')
# candidate_generation.m:37
                temp_weight[arange(end() - crop_size(1) + 1,end()),arange(1,crop_size(2))]=temp_weight(arange(end() - crop_size(1) + 1,end()),arange(1,crop_size(2))) + 1
# candidate_generation.m:40
                index_batch=index_batch + 1
# candidate_generation.m:42
                temp_candidate[arange(end() - crop_size(1) + 1,end()),arange(end() - crop_size(2) + 1,end())]=temp_candidate(arange(end() - crop_size(1) + 1,end()),arange(end() - crop_size(2) + 1,end())) + imresize(cropped_depths(arange(),arange(),index_batch),crop_size,'bilinear')
# candidate_generation.m:44
                temp_weight[arange(end() - crop_size(1) + 1,end()),arange(end() - crop_size(2) + 1,end())]=temp_weight(arange(end() - crop_size(1) + 1,end()),arange(end() - crop_size(2) + 1,end())) + 1
# candidate_generation.m:47
                temp_candidate=temp_candidate / temp_weight / crop_ratio
# candidate_generation.m:49
        if mod(index_candidate,2) == 1:
            candidates[arange(),arange(),index_candidate]=temp_candidate
# candidate_generation.m:53
        else:
            if mod(index_candidate,1) == 0:
                candidates[arange(),arange(),index_candidate]=fliplr(temp_candidate)
# candidate_generation.m:55
    
    candidates=imresize(candidates,concat([72,96]),'bilinear')
# candidate_generation.m:60
    return candidates
    
if __name__ == '__main__':
    pass
    