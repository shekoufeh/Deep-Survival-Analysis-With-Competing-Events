# Imputation Strategy for Data Preprocessing

Requirements for imputation strategy
---------------
* pyhton 3.7,
* R version 4.0.3,
* requires packages tidyverse 1.3.1 and discsurv 1.4.1

* Further package versions can be found in: environment feateng_env.yml

Imputation Strategy for Data Preprocessing
---------------
SEER, CRASH-2 and simulated datasets can be found in ```./imputation-scripts/imputationstrategy/data```. Expects all R scripts to be run from imputationstrategy (workspace not within 'scripts' folder but one folder above).
```21-functions-imputation.R``` contains new creation of weights (old version in outcommented line)

First: run each R script for impuation and preprocessing:
```
script/21-preprocessing-simulation.R 
scripts/21-preprocessing-CRASH2.R 
scripts/21-preprocessing-SEER.R 
```

Next: Run python script to prepare 'feature engeneered' code (as originally expected by DRSA network):
```
scripts/feateng_sim_606585.py # path needs to be adapted
scripts/feateng_CRASH2.py # path needs to be adapted; run once for CRASH2da and once for CRASH2bo
scripts/feateng_SEER.py # path needs to be adapted
```
