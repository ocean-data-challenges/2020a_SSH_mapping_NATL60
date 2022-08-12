import xarray as xr
import numpy
import pyinterp
import pyinterp.fill
import logging 

def oi_regrid(ds_source, ds_target):
    
    logging.info('     Regridding...')
    
    # Define source grid
    x_source_axis = pyinterp.Axis(ds_source["lon"][:].values, is_circle=False)
    y_source_axis = pyinterp.Axis(ds_source["lat"][:].values)
    z_source_axis = pyinterp.TemporalAxis(ds_source["time"][:].values)
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
                                     bounds_error=False).reshape(mx_target.shape).T
    
    # MB add extrapolation in NaN values if needed
    if numpy.isnan(ssh_interp).any():
        logging.info('     NaN found in ssh_interp, starting extrapolation...')
        x_source_axis = pyinterp.Axis(ds_target['lon'].values, is_circle=False)
        y_source_axis = pyinterp.Axis(ds_target['lat'].values)
        z_source_axis = pyinterp.TemporalAxis(ds_target["time"][:].values)
        grid = pyinterp.Grid3D(x_source_axis, y_source_axis, z_source_axis,  ssh_interp.T)
        has_converged, filled = pyinterp.fill.gauss_seidel(grid)
    else:
        filled = ssh_interp.T
    
    # Save to dataset
    ds_ssh_interp = xr.Dataset({'sossheig' : (('time', 'lat', 'lon'), filled.T)},
                               coords={'time': ds_target['time'].values,
                                       'lon': ds_target['lon'].values, 
                                       'lat': ds_target['lat'].values, 
                                       })
    
    return ds_ssh_interp
