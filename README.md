# Competing-Event-Deep-Survival-Analysis

This repository contains scripts for analysing survival data with competing events using Deep Neural Networks. A preprocessing on the datasets is performed prior to feeding it to the Deep neural network. The data preprocessing is based on an imputation strategy that incorporates the subdistribution weights derived from a classical model. The Deep neural network an adaptation of the DeepHit [1].

The scripts for imputation strategy can be found in ```./imputation-scripts```.

Requirements for imputation strategy
---------------
* pyhton 3.7
* R version 4.0.3
* requires packages tidyverse 1.3.1 and discsurv 1.4.1

* Further package versions can be found in: environment feateng_env.yml

Requirements for Deep survival analysis
---------------
* python 3.6
* To run on GPU: python 2.7, tensorflow 1.12.0

* Further package specifications can be found in: deephit-environment.yml

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

Survival Analysis with Competing Events Using DeepHit
---------------
After preprocessing the dataset use 
```
python convert-preprocessed-into-deephit-format.py 
```
to prepare the data to be processed with the deep neural network. For instance for training the network with ```SEER_1``` dataset use:
```
python main_RandomSearch.py SEER_1
```
To test the trained network, use:
```
python summarize_results.py SEER_1
```


Folder naming conventions:

* DeepHit 1, with imputation: ALL-DRAWN, drawn-input
* DeepHit 1, without imputation: ALL-NOPREONEEVENT, nopreoneevent-input
* DeepHit 2: ALL-UNCENSORED, uncens-input


Evaluation
---------------
For evaluations (computing C-index and Brier Score), run the following scripts:
```
python collect-prediction-files.py
python collect-cIndex-brierScore.py 
compute_CIF.R
```

References
---------------
[1] Lee, C., Zame, W. R., Yoon, J., & van der Schaar, M. (2018, April). Deephit: A deep learning approach to survival analysis with competing risks. In Thirty-second AAAI conference on artificial intelligence.
