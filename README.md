[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4045400.svg)](https://doi.org/10.5281/zenodo.4045400)

# SSH Mapping Data Challenge 2020a

This repository contains codes and sample notebooks for downloading and processing the SSH mapping data challenge.

The quickstart can be run online by clicking here:
[![Binder](https://binder.pangeo.io/badge_logo.svg)](https://binder.pangeo.io/v2/gh/ocean-data-challenges/2020a_SSH_mapping_NATL60/master?filepath=quickstart.ipynb)

## Motivation

The goal is to investigate how to best reconstruct sequences of Sea Surface Height (SSH) maps from partial satellite altimetry observations. This data challenge follows an _Observation System Simulation Experiment_ framework: "Real" full SSH are from a numerical simulation with a realistic, high-resolution ocean circulation model: the reference simulation. Satellite observations are simulated by sampling the reference simulation based on realistic orbits of past, existing or future altimetry satellites. A baseline reconstruction method is provided (see below) and the practical goal of the challenge is to beat this baseline according to scores also described below and in Jupyter notebooks.

### Reference simulation
The reference simulation is the NATL60 simulation based on the NEMO model (Ajayi et al. 2020 doi:[10.1029/2019JC015827](https://doi.org/10.1029/2019JC015827)). The simulation is run without tidal forcing. 

### Observations
The SSH observations include simulations of Topex-Poseidon, Jason 1, Geosat Follow-On, Envisat, and SWOT altimeter data. This nadir altimeters constellation was operating during the 2003-2005 period and is still considered as a historical optimal constellation in terms of spatio-temporal coverage. The data challenge simulates the addition of SWOT to this reference constellation. No observation error is considered in this challenge.

### Data sequence and use
 
The SSH reconstructions are assessed over the period from 2012-10-22 to 2012-12-02: 42 days, which is equivalent to two SWOT cycles in the SWOT science phase orbit.
For reconstruction methods that need a spin-up, the **observations** can be used from 2012-10-01 until the beginning of the evaluation period (21 days). This spin-up period is not included in the evaluation. For reconstruction methods that need learning from full fields, the **reference data** can be used from 2013-01-02 to 2013-09-30. The reference data between 2012-12-02 and 2013-01-02 should never be used so that any learning period or other method-related-training period can be considered uncorrelated to the evaluation period.

![Data Sequence](figures/DC-data_availability.png)

## Leaderboard

| Method     |   µ(RMSE) |   σ(RMSE) |   λx (degree) |   λt (days) | Notes                     | Reference        |
|:-----------|------------------------:|---------------------:|-------------------------:|-----------------------:|:--------------------------|:-----------------|
| baseline OI 1 nadir |                    0.69 |                 0.03 |                     3.31 |                  33.32 | Covariances not optimized | [quickstart.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/quickstart.ipynb)  |
| baseline OI 4 nadirs |                    0.83 |                 0.04 |                     2.25 |                  15.67 | Covariances not optimized | [quickstart.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/quickstart.ipynb) |
| baseline OI 1 swot |                    0.85 |                 0.05 |                     1.22 |                  12.38 | Covariances not optimized | [quickstart.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/quickstart.ipynb) |
| | | | | | | |
| duacs 4 nadirs |       0.92 |     <span style="color:green"> **0.01** </span> |          1.42 |       12.13 | Covariances DUACS | [eval_duacs.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_duacs.ipynb)  |
| bfn 4 nadirs  |       0.92 |      0.02 |          1.23 |       10.82 | QG Nudging | [eval_bfn.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_bfn.ipynb) |
| dymost 4 nadirs |       0.91 |     <span style="color:green"> **0.01** </span> |          1.36 |       11.91 | Dynamic mapping | [eval_dymost.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_dymost.ipynb) |
| miost 4 nadirs |       0.93 |     <span style="color:green"> **0.01** </span> |          1.35 |       10.41 | Multiscale mapping | [eval_miost.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_miost.ipynb) |
| 4DVarNet 4 nadirs |      <span style="color:green"> **0.94** |     <span style="color:green">**0.01** </span> |          1.19 |       10.64 | 4DVarNet mapping | [eval_4dvarnet.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_4dvarnet.ipynb) |
| 4DVarNet v2022 4 nadirs :trophy: |       <span style="color:green">**0.94** </span> |      <span style="color:green">**0.01** </span> |         <span style="color:green"> **0.83** |      <span style="color:green"> **8.03** | 4DVarNet mapping | [eval_4dvarnet_v2022.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_4dvarnet_v2022.ipynb) |
| | | | | | | |
| duacs 1 swot + 4 nadirs |       0.92 |      0.02 |          1.22 |       11.37 | Covariances DUACS |[eval_duacs.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_duacs.ipynb) |
| bfn 1 swot + 4 nadirs  |       0.93 |      0.02 |           1. |        10.24 | QG Nudging | [eval_bfn.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_bfn.ipynb) |
| dymost 1 swot + 4 nadirs |       0.93 |      0.02 |           1.19 |        10.04 | Dynamic mapping | [eval_dymost.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_dymost.ipynb) |
| miost 1 swot + 4 nadirs |       0.94 |      <span style="color:green">**0.01** </span> |          1.18 |       10.33 | Multiscale mapping | [eval_miost.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_miost.ipynb) |
| 4DVarNet 1 swot + 4 nadirs |       0.95 |      <span style="color:green">**0.01** </span> |          0.7 |        6.48 | 4DVarNet mapping | [eval_4dvarnet.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_4dvarnet.ipynb) |
| 4DVarNet v2022 1 swot + 4 nadirs :trophy: |       <span style="color:green">**0.96** </span> |     <span style="color:green"> **0.01** </span> |          <span style="color:green">**0.62** </span> |        <span style="color:green">**4.35** </span> | 4DVarNet mapping | [eval_4dvarnet_v2022.ipynb](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/eval_4dvarnet_v2022.ipynb) |



**µ(RMSE)**: average RMSE score.  
**σ(RMSE)**: standard deviation of the RMSE score.  
**λx**: minimum spatial scale resolved.  
**λt**: minimum time scale resolved. 
 
## Quick start
You can follow the quickstart guide in [this notebook](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/quickstart.ipynb) or launch it directly from <a href="https://binder.pangeo.io/v2/gh/ocean-data-challenges/2020a_SSH_mapping_NATL60/master?filepath=quickstart.ipynb" target="_blank">binder</a>.

## Download the data
The data are hosted on the [AVISO+ website](https://www.aviso.altimetry.fr/en/data/products/ocean-data-challenges/2020a-ssh-mapping-natl60.html) and tagged with DOI: 10.24400/527896/a01-2020.002. The website also provides a data handbook. This is the recommended access. This [wiki](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/wiki/AVISO---account-creation) can help you create an AVISO account to access the data. The data are also temporarily available [here](https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/catalog/meomopendap/extract/ocean-data-challenges/dc_data1/catalog.html). They are presented with the following directory structure:

```
. 
|-- dc_obs
|   |-- 2020a_SSH_mapping_NATL60_topex-poseidon_interleaved.nc
|   |-- 2020a_SSH_mapping_NATL60_nadir_swot.nc 
|   |-- 2020a_SSH_mapping_NATL60_karin_swot.nc
|   |-- 2020a_SSH_mapping_NATL60_jason1.nc
|   |-- 2020a_SSH_mapping_NATL60_geosat2.nc
|   |-- 2020a_SSH_mapping_NATL60_envisat.nc

|-- dc_ref
|   |-- NATL60-CJM165_GULFSTREAM_y****m**d**.1h_SSH.nc

```

To start out download the *observation* dataset (dc_obs, 285M) from the temporary data server, use: 
```shell
wget https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/ocean-data-challenges/dc_data1/dc_obs.tar.gz
```

and the *reference* dataset (dc_ref, 11G) using (*this step may take several minutes*): 

```shell
wget https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/fileServer/meomopendap/extract/ocean-data-challenges/dc_data1/dc_ref.tar.gz
```
and then uncompress the files using `tar -xvf <file>.tar.gz`. You may also use `ftp`, `rsync` or `curl`to donwload the data.  


## Baseline and evaluation

### Baseline
The baseline mapping method is optimal interpolation (OI), in the spirit of the present-day standard for DUACS products provided by AVISO. OI is implemented in the [`baseline_oi`](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/baseline_oi.ipynb) Jupyter notebook. The SSH reconstructions are saved as a NetCDF file in the `results` directory. The content of this directory is git-ignored.
   
### Evaluation

The evaluation of the mapping methods is based on the comparison of the SSH reconstructions with the *reference* dataset. It includes two scores, one based on the Root-Mean-Square Error (RMSE), the other based on Fourier wavenumber spectra. The evaluation notebook [`example_data_eval`](https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60/blob/master/notebooks/example_data_eval.ipynb) implements the computation of these two scores as they could appear in the leaderboard. The notebook also provides additional, graphical diagnostics based on RMSE and spectra.

## Data processing

Cross-functional modules are gathered in the `src` directory. They include tools for regridding, plots, evaluation, writing and reading NetCDF files. The directory also contains a module that implements the baseline method.  

## Acknowledgement

The structure of this data challenge was to a large extent inspired by [WeatherBench](https://github.com/pangeo-data/WeatherBench).
