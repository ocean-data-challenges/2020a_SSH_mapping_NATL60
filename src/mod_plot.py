import xarray as xr
import numpy
import logging
import matplotlib.pylab as plt
from matplotlib.ticker import ScalarFormatter


def plot_psd_score_v0(ds_psd):
        
    try:
        nb_experiment = len(ds_psd.experiment)
    except:
        nb_experiment = 1
    
    fig, ax0 =  plt.subplots(1, nb_experiment, sharey=True, figsize=(20, 5))
    #plt.subplots_adjust(right=0.1, left=0.09)
    for exp in range(nb_experiment):
        try:
            ctitle = ds_psd.experiment.values[exp]
        except:
            ctitle = ''

        if nb_experiment > 1:
            ax = ax0[exp]
            data = (ds_psd.isel(experiment=exp).values)
        else:
            ax = ax0
            data = (ds_psd.values)
        ax.invert_yaxis()
        ax.invert_xaxis()
        c1 = ax.contourf(1./(ds_psd.freq_lon), 1./ds_psd.freq_time, data,
                          levels=numpy.arange(0,1.1, 0.1), cmap='RdYlGn', extend='both')
        ax.set_xlabel('spatial wavelength (degree_lon)', fontweight='bold', fontsize=18)
        ax0[0].set_ylabel('temporal wavelength (days)', fontweight='bold', fontsize=18)
        #plt.xscale('log')
        ax.set_yscale('log')
        ax.grid(linestyle='--', lw=1, color='w')
        ax.tick_params(axis='both', labelsize=18)
        ax.set_title(f'PSD-based score ({ctitle})', fontweight='bold', fontsize=18)
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
        c2 = ax.contour(1./(ds_psd.freq_lon), 1./ds_psd.freq_time, data, levels=[0.5], linewidths=2, colors='k')
        
        cbar = fig.colorbar(c1, ax=ax, pad=0.01)
        cbar.add_lines(c2)

    bbox_props = dict(boxstyle="round,pad=0.5", fc="w", ec="k", lw=2)
    ax0[-1].annotate('Resolved scales',
                    xy=(1.2, 0.8),
                    xycoords='axes fraction',
                    xytext=(1.2, 0.55),
                    bbox=bbox_props,
                    arrowprops=
                        dict(facecolor='black', shrink=0.05),
                        horizontalalignment='left',
                        verticalalignment='center')

    ax0[-1].annotate('UN-resolved scales',
                    xy=(1.2, 0.2),
                    xycoords='axes fraction',
                    xytext=(1.2, 0.45),
                    bbox=bbox_props,
                    arrowprops=
                    dict(facecolor='black', shrink=0.05),
                        horizontalalignment='left',
                        verticalalignment='center')
    
    plt.show()


def plot_demo_obs(list_of_dataset, dc_ref, central_date, delta_t):

    tmin = central_date - delta_t
    tmax = central_date + delta_t

    list_of_dataset_sel = []
    for ds in list_of_dataset:
        ds_sel = ds.sel(time=slice(tmin, tmax))
        list_of_dataset_sel.append(ds_sel)

    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    for ds in list_of_dataset_sel:
        plt.scatter(ds.lon % 360., ds.lat, c=ds.ssh_model, s=20, cmap='gist_stern')
    plt.xlabel('longitude', fontweight='bold')
    plt.ylabel('latitude', fontweight='bold')
    plt.title(f'SSH model @ altimeter track')
    plt.colorbar(orientation='horizontal')
    plt.subplot(122)
    plt.pcolormesh(dc_ref.lon % 360, dc_ref.lat, dc_ref.sossheig.sel(time=str(central_date)).mean(dim='time'),
                   cmap='gist_stern')
    plt.xlabel('longitude', fontweight='bold')
    plt.ylabel('latitude', fontweight='bold')
    plt.title(f'SSH model')
    plt.colorbar(orientation='horizontal')
    plt.show()


def reformat_dc_ref(dc_ref):
    ds_out = xr.Dataset({'ssh_model': (('lat', 'lon'), dc_ref.sossheig.values)},
                        coords={'lon': dc_ref.lon.values % 360,
                                'lat': dc_ref.lat.values,
                                })
    ds_out.lon.attrs["long_name"] = 'Longitude'
    ds_out.lat.attrs["long_name"] = 'Latitude'

    return ds_out


def hvplot_demo_obs_nadir(list_of_dataset, dc_ref, central_date, delta_t):

    ds_concat_nadirs = xr.concat(list_of_dataset, dim='time')
    ds_concat_nadirs = ds_concat_nadirs.sortby(ds_concat_nadirs.time)
    ds_concat_nadirs = ds_concat_nadirs.assign_coords({'lon': ds_concat_nadirs.lon, 'lat': ds_concat_nadirs.lat})

    ds_concat_nadirs_selection = ds_concat_nadirs.sel(time=slice(central_date - delta_t, central_date + delta_t)).drop(
        'time')

    dc_ref_reformated = reformat_dc_ref(dc_ref.sel(time=central_date, method='nearest'))

    plot = ds_concat_nadirs_selection.hvplot.scatter(x='lon', y='lat', color='ssh_model',
                                                     height=300, width=400, cmap = 'gist_stern', datashade=True) \
           + dc_ref_reformated.hvplot.quadmesh(x='lon', y='lat', color='ssh_model',
                                               height=300, width=400, cmap = 'gist_stern', datashade=True)

    return plot


def hvplot_demo_obs_karin(list_of_dataset, dc_ref, central_date, delta_t):

    ds_swot_karin_sel = list_of_dataset.sel(time=slice(central_date - delta_t, central_date + delta_t))
    ds_swot_karin_sel = ds_swot_karin_sel.assign_coords(
        {'lon': ds_swot_karin_sel.lon, 'lat': ds_swot_karin_sel.lat}).drop('nC')

    dc_ref_reformated = reformat_dc_ref(dc_ref.sel(time=central_date, method='nearest'))

    plot = ds_swot_karin_sel.hvplot.scatter(x='lon', y='lat', color='ssh_model',
                                            height=300, width=400, cmap = 'gist_stern', datashade=True) +\
           dc_ref_reformated.hvplot.quadmesh(x='lon', y='lat', color='ssh_model',
                                             height=300, width=400, cmap = 'gist_stern', datashade=True)

    return plot


def plot_psd_score(ds):
    
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    #ax.invert_yaxis()
    #ax.invert_xaxis()
    c1 = plt.contourf(1./(ds['freq_lon']), 1./ds['freq_time'], ds['psd_score'],
                      levels=numpy.arange(0,1.1, 0.1), cmap='RdYlGn', extend='both')
    cbar = plt.colorbar(pad=0.01)
    plt.xlabel('spatial wavelenght (degree_lon)', fontweight='bold', fontsize=20)
    plt.ylabel('temporal wavelenght (days)', fontweight='bold', fontsize=20)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.grid(linestyle='--', lw=1, color='w')
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title('PSD-based score', fontweight='bold', fontsize=20)
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_formatter(ScalarFormatter())
    c2 = plt.contour(1./(ds['freq_lon']), 1./ds['freq_time'], ds['psd_score'], levels=[0.5], linewidths=2, colors='k')
    cbar.add_lines(c2)

    bbox_props = dict(boxstyle="round,pad=0.5", fc="w", ec="k", lw=2)
    ax.annotate('Resolved scales',
            xy=(1.15, 0.8),
            xycoords='axes fraction',
            xytext=(1.15, 0.55),
            bbox=bbox_props,
            arrowprops=
                dict(facecolor='black', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='center')

    ax.annotate('UN-resolved scales',
            xy=(1.15, 0.2),
            xycoords='axes fraction',
            xytext=(1.15, 0.45),
            bbox=bbox_props,
            arrowprops=
                dict(facecolor='black', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='center')
    
    plt.show()
