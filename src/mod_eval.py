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

    # Temporal stability of the error
    reconstruction_error_stability_metric = rmse_t.std().values

    # Show leaderboard SSH-RMSE metric (spatially and time averaged normalized RMSE)
    leaderboard_rmse = 1.0 - (((ds_oi['sossheig'] - ds_ref['sossheig']) ** 2).mean()) ** 0.5 / (
        ((ds_ref['sossheig']) ** 2).mean()) ** 0.5

    logging.info('          => Leaderboard SSH RMSE score = %s', numpy.round(leaderboard_rmse.values, 2))
    logging.info('          Error variability = %s (temporal stability of the mapping error)', numpy.round(reconstruction_error_stability_metric, 2))
    
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
        psd_based_score = (1.0 - mean_psd_err/mean_psd_signal)

        # Find the key metrics: shortest temporal & spatial scales resolved
        # Ideally, we must extract the 0.5 iso-contour and find the minimum scale fron it
        # Here we look at the min value where psd_based_score >= 0.5
        # Pour etre + precis, il faudrait faire un coder plus "chiader" pour interpoler les échelles sur l'iso-contour
        # (cf. ce qui est fait dans SCUBA pour la valid avec along-track indenpedent...)

        index_minimum_lon_scale_resolved = numpy.max(
            numpy.ma.notmasked_edges(
                numpy.ma.masked_invalid(psd_based_score.where(psd_based_score >= 0.5).values), axis=0)[1][1])

        index_minimum_time_scale_resolved = numpy.max(
            numpy.ma.notmasked_edges(
                numpy.ma.masked_invalid(psd_based_score.where(psd_based_score >= 0.5).values), axis=1)[1][0])

        shortest_spatial_wavelength_resolved = 1./psd_based_score.freq_lon.values[index_minimum_lon_scale_resolved]
        shortest_temporal_wavelength_resolved = 1. / psd_based_score.freq_time.values[index_minimum_time_scale_resolved]

        logging.info('          => Leaderboard Spectral score = %s (degree lon)',
                     numpy.round(shortest_spatial_wavelength_resolved, 2))
        logging.info('          => shortest temporal wavelength resolved = %s (days)',
                     numpy.round(shortest_temporal_wavelength_resolved, 2))

        return (1.0 - mean_psd_err/mean_psd_signal)