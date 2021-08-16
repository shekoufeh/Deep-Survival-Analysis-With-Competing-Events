import argparse
import random

features = ["age", "SAPS_II", "female", "intubation", "pneumonia", "harn", "other_inf", "hospital",
            "elective", "emergency", "card_pul", "neurological", "met_ren", "event"]

# feat_dict: featname: set()---distinct feat values
feat_dict = {}

# Event dict
event_dict = {'e1': 0, 'e2': 1}

# feat_size: field width
feat_size = {
    "age": 101 + 1,
    "SAPS_II": 97 + 1,
    "female": 2 + 1,
    "intubation": 2 +1 ,
    "pneumonia": 2 + 1,
    "harn": 2 + 1 ,
    "other_inf": 2 + 1,
    "hospital": 2 + 1,
    "elective": 2 + 1,
    "emergency": 2 + 1,
    "card_pul": 2 + 1,
    "neurological": 2 + 1,
    "met_ren": 2 + 1,
    "event": 2 + 1
}

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
    # TODO: Evtl feature Engeneering betreiben.
    if feat_name == "sodium":
        return int(float(str_val) * 2.5)
    elif feat_name == "creatinine":
        return int(float(str_val) * 6)
    #elif feat_name == "event":
    #    return int(event_dict[str_val])
    else:
        return int(float(str_val))


# build yzbx data
def build_yzbx_data(raw_train, raw_test, yzbx_train, yzbx_test):
    fnames_i = [raw_train, raw_test] #
    fnames_o = [yzbx_train, yzbx_test]

    for j in range(len(fnames_i)):
        yzbx_list = []
        with open(fnames_i[j], 'r') as f:
            lines = f.readlines()
            for line in lines:
                x_items = []
                # truncate
                x_items.append("0:1")
                line_items = line.split(',')
                for i in range(len(line_items) - 2): #(first is row ID), last two are z and b
                    feat_num = i + 1
                    feat_name = features[i]
                    feat_val = get_feat_val(feat_name, line_items[i])
                    key = "{}:{}".format(feat_num, feat_val)
                    if key not in feat_index.keys():
                        key = "{}:other".format(feat_num)
                    x_items.append("{}:1".format(feat_index[key]))
                # get b and z
                # t from hour to day
                z = line_items[-1].rstrip()
                b = line_items[-2]
                if b == 'NA':
                    z = int(float(z))
                    b = random.randint(z + 1, 2 * (z + 1))# Wie in DRSA example.
                else:
                    b = int(float(b))
                    z = random.randint(b + 1, 2 * (b + 1)) # Wie in DRSA example.
                # dummy y
                y = 0
                yzbx = ' '.join([str(y), str(z), str(b)] + x_items)
                yzbx_list.append(yzbx + '\n')

        with open(fnames_o[j], 'w') as f:
            f.writelines(yzbx_list)


# calculate features' statistical: max value, min value, mean value, and different value counts
def feat_stat(train, test):
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

    # print result
    for feat in features:
        stats = feat_dict[feat]
        print("{} result:".format(feat))
        print("max value:{0}    min value:{1}   distinct cnt:{2}".format(max(stats), min(stats), len(stats)))


def main(args):
    # calculate statistical results on dataset
    feat_stat(args.raw_train, args.raw_test)
    build_feat_index(args.featindex)
    build_yzbx_data(args.raw_train, args.raw_test, args.yzbx_train, args.yzbx_test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="feature engineering for SUPPORT clinical dataset")
    parser.add_argument(
        "--raw_train", action="store", required=True, help="raw train file name")
    parser.add_argument(
        "--raw_test", action="store", required=True, help="raw test file name")
    parser.add_argument(
        "--yzbx_train", action="store", required=True, help="train yzbx")
    parser.add_argument(
        "--yzbx_test", action="store", required=True, help="test yzbx")
    parser.add_argument(
        "--featindex", action="store", required=True, help="feature index")
    args = parser.parse_args()
    main(args)
