import argparse
import random

version_of_data = "CRASH2ba"# or CRASH2da or CRASH2bo or CRASH2

# run feateng
data_dir = "C:/Users/behning/Projekte/ImputationStrategy/imputationstrategy/createddata/"+ version_of_data +"/raw/"

if version_of_data == "CRASH2":
    features = ["isex", "iage", "ninjurytime", "iinjurytype", "isbp", "ihr", "irr", "icc", "igcs"]
    feat_size = {"isex": 2 + 1,
                 "iage": 86 + 1,  # age 14-99 featured to 1-86
                 "ninjurytime": 720 + 1,  # from 0.1 to 72 round to 1 digit muliplied by 10
                 "iinjurytype": 3 + 1,  # no featen
                 "isbp": 247 + 1,  # from 4-250 minus 3
                 "ihr": 218 + 1,
                 "irr": 96 + 1,  # can stay
                  "icc": 30 +1, #can stay
                 "igcs": 13 + 1}
elif version_of_data in ("CRASH2bo", "CRASH2da"):
    features = ["isex", "iage", "ninjurytime", "iinjurytype", "isbp", "ihr", "irr", "igcs"]
    # feat_size: field width
    # always is the range of possible distinct features + 1 for NA
    feat_size = {"isex": 2 + 1,
                 "iage": 86 + 1,  # age 14-99 featured to 1-86
                 "ninjurytime": 720 + 1,  # from 0.1 to 72 round to 1 digit muliplied by 10
                 "iinjurytype": 3 + 1,  # no featen
                 "isbp": 247 + 1,  # from 4-250 minus 3
                 "ihr": 218 + 1,
                 "irr": 96 + 1,  # can stay
                 "igcs": 13 + 1}




# feat_dict: featname: set()---distinct feat values
feat_dict = {}

# feat_index
feat_index = {}


# build feat_index
def build_feat_index(feat_index_f):
    max_index = 0
    feat_index_lines = []

    # truncate
    feat_index["0:truncate"] = max_index
    feat_index_lines.append("0:truncate\t{}\n".format(max_index))
    max_index += 1

    for i in range(len(features)):
        feat_num = i + 1
        # other
        feat_index["{}:other".format(feat_num)] = max_index
        feat_index_lines.append("{}:other\t{}\n".format(feat_num, max_index))
        max_index += 1
        # normal values
        width = feat_size[features[i]]
        for value in range(width - 1):
            feat_index["{}:{}".format(feat_num, value)] = max_index
            feat_index_lines.append("{}:{}\t{}\n".format(feat_num, value, max_index))
            max_index += 1

    # write feat_index file:
    with open(feat_index_f, 'w') as f:
        f.writelines(feat_index_lines)

def get_feat_val(feat_name, str_val):
    if feat_name in ("iage"):
        return int(str_val)-14
    elif feat_name in ("ninjurytime"):
        return int(round(float(str_val),1) *10 -1)
    elif feat_name in ("isbp"):
        return int(str_val)-4
    elif feat_name in ("ihr", "igcs"):
        return int(str_val)-3
    else:
        return int(str_val)-1 # isex, iinjurytype


def build_ysxt_data(raw_train, raw_test, raw_val, ysxt_train, ysxt_test, ysxt_val):
    fnames_i = [raw_train, raw_test, raw_val] #
    fnames_o = [ysxt_train, ysxt_test, ysxt_val]

    for j in range(len(fnames_i)):
        ysxt_list = []
        with open(fnames_i[j], 'r') as f:
            lines = f.readlines()
            for line in lines:
                x_items = []
                # truncate dummy append
                x_items.append("0:1")
                line_items = line.split(',')
                for i in range( len(line_items)-2): #(first is row ID), second is status
                    feat_num = i +1#+ 2
                    feat_name = features[i]
                    feat_val = get_feat_val(feat_name, line_items[i+2])
                    key = "{}:{}".format(feat_num, feat_val)
                    if key not in feat_index.keys():
                        key = "{}:other".format(feat_num)
                    x_items.append("{}:1".format(feat_index[key]))

                status = line_items[1].rstrip() # status is in line 2
                time = line_items[0]

                ysxt = ' '.join([str(status)] + x_items + [str(time)])
                ysxt_list.append(ysxt + '\n')

        with open(fnames_o[j], 'w') as f:
            f.writelines(ysxt_list)

# calculate features' statistical: max value, min value, mean value, and different value counts
def feat_stat(train, test, val):
    for feat in features:
        feat_dict[feat] = set()

    # train
    with open(train, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(',')
            for i in range(len(items) - 2):
                feat_name = features[i]
                feat_dict[feat_name].add(float(items[i]))
    # test
    with open(test, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(',')
            for i in range(len(items) - 2):
                feat_name = features[i]
                feat_dict[feat_name].add(float(items[i]))

    # val
    with open(val, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(',')
            for i in range(len(items) - 2):
                feat_name = features[i]
                feat_dict[feat_name].add(float(items[i]))

    # print result
    for feat in features:
        stats = feat_dict[feat]
        print("{} result:".format(feat))
        print("max value:{0}    min value:{1}   distinct cnt:{2}".format(max(stats), min(stats), len(stats)))


def main(args):
    # calculate statistical results on dataset
    feat_stat(args.raw_train, args.raw_test, args.raw_val)
    build_feat_index(args.featindex)
    #build_yzbx_data(args.raw_train, args.raw_test, args.yzbx_train, args.yzbx_test)
    build_ysxt_data(args.raw_train, args.raw_test, args.raw_val, args.ysxt_train,
                    args.ysxt_test, args.ysxt_val)


for seed2 in ["1", "12", "123", "1234", "4123", "5123", "6123", "7123", "8123", "9123"]:
    raw_train = data_dir + "data_raw_train_" + seed2 + ".csv"
    raw_test = data_dir + "data_raw_test_" + seed2 + ".csv"
    raw_val = data_dir + "data_raw_val_" + seed2 + ".csv"
    ysxt_train = data_dir + "feateng/" + "train_" + seed2 + ".txt"
    ysxt_test = data_dir + "feateng/" + "test_" + seed2 + ".txt"
    ysxt_val = data_dir + "feateng/" + "validation_" + seed2 + ".txt"
    featindex = data_dir + "feateng/featindex.txt"
    # calculate statistical results on dataset
    feat_stat(raw_train, raw_test, raw_val)
    build_feat_index(featindex)
    # build_yzbx_data(args.raw_train, args.raw_test, args.yzbx_train, args.yzbx_test)
    build_ysxt_data(raw_train, raw_test, raw_val, ysxt_train,
                    ysxt_test, ysxt_val)

# create also for uncesored data


# last additional
# for seed2 in ["1", "12", "123", "1234", "4123", "5123", "6123", "7123", "8123", "9123"]:
#     raw_train = data_dir + "data_raw_additional_test_"+ seed2+ ".csv"
#     raw_test = data_dir + "data_raw_additional_test_"+ seed2+ ".csv"
#     raw_val = data_dir + "data_raw_additional_test_"+ seed2+ ".csv"
#     ysxt_train = data_dir + "feateng/" + "data_additional_train_"+ seed2+ ".txt"
#     ysxt_test = data_dir + "feateng/" + "data_additional_test_"+ seed2+ ".txt"
#     ysxt_val = data_dir + "feateng/" + "data_additional_val_"+ seed2+ ".txt"
#     featindex = data_dir + "feateng/featindex_2.txt"
#     build_feat_index(featindex)
#     build_ysxt_data(raw_train, raw_test, raw_val,  ysxt_train, ysxt_test, ysxt_val)
#
# raw_train = data_dir + "data_raw_additional_e2_test.csv"
# raw_test = data_dir + "data_raw_additional_e2_test.csv"
# raw_val = data_dir + "data_raw_additional_e2_test.csv"
# ysxt_train = data_dir + "feateng/" + "additional_train_e2.txt"
# ysxt_test = data_dir + "feateng/" + "additional_test_e2.txt"
# ysxt_val = data_dir + "feateng/" + "additional_validation_e2.txt"
#
# build_ysxt_data(raw_train, raw_test, raw_val,  ysxt_train, ysxt_test, ysxt_val)