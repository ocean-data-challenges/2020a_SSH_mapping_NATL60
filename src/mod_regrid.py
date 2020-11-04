import xarray as xr
import numpy
import pyinterp
import logging 

def oi_regrid(ds_source, ds_target):
    
    logging.info('     Regridding...')
    
    # Define source grid
    x_source_axis = pyinterp.Axis(ds_source["lon"][:], is_circle=False)
    y_source_axis = pyinterp.Axis(ds_source["lat"][:])
    z_source_axis = pyinterp.TemporalAxis(ds_source["time"][:])
    ssh_source = ds_source["gssh"][:].T
    grid_source = pyinterp.Grid3D(x_source_axis, y_source_axis, z_source_axis, ssh_source.data)
    
    # Define target grid
    mx_target, my_target, mz_target = numpy.meshgrid(ds_target['lon'].values,
                                                     ds_target['lat'].values,
                                                     z_source_axis.safe_cast(ds_target['time'].values),
                                                     indexing="ij")
    # Spatio-temporal Interpolation
    ssh_interp = pyinterp.trivariate(grid_source,
                                     mx_target.flatten(),
                                     my_target.flatten(),
                                     mz_target.flatten(),
                                     bounds_error=True).reshape(mx_target.shape).T
    
    # Save to dataset
    ds_ssh_interp = xr.Dataset({'sossheig' : (('time', 'lat', 'lon'), ssh_interp)},
                               coords={'time': ds_target['time'].values,
                                       'lon': ds_target['lon'].values, 
                                       'lat': ds_target['lat'].values, 
                                       })
    
    return ds_ssh_interp
