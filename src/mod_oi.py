import xarray as xr
import numpy
import logging


def oi_grid(glon, glat, gtime, simu_start_date):
    """
    
    """
    
    logging.info('     Set OI grid...')

    nx = len(glon)
    ny = len(glat)
    nt = len(gtime)

    # define & initialize ssh array
    gssh = numpy.empty((nt, ny, nx))
    nobs = numpy.empty(nt)

    # Make 2D grid
    glon2, glat2 = numpy.meshgrid(glon, glat)
    fglon = glon2.flatten()
    fglat = glat2.flatten()

    ng = len(fglat) # number of grid points
    vtime = (gtime - numpy.datetime64(simu_start_date)) / numpy.timedelta64(1, 'D')
    
    
    ds_oi_grid = xr.Dataset({'gssh' : (('time', 'lat', 'lon'), gssh), 
                             'glon2' : (('lat', 'lon'), glon2),
                             'glat2' : (('lat', 'lon'), glat2),
                             'fglon' : (('ng'), fglon),
                             'fglat' : (('ng'), fglat),
                             'nobs' : (('time'), nobs)},
                              coords={'gtime': (vtime).astype(numpy.float),
                                      'time': gtime,
                                      'lat': glat, 
                                      'lon': glon,
                                      'ng': numpy.arange(ng)})

    return ds_oi_grid
    

def oi_param(Lx, Ly, Lt, noise):
    
    logging.info('     Set OI params...')
    
    ds_oi_param = xr.Dataset({'Lx' : Lx,
                              'Ly' : Ly,
                              'Lt' : Lt,
                              'noise' : noise})
    
    return ds_oi_param
    

def oi_core(it, ds_oi_grid, ds_oi_param, ds_obs):
    
    ind1 = numpy.where((numpy.abs(ds_obs.time.values - ds_oi_grid.gtime.values[it]) < 2.*ds_oi_param.Lt.values))[0]
    nobs = len(ind1)
    print('Processing time-step : ', it, '/', len(ds_oi_grid.gtime.values) - 1, '      nobs = ', nobs, end="\r")
    
    BHt = numpy.empty((len(ds_oi_grid.ng), nobs))
    HBHt = numpy.empty((nobs, nobs))
    
    obs_lon = ds_obs.lon.values[ind1]
    obs_lat = ds_obs.lat.values[ind1]
    obs_time = ds_obs.time.values[ind1]
    
    fglon = ds_oi_grid.fglon.values
    fglat = ds_oi_grid.fglat.values
    ftime = ds_oi_grid.gtime.values[it]
    
    for iobs in range(nobs):
        # print(iobs)
        
        BHt[:,iobs] = numpy.exp(-((ftime - obs_time[iobs])/ds_oi_param.Lt.values)**2 - 
                                ((fglon - obs_lon[iobs])/ds_oi_param.Lx.values)**2 - 
                                ((fglat - obs_lat[iobs])/ds_oi_param.Ly.values)**2)
        
        HBHt[:,iobs] = numpy.exp(-((obs_time - obs_time[iobs])/ds_oi_param.Lt.values)**2 -
                                 ((obs_lon - obs_lon[iobs])/ds_oi_param.Lx.values)**2 -
                                 ((obs_lat - obs_lat[iobs])/ds_oi_param.Ly.values)**2)
    
    del obs_lon, obs_lat, obs_time

    R = numpy.diag(numpy.full((nobs), ds_oi_param.noise.values**2))

    Coo = HBHt + R
    Mi = numpy.linalg.inv(Coo)

    sol = numpy.dot(numpy.dot(BHt, Mi), ds_obs.ssh_model.values[ind1])

    ds_oi_grid.gssh[it, :, :] = sol.reshape(ds_oi_grid.lat.size, ds_oi_grid.lon.size)
    ds_oi_grid.nobs[it] = nobs
    
    
    #return None #  sol.reshape(ds_oi_grid.glat.size, ds_oi_grid.glon.size), nobs

