'''
This runs random search to find the optimized hyper-parameters using cross-validation

INPUTS:
    - OUT_ITERATION: # of training/testing splits
    - RS_ITERATION: # of random search iteration
    - data_mode: mode to select the time-to-event data from "import_data.py"
    - seed: random seed for training/testing/validation splits
    - EVAL_TIMES: list of time-horizons at which the performance is maximized; 
                  the validation is performed at given EVAL_TIMES (e.g., [12, 24, 36])

OUTPUTS:
    - "hyperparameters_log.txt" is the output
    - Once the hyper parameters are optimized, run "summarize_results.py" to get the final results.
'''
import sys
import time, os
import get_main
import numpy as np
import import_data as impt


# this saves the current hyperparameters
def save_logging(dictionary, log_name):
    with open(log_name, 'w') as f:
        for key, value in dictionary.items():
            f.write('%s:%s\n' % (key, value))

# this open can calls the saved hyperparameters
def load_logging(filename):
    data = dict()
    with open(filename) as f:
        def is_float(input):
            try:
                num = float(input)
            except ValueError:
                return False
            return True

        for line in f.readlines():
            if ':' in line:
                key,value = line.strip().split(':', 1)
                if value.isdigit():
                    data[key] = int(value)
                elif is_float(value):
                    data[key] = float(value)
                elif value == 'None':
                    data[key] = None
                else:
                    data[key] = value
            else:
                pass # deal with bad lines of text here    
    return data

# this randomly select hyperparamters based on the given list of candidates
def get_random_hyperparameters(out_path, useRandomized=False):
    SET_BATCH_SIZE    = [32, 64, 128] #mb_size
 
    SET_LAYERS        = [1,2,3,5] #number of layers
    SET_NODES         = [50, 100, 200, 300] #number of nodes

    SET_ACTIVATION_FN = ['relu', 'elu', 'tanh'] #non-linear activation functions

    SET_ALPHA         = [0.1, 0.5, 1.0, 3.0, 5.0] #alpha values -> log-likelihood loss 
    SET_BETA          = [0.1, 0.5, 1.0, 3.0, 5.0] #beta values -> ranking loss
    SET_GAMMA         = [0.1, 0.5, 1.0, 3.0, 5.0] #gamma values -> calibration loss
    if(useRandomized):
        new_parser = {'mb_size': SET_BATCH_SIZE[np.random.randint(len(SET_BATCH_SIZE))],
    
                     'iteration': 50000,
    
                     'keep_prob': 0.6,
                     'lr_train': 1e-4,
    
                     'h_dim_shared': SET_NODES[np.random.randint(len(SET_NODES))],
                     'h_dim_CS': SET_NODES[np.random.randint(len(SET_NODES))],
                     'num_layers_shared':SET_LAYERS[np.random.randint(len(SET_LAYERS))],
                     'num_layers_CS':SET_LAYERS[np.random.randint(len(SET_LAYERS))],
                     'active_fn': SET_ACTIVATION_FN[np.random.randint(len(SET_ACTIVATION_FN))],
    
                     'alpha':1.0, #default (set alpha = 1.0 and change beta and gamma)
                     'beta':SET_BETA[np.random.randint(len(SET_BETA))],
                     'gamma':0,   #default (no calibration loss)
                     # 'alpha':SET_ALPHA[np.random.randint(len(SET_ALPHA))],
                     # 'beta':SET_BETA[np.random.randint(len(SET_BETA))],
                     # 'gamma':SET_GAMMA[np.random.randint(len(SET_GAMMA))],
    
                     'out_path':out_path}
    else:
        new_parser = {'mb_size': SET_BATCH_SIZE[1],
                     'iteration': 50000,
                     'keep_prob': 0.6,
                     'lr_train': 1e-4,
                     'h_dim_shared': SET_NODES[3],
                     'h_dim_CS': SET_NODES[3],
                     'num_layers_shared':SET_LAYERS[1],
                     'num_layers_CS':SET_LAYERS[1],
                     'active_fn': SET_ACTIVATION_FN[0],
                     'alpha':1.0, #default (set alpha = 1.0 and change beta and gamma)
                     'beta':SET_BETA[0],
                     'gamma':0,   #default (no calibration loss)
                     # 'alpha':SET_ALPHA[np.random.randint(len(SET_ALPHA))],
                     # 'beta':SET_BETA[np.random.randint(len(SET_BETA))],
                     # 'gamma':SET_GAMMA[np.random.randint(len(SET_GAMMA))],
                     'out_path':out_path}
    return new_parser #outputs the dictionary of the randomly-chosen hyperparamters



##### MAIN SETTING
OUT_ITERATION               = 1 # default = 5
RS_ITERATION                = 1 # default = 50

data_mode                   = sys.argv[-1] # MY-SYNTHETHIC
seed                        = 1234

tfseed                      = None # seed for network initialization
##### IMPORT DATASET
'''
    num_Category            = typically, max event/censoring time * 1.2 (to make enough time horizon)
    num_Event               = number of evetns i.e. len(np.unique(label))-1
    max_length              = maximum number of measurements
    x_dim                   = data dimension including delta (num_features)
    mask1, mask2            = used for cause-specific network (FCNet structure)

    EVAL_TIMES              = set specific evaluation time horizons at which the validatoin performance is maximized. 
    						  (This must be selected based on the dataset)

'''
if data_mode == 'SYNTHETIC':
   (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_SYNTHETIC(norm_mode = 'standard')
   EVAL_TIMES = [12, 24, 36]
elif data_mode == 'MY-SYNTHETHIC':
   (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC(norm_mode = 'standard')
   EVAL_TIMES = [7, 14, 20]
elif data_mode == 'MY-SYNTHETIC-E1':
   (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC_E1(norm_mode = 'standard')
   EVAL_TIMES = [7, 14, 20]
elif data_mode == 'METABRIC':
   (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_METABRIC(norm_mode = 'standard')
   EVAL_TIMES = [144, 288, 432] 
else:
    if(data_mode[:4]=='SEER' and len(data_mode)>12 and data_mode[5:10]=='nopro'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_SEER_ALL_UNCENSORED(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [2,6,12]
    elif(data_mode[:4]=='SEER' and len(data_mode)>12 and data_mode[5:10]=='noPre'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_SEER_ALL_NOPRE_ONE_EVENT(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [2,6,12]
    elif(data_mode[:4]=='SEER'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_SEER_ALL_DRAWN(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [2,6,12]
    elif(data_mode[:3]=='ICU' and len(data_mode)>12 and data_mode[4:9]=='nopro'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_ICU_ALL_UNCENSORED(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [7, 17, 28, 38, 56, 60]
    elif(data_mode[:3]=='ICU' and len(data_mode)>12 and data_mode[4:9]=='noPre'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_ICU_ALL_NOPRE_ONE_EVENT(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [7, 17, 28, 38, 56, 60]
    elif(data_mode[:3]=='ICU'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_ICU_ALL_DRAWN(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [7, 17, 28, 38, 56, 60]
    elif(data_mode[:8]=='crash2bo' and len(data_mode)>12 and data_mode[9:14]=='nopro'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2bo_ALL_UNCENSORED(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:8]=='crash2bo' and len(data_mode)>12 and data_mode[9:14]=='noPre'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2bo_ALL_NOPRE_ONE_EVENT(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:8]=='crash2bo'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2bo_ALL_DRAWN(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:8]=='crash2da' and len(data_mode)>12 and data_mode[9:14]=='nopro'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2da_ALL_UNCENSORED(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:8]=='crash2da' and len(data_mode)>12 and data_mode[9:14]=='noPre'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2da_ALL_NOPRE_ONE_EVENT(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:8]=='crash2da'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2da_ALL_DRAWN(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:6]=='crash2' and len(data_mode)>12 and data_mode[7:12]=='nopro'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2_ALL_UNCENSORED(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:6]=='crash2' and len(data_mode)>12 and data_mode[7:12]=='noPre'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2_ALL_NOPRE_ONE_EVENT(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:6]=='crash2'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_CRASH2_ALL_DRAWN(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [9, 18, 28]
    elif(data_mode[:6]=='uncens'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC_ALL_UNCENSORED(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [7, 14, 20]
    elif(data_mode[:6]=='noPrep'):
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC_ALL_NOPRE_ONE_EVENT(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [7, 14, 20]
    else:
        (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC_ALL_DRAWN(dataset=data_mode, norm_mode = 'standard')
        EVAL_TIMES = [7, 14, 20]

DATA = (data, time, label)
MASK = (mask1, mask2) #masks are required to calculate loss functions without for-loops.

out_path      = data_mode + '/results/'

for itr in range(OUT_ITERATION):
    
    if not os.path.exists(out_path + '/itr_' + str(itr) + '/'):
        os.makedirs(out_path + '/itr_' + str(itr) + '/')

    max_valid = 0.
    log_name = out_path + '/itr_' + str(itr) + '/hyperparameters_log.txt'

    for r_itr in range(RS_ITERATION):
        print('OUTER_ITERATION: ' + str(itr))
        print('Random search... itr: ' + str(r_itr))
        new_parser = get_random_hyperparameters(out_path)
        print(new_parser)

        # get validation performance given the hyperparameters
        tmp_max,avgTime,maxit = get_main.get_valid_performance(data_mode,DATA, MASK, new_parser, itr, EVAL_TIMES, MAX_VALUE=max_valid,networkseed=tfseed)

        if tmp_max > max_valid:
            max_valid = tmp_max
            max_parser = new_parser
            save_logging(max_parser, log_name)  #save the hyperparameters if this provides the maximum validation performance
        with open(data_mode+'-time-iteration.txt','w') as lgf:
            lines=[str(maxit)+'\n',str(avgTime)]
            lgf.writelines(lines)
            
        print('Current best: ' + str(max_valid))