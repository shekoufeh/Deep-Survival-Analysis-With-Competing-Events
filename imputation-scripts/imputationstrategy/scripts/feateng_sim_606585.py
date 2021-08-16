# Script that performs feature engineering multiple times.
from feateng_subdist_sim1 import build_ysxt_data, feat_stat, build_feat_index
seed1 = "606585"

data_dir = "C:/Users/behning/Projekte/ImputationStrategy/imputationstrategy/createddata/simulation/raw/"+seed1+"/"
for p in ["0.2", "0.4", "0.8"]:
    for seed2 in ["1", "12", "123", "1234", "4123", "5123", "6123", "7123", "8123", "9123"]:
        raw_train = data_dir + "data_raw_train_" + p + "_1_" + seed1 + "_"+ seed2 + ".csv"
        raw_test = data_dir + "data_raw_test_" + p + "_1_" + seed1 + "_"+ seed2 + ".csv"
        raw_val = data_dir + "data_raw_val_" + p + "_1_" + seed1 +"_"+ seed2 + ".csv"
        ysxt_train = data_dir + "feateng/" + "train_" + p + "_1_" + seed1 + "_"+ seed2 + ".txt"
        ysxt_test = data_dir + "feateng/" + "test_" + p + "_1_" + seed1 + "_"+ seed2 + ".txt"
        ysxt_val = data_dir + "feateng/" + "validation_" + p + "_1_" + seed1 + "_"+ seed2 + ".txt"
        featindex = data_dir + "feateng/featindex.txt"
        # calculate statistical results on dataset
        feat_stat(raw_train, raw_test, raw_val)
        build_feat_index(featindex)
        # build_yzbx_data(args.raw_train, args.raw_test, args.yzbx_train, args.yzbx_test)
        build_ysxt_data(raw_train, raw_test, raw_val, ysxt_train,
                        ysxt_test, ysxt_val)

for p in ["0.2", "0.4", "0.8"]:
    for seed2 in ["1", "12", "123", "1234", "4123", "5123", "6123", "7123", "8123", "9123"]:
        raw_train = data_dir + "data_raw_uncensored_train_" + p + "_1_" + seed1 + "_"+ seed2 + ".csv"
        raw_test = data_dir + "data_raw_uncensored_test_" + p + "_1_" + seed1 + "_"+ seed2 + ".csv"
        raw_val = data_dir + "data_raw_uncensored_val_" + p + "_1_" + seed1 +"_"+ seed2 + ".csv"
        ysxt_train = data_dir + "feateng/" + "uncensored_train_" + p + "_1_" + seed1 + "_"+ seed2 + ".txt"
        ysxt_test = data_dir + "feateng/" + "uncensored_test_" + p + "_1_" + seed1 + "_"+ seed2 + ".txt"
        ysxt_val = data_dir + "feateng/" + "uncensored_validation_" + p + "_1_" + seed1 + "_"+ seed2 + ".txt"
        featindex = data_dir + "feateng/uncensored_featindex.txt"
        # calculate statistical results on dataset
        feat_stat(raw_train, raw_test, raw_val)
        build_feat_index(featindex)
        # build_yzbx_data(args.raw_train, args.raw_test, args.yzbx_train, args.yzbx_test)
        build_ysxt_data(raw_train, raw_test, raw_val, ysxt_train,
                        ysxt_test, ysxt_val)
