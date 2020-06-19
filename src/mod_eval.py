import xarray as xr
import numpy
import logging
import xrft
from dask.diagnostics import ProgressBar

def rmse_based_scores(ds_oi, ds_ref):
    
    logging.info('     Compute RMSE-based scores...')
    
    # RMSE(t) based score
    rmse_t = 1.0 - (((ds_oi['sossheig'] - ds_ref['sossheig'])**2).mean(dim=('lon', 'lat')))**0.5/(((ds_ref['sossheig'])**2).mean(dim=('lon', 'lat')))**0.5
    # RMSE(x, y) based score
    # rmse_xy = 1.0 - (((ds_oi['sossheig'] - ds_ref['sossheig'])**2).mean(dim=('time')))**0.5/(((ds_ref['sossheig'])**2).mean(dim=('time')))**0.5
    rmse_xy = (((ds_oi['sossheig'] - ds_ref['sossheig'])**2).mean(dim=('time')))**0.5
    
    rmse_t = rmse_t.rename('rmse_t')
    rmse_xy = rmse_xy.rename('rmse_xy')
    
    return rmse_t, rmse_xy


def psd_based_scores(ds_oi, ds_ref):
    
    logging.info('     Compute PSD-based scores...')
    
    with ProgressBar():
        
        # Compute error = SSH_reconstruction - SSH_true
        err = (ds_oi['sossheig'] - ds_ref['sossheig'])
        err = err.chunk({"lat":1, 'time': err['time'].size, 'lon': err['lon'].size})
        # make time vector in days units 
        err['time'] = (err.time - err.time[0]) / numpy.timedelta64(1, 'D')
        
        # Rechunk SSH_true
        signal = ds_ref['sossheig'].chunk({"lat":1, 'time': ds_ref['time'].size, 'lon': ds_ref['lon'].size})
        # make time vector in days units
        signal['time'] = (signal.time - signal.time[0]) / numpy.timedelta64(1, 'D')
    
        # Compute PSD_err and PSD_signal
        psd_err = xrft.power_spectrum(err, dim=['time', 'lon'], detrend='linear', window=True).compute()
        psd_signal = xrft.power_spectrum(signal, dim=['time', 'lon'], detrend='linear', window=True).compute()
        
        # Averaged over latitude
        mean_psd_signal = psd_signal.mean(dim='lat').where((psd_signal.freq_lon > 0.) & (psd_signal.freq_time > 0), drop=True)
        mean_psd_err = psd_err.mean(dim='lat').where((psd_err.freq_lon > 0.) & (psd_err.freq_time > 0), drop=True)
        
        # return PSD-based score
        return (1.0 - mean_psd_err/mean_psd_signal)