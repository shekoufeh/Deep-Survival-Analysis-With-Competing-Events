_EPSILON = 1e-08

import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import import_data as impt
import utils_network as utils
from class_DeepHit import Model_DeepHit
from sklearn.model_selection import train_test_split
from utils_eval import weighted_c_index, weighted_brier_score

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

##### MAIN SETTING
OUT_ITERATION               = 1 # default = 5

data_mode                   = sys.argv[-1] #METABRIC, SYNTHETIC,MY-SYNTHETHIC
seed                        = 1234
EVAL_TIMES                  = [7, 14, 20] # evalution times (for C-index and Brier-Score)
PRINT_EVALUATIONS           = False

##### IMPORT DATASET
'''
    num_Category            = max event/censoring time * 1.2 (to make enough time horizon)
    num_Event               = number of evetns i.e. len(np.unique(label))-1
    max_length              = maximum number of measurements
    x_dim                   = data dimension including delta (num_features)
    mask1, mask2            = used for cause-specific network (FCNet structure)
'''
if data_mode == 'SYNTHETIC':
    (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_SYNTHETIC(norm_mode = 'standard')
    EVAL_TIMES  = [12, 24, 36]
elif data_mode == 'MY-SYNTHETHIC':
    (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC(norm_mode = 'standard')
    EVAL_TIMES  = [7, 14, 20]
elif data_mode == 'MY-SYNTHETIC-E1':
    (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_MY_SYNTHETIC_E1(norm_mode = 'standard')
    EVAL_TIMES  = [7, 14, 20]
elif data_mode == 'METABRIC':
    (x_dim), (data, time, label), (mask1, mask2) = impt.import_dataset_METABRIC(norm_mode = 'standard')
    EVAL_TIMES  = [144, 288, 432]
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

_, num_Event, num_Category  = np.shape(mask1)  # dim of mask1: [subj, Num_Event, Num_Category]

EVAL_TIMES=list(np.arange(1,29)) if (data_mode[:6]=='crash2') else list(np.arange(1,21))
EVAL_TIMES=list(np.arange(1,61)) if (data_mode[:3]=='ICU') else EVAL_TIMES
EVAL_TIMES=list(np.arange(1,14)) if (data_mode[:4]=='SEER') else EVAL_TIMES

in_path = data_mode + '/results/'

if not os.path.exists(in_path):
    os.makedirs(in_path)

FINAL1 = np.zeros([num_Event, len(EVAL_TIMES), OUT_ITERATION])
FINAL2 = np.zeros([num_Event, len(EVAL_TIMES), OUT_ITERATION])

for out_itr in range(OUT_ITERATION):
    in_hypfile = in_path + '/itr_' + str(out_itr) + '/hyperparameters_log.txt'
    in_parser = load_logging(in_hypfile)

    ##### HYPER-PARAMETERS
    mb_size                     = in_parser['mb_size']

    iteration                   = in_parser['iteration']

    keep_prob                   = in_parser['keep_prob']
    lr_train                    = in_parser['lr_train']

    h_dim_shared                = in_parser['h_dim_shared']
    h_dim_CS                    = in_parser['h_dim_CS']
    num_layers_shared           = in_parser['num_layers_shared']
    num_layers_CS               = in_parser['num_layers_CS']

    if in_parser['active_fn'] == 'relu':
        active_fn                = tf.nn.relu
    elif in_parser['active_fn'] == 'elu':
        active_fn                = tf.nn.elu
    elif in_parser['active_fn'] == 'tanh':
        active_fn                = tf.nn.tanh
    else:
        print('Error!')
    
    initial_W                   = tf.contrib.layers.xavier_initializer()

    alpha                       = in_parser['alpha']  #for log-likelihood loss
    beta                        = in_parser['beta']  #for ranking loss
    gamma                       = in_parser['gamma']  #for RNN-prediction loss
    parameter_name              = 'a' + str('%02.0f' %(10*alpha)) + 'b' + str('%02.0f' %(10*beta)) + 'c' + str('%02.0f' %(10*gamma))

    ##### MAKE DICTIONARIES
    # INPUT DIMENSIONS
    input_dims                  = { 'x_dim'         : x_dim,
                                    'num_Event'     : num_Event,
                                    'num_Category'  : num_Category}

    # NETWORK HYPER-PARMETERS
    network_settings            = { 'h_dim_shared'         : h_dim_shared,
                                    'h_dim_CS'          : h_dim_CS,
                                    'num_layers_shared'    : num_layers_shared,
                                    'num_layers_CS'    : num_layers_CS,
                                    'active_fn'      : active_fn,
                                    'initial_W'         : initial_W }


    # for out_itr in range(OUT_ITERATION):
    print ('ITR: ' + str(out_itr+1) + ' DATA MODE: ' + data_mode + ' (a:' + str(alpha) + ' b:' + str(beta) + ' c:' + str(gamma) + ')' )
    ##### CREATE DEEPFHT NETWORK
    tf.reset_default_graph()
    
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    model = Model_DeepHit(sess, "DeepHit", input_dims, network_settings)
    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())
    
    if (data_mode=="MY-SYNTHETHIC" or data_mode == 'MY-SYNTHETIC-E1') :
        setSizes=[15000,5000,10000] # Train, Validation, Test
        (tr_data,te_data, tr_time,te_time, tr_label,te_label, 
         tr_mask1,te_mask1, tr_mask2,te_mask2)  = utils.my_train_test_split(data, time, label, mask1, mask2, test_size=10000) 
       
    
        (tr_data,va_data, tr_time,va_time, tr_label,va_label, 
         tr_mask1,va_mask1, tr_mask2,va_mask2)  = utils.my_train_test_split(tr_data, tr_time, tr_label, tr_mask1, tr_mask2, test_size=5000) 
   
    elif(data_mode == 'SYNTHETIC' or data_mode == 'METABRIC' ):
        ### TRAINING-TESTING SPLIT
        (tr_data,te_data, tr_time,te_time, tr_label,te_label, 
         tr_mask1,te_mask1, tr_mask2,te_mask2)  = train_test_split(data, time, label, mask1, mask2, test_size=0.20, random_state=seed) 
       
    
        (tr_data,va_data, tr_time,va_time, tr_label,va_label, 
         tr_mask1,va_mask1, tr_mask2,va_mask2)  = train_test_split(tr_data, tr_time, tr_label, tr_mask1, tr_mask2, test_size=0.20, random_state=seed) 
    else:
        if(data_mode[:4]=='SEER'):
            setSizes=[60898,24361,36539]
        elif(data_mode[:3]=='ICU'):
            setSizes=[1125,281,470] # Train, Validation, Test
        elif(data_mode[:8]=='crash2da' or data_mode[:8]=='crash2bo'):
            setSizes=[9729,3256,6851]
        elif(data_mode[:6]=='crash2'):
            setSizes=[9517,3176,6345] # Train, Validation, Test
        else:
            ### TRAINING-TESTING SPLIT
            setSizes=[15000,5000,10000] # Train, Validation, Test
        (tr_data,te_data, tr_time,te_time, tr_label,te_label, 
         tr_mask1,te_mask1, tr_mask2,te_mask2)  = utils.my_train_test_split(data, time, label, mask1, mask2, test_size=setSizes[2]) 
    
        (tr_data,va_data, tr_time,va_time, tr_label,va_label, 
         tr_mask1,va_mask1, tr_mask2,va_mask2)  = utils.my_train_test_split(tr_data, tr_time, tr_label, tr_mask1, tr_mask2, test_size=setSizes[1]) 
 
    ##### PREDICTION & EVALUATION
    saver.restore(sess, in_path + '/itr_' + str(out_itr) + '/models/model_itr_' + str(out_itr))

    ### PREDICTION
    pred = model.predict(te_data)
    
    # Save predictions
    for event in range(pred.shape[1]):
        np.savetxt(in_path+"predictions-event-"+str(event+1)+".txt",pred[:,event,:])
     
    if(PRINT_EVALUATIONS):
        ### EVALUATION
        result1, result2 = np.zeros([num_Event, len(EVAL_TIMES)]), np.zeros([num_Event, len(EVAL_TIMES)])
    
        for t, t_time in enumerate(EVAL_TIMES):
            eval_horizon = int(t_time)
    
            if eval_horizon >= num_Category:
                print( 'ERROR: evaluation horizon is out of range')
                result1[:, t] = result2[:, t] = -1
            else:
                # calculate F(t | x, Y, t >= t_M) = \sum_{t_M <= \tau < t} P(\tau | x, Y, \tau > t_M)
                risk = np.sum(pred[:,:,:(eval_horizon+1)], axis=2) #risk score until EVAL_TIMES
                for k in range(num_Event):
                    # result1[k, t] = c_index(risk[:,k], te_time, (te_label[:,0] == k+1).astype(float), eval_horizon) #-1 for no event (not comparable)
                    # result2[k, t] = brier_score(risk[:,k], te_time, (te_label[:,0] == k+1).astype(float), eval_horizon) #-1 for no event (not comparable)
                    result1[k, t] = weighted_c_index(tr_time, (tr_label[:,0] == k+1).astype(int), risk[:,k], te_time, (te_label[:,0] == k+1).astype(int), eval_horizon) #-1 for no event (not comparable)
                    result2[k, t] = weighted_brier_score(tr_time, (tr_label[:,0] == k+1).astype(int), risk[:,k], te_time, (te_label[:,0] == k+1).astype(int), eval_horizon) #-1 for no event (not comparable)
    
        FINAL1[:, :, out_itr] = result1
        FINAL2[:, :, out_itr] = result2
    
        ### SAVE RESULTS
        row_header = []
        for t in range(num_Event):
            row_header.append('Event_' + str(t+1))
    
        col_header1 = []
        col_header2 = []
        for t in EVAL_TIMES:
            col_header1.append(str(t) + 'yr c_index')
            col_header2.append(str(t) + 'yr B_score')
    
        # c-index result
        df1 = pd.DataFrame(result1, index = row_header, columns=col_header1)
        df1.to_csv(in_path + '/result_CINDEX_itr' + str(out_itr) + '.csv')
    
        # brier-score result
        df2 = pd.DataFrame(result2, index = row_header, columns=col_header2)
        df2.to_csv(in_path + '/result_BRIER_itr' + str(out_itr) + '.csv')
    
        ### PRINT RESULTS
        print('========================================================')
        print('ITR: ' + str(out_itr+1) + ' DATA MODE: ' + data_mode + ' (a:' + str(alpha) + ' b:' + str(beta) + ' c:' + str(gamma) + ')' )
        print('SharedNet Parameters: ' + 'h_dim_shared = '+str(h_dim_shared) + ' num_layers_shared = '+str(num_layers_shared) + 'Non-Linearity: ' + str(active_fn))
        print('CSNet Parameters: ' + 'h_dim_CS = '+str(h_dim_CS) + ' num_layers_CS = '+str(num_layers_CS) + 'Non-Linearity: ' + str(active_fn)) 
    
        print('--------------------------------------------------------')
        print('- C-INDEX: ')
        print(df1)
        print('--------------------------------------------------------')
        print('- BRIER-SCORE: ')
        print(df2)
        print('========================================================')


if(PRINT_EVALUATIONS):  
    ### FINAL MEAN/STD
    # c-index result
    df1_mean = pd.DataFrame(np.mean(FINAL1, axis=2), index = row_header, columns=col_header1)
    df1_std  = pd.DataFrame(np.std(FINAL1, axis=2), index = row_header, columns=col_header1)
    df1_mean.to_csv(in_path + '/result_CINDEX_FINAL_MEAN.csv')
    df1_std.to_csv(in_path + '/result_CINDEX_FINAL_STD.csv')
    
    # brier-score result
    df2_mean = pd.DataFrame(np.mean(FINAL2, axis=2), index = row_header, columns=col_header2)
    df2_std  = pd.DataFrame(np.std(FINAL2, axis=2), index = row_header, columns=col_header2)
    df2_mean.to_csv(in_path + '/result_BRIER_FINAL_MEAN.csv')
    df2_std.to_csv(in_path + '/result_BRIER_FINAL_STD.csv')
    
    
    ### PRINT RESULTS
    print('========================================================')
    print('- FINAL C-INDEX: ')
    print(df1_mean)
    print('--------------------------------------------------------')
    print('- FINAL BRIER-SCORE: ')
    print(df2_mean)
    print('========================================================')
