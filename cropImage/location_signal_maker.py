# Generated with SMOP  0.41
from libsmop import *
# location_signal_maker.m

    
@function
def location_signal_maker(signal_number=None,*args,**kwargs):
    varargin = location_signal_maker.varargin
    nargin = location_signal_maker.nargin

    location_signal=zeros(signal_number,2)
# location_signal_maker.m:3
    mesh_size=ceil(sqrt(dot(2,signal_number)))
# location_signal_maker.m:4
    mesh_x,mesh_y=meshgrid(arange(- mesh_size + 1,mesh_size - 1),arange(0,mesh_size - 1),nargout=2)
# location_signal_maker.m:6
    mesh_x=ravel(mesh_x)
# location_signal_maker.m:8
    mesh_y=ravel(mesh_y)
# location_signal_maker.m:9
    mesh_dist_value=(mesh_x ** 2 + mesh_y ** 2) + mesh_y / mesh_size + mesh_x / (mesh_size ** 2)
# location_signal_maker.m:10
    
    mesh_dist_value=mesh_dist_value + dot(signal_number,double(logical_and((mesh_y == 0),(mesh_x < 0))))
# location_signal_maker.m:12
    mesh_dist_sort=sort(mesh_dist_value)
# location_signal_maker.m:13
    for index in arange(1,signal_number).reshape(-1):
        index_location=find(mesh_dist_value == mesh_dist_sort(index))
# location_signal_maker.m:17
        location_signal[index,1]=mesh_y(index_location)
# location_signal_maker.m:19
        location_signal[index,2]=mesh_x(index_location)
# location_signal_maker.m:20
    