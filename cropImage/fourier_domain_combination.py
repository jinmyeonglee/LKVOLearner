# Generated with SMOP  0.41
from libsmop import *
from location_signal_maker import *
# fourier_domain_combination.m

    
@function
def fourier_domain_combination(candidates=None,train_weight_term=None,train_bias_term=None,*args,**kwargs):
    # varargin = fourier_domain_combination.varargin
    # nargin = fourier_domain_combination.nargin

    location_signal=location_signal_maker(1605)

    use_signal_num=1605
    #
    index_candidate=concat([zeros(1,7),arange(17,1,- 2),zeros(1,7),arange(18,1,- 2)])
    fft_map=zeros(size(candidates,1),size(candidates,2),32)
    map_center=concat([round(size(candidates,1) / 2 + 1),round(size(candidates,2) / 2 + 1)])

    for index_scale in concat([arange(8,16),arange(24,32)]).reshape(-1):
        fft_map[arange(),arange(),index_scale]=fftshift(fft2(candidates(arange(),arange(),index_candidate(index_scale))))

    ## weight map
    
    weight_map_real=ones(size(fft_map)) / 2
    weight_map_imag=ones(size(fft_map)) / 2
    weight_map_real[arange(),arange(),concat([arange(1,15),arange(17,31)])]=0
    weight_map_imag[arange(),arange(),concat([arange(1,15),arange(17,31)])]=0
    for index_signal in arange(1,use_signal_num).reshape(-1):
        for index_scale in concat([arange(8,16),arange(24,32)]).reshape(-1):
            weight_map_real[map_center(1) + location_signal(index_signal,1),map_center(2) + location_signal(index_signal,2),index_scale]=train_weight_term(index_signal,1,index_scale)
            weight_map_real[map_center(1) - location_signal(index_signal,1),map_center(2) - location_signal(index_signal,2),index_scale]=train_weight_term(index_signal,1,index_scale)
            weight_map_imag[map_center(1) + location_signal(index_signal,1),map_center(2) + location_signal(index_signal,2),index_scale]=train_weight_term(index_signal,2,index_scale)
            weight_map_imag[map_center(1) - location_signal(index_signal,1),map_center(2) - location_signal(index_signal,2),index_scale]=train_weight_term(index_signal,2,index_scale)
        ##
        fft_map[map_center(1) + location_signal(index_signal,1),map_center(2) + location_signal(index_signal,2),index_scale]=fft_map(map_center(1) + location_signal(index_signal,1),map_center(2) + location_signal(index_signal,2),index_scale) - train_bias_term(index_signal,index_scale)
        fft_map[map_center(1) - location_signal(index_signal,1),map_center(2) - location_signal(index_signal,2),index_scale]=fft_map(map_center(1) - location_signal(index_signal,1),map_center(2) - location_signal(index_signal,2),index_scale) - train_bias_term(index_signal,index_scale)

    ##
    fft_map_new=sum(multiply(real(fft_map),weight_map_real) + multiply(dot(1j,imag(fft_map)),weight_map_imag),3)
    depth=real(ifft2(fftshift(fft_map_new)))
    return depth
