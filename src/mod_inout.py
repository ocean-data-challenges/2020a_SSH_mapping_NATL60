import xarray as xr
import numpy
import logging

def read_obs(input_file, oi_grid, oi_param, simu_start_date, coarsening):
    
    logging.info('     Reading observations...')
    
    def preprocess(ds):
        return ds.coarsen(coarsening, boundary="trim").mean()
    
    ds_obs = xr.open_mfdataset(input_file, combine='nested', concat_dim='time', parallel=True, preprocess=preprocess) #.sortby('time')
    #ds_obs = ds_obs.coarsen(coarsening, boundary="trim").mean().sortby('time')
    ds_obs = ds_obs.sortby('time')
    
    lon_min = oi_grid.lon.min().values
    lon_max = oi_grid.lon.max().values
    lat_min = oi_grid.lat.min().values
    lat_max = oi_grid.lat.max().values
    time_min = oi_grid.time.min().values
    time_max = oi_grid.time.max().values
    
    ds_obs = ds_obs.sel(time=slice(time_min - numpy.timedelta64(int(2*oi_param.Lt.values), 'D'), 
                                   time_max + numpy.timedelta64(int(2*oi_param.Lt.values), 'D')), drop=True)
    
    # correct lon if domain is between [-180:180]
    if lon_min < 0:
        ds_obs['lon'] = xr.where(ds_obs['lon'] >= 180., ds_obs['lon']-360., ds_obs['lon'])
        
    ds_obs = ds_obs.where((ds_obs['lon'] >= lon_min - oi_param.Lx.values) & 
                          (ds_obs['lon'] <= lon_max + oi_param.Lx.values) &
                          (ds_obs['lat'] >= lat_min - oi_param.Ly.values) &
                          (ds_obs['lat'] <= lat_max + oi_param.Ly.values) , drop=True)
    
    vtime = (ds_obs['time'].values - numpy.datetime64(simu_start_date)) / numpy.timedelta64(1, 'D')
    ds_obs = ds_obs.assign_coords({'time': vtime})
    
    return ds_obs
