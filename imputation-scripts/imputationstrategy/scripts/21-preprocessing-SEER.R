rm(list=ls())

# load R packages 
library("tidyverse")
library("discSurv")


# input preprocessing functions
source("scripts/21-functions-imputation.R")

# create paths
f_path <- paste(getwd(),"/createddata/SEER/raw/", sep ="")
dir.create(f_path, showWarnings = FALSE)

#  initialize parameters
seed <- 606585
eoi <- "e1"
eventCols <- c("e1", "e2")
timeCol <- "time"
set.seed(seed)

# inread dataset
seer_data <- read.table("data/SEER/SEER-competing-risks.csv",
                        sep = ",",
                        header = TRUE)

# preprocess
seer_data$status <- seer_data$state
seer_data$e1 <- (seer_data$state == 1) *1.0
seer_data$e2 <- (seer_data$state > 1) *1.0
seer_data$time <- seer_data$time.discrete.year
seer_data$time.discrete.year <- NULL
seer_data$state <- NULL
seer_data$obj <- 1:nrow(seer_data)

# create site mapping
seer_data$siteo2 <- factor(seer_data$siteo2)
write.table(data.frame(siteo2 = unique(seer_data$siteo2), level = unique(as.numeric(seer_data$siteo2))),
            file = paste("data/SEER/site_mapping.csv", sep =""))
seer_data$siteo2 <- as.numeric(seer_data$siteo2)

# sample train and test
for(stat in sort(unique(seer_data$status))){
  obj_list <- unique(seer_data$obj[seer_data$status == stat])
  # sample for each status
  if(! exists("train_set")){
    train_set <- sample(obj_list, length(obj_list) *0.5)
    test_set <- sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*0.6)
    val_set <- obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))]
  }else{
    train_set <- c(train_set, sample(obj_list, length(obj_list) *0.5))
    test_set <- c(test_set, sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*0.6))
    val_set <- c(val_set, obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))])
  }
}
seer_data$obj <- NULL

# reorder columns: time | status | X
seer_data <- seer_data[c("time", "status", "marstat","racrecy", "nhia", "agedx", "siteo2", "lateral", "grade", "eod10pn", "eod10ne",
                         "radiatn", "radsurg", "numprims", "erstatus", "prstatus", "adjtm6value", "adjnm6value",
                         "tumorsize", "surgprimRecode", "e1", "e2" )]


for(seed2 in c(1, 12, 123, 1234, 4123, 5123, 6123, 7123, 8123, 9123 )){
  df_sample_syn <- DRSA_createSampledRawOutput21(dataS = seer_data, eventCols = eventCols, eoi = eoi, timeCol = timeCol, seed2 = seed2)
  
  # new status
  df_sample_syn$status <- as.numeric(seer_data[, eoi] == 1)
  
  # drop columns
  df_sample_syn[, c("subDistWeights", "v_samplegew", "y", eventCols, "time", "day")] <- NULL
  # rename
  df_sample_syn <- df_sample_syn %>% rename(time = timeInt) %>% arrange(obj) %>% data.frame()
  
  
  print(paste("Size of Training Set:", length(unique(train_set))))
  # write sampled objects
  writeObjects(data = df_sample_syn, obj_set = train_set, path = f_path, name = paste("train", seed2, sep = "_") )
  writeObjects(data = df_sample_syn, obj_set = test_set, path = f_path, name = paste("test", seed2, sep = "_") )
  writeObjects(data = df_sample_syn, obj_set = val_set, path = f_path, name = paste("val", seed2, sep = "_") )
}

uncensored_df <- seer_data
uncensored_df$status <- uncensored_df$e1 *1 + uncensored_df$e2 *2
uncensored_df[, c("e1", "e2")] <- NULL
uncensored_df$obj <- 1:nrow(uncensored_df)
# oder names like with sampled data
uncensored_df <- uncensored_df[, names(df_sample_syn)]

writeObjects(data = uncensored_df, obj_set = train_set, path = f_path, name = paste("e2_train", sep = "_") )
writeObjects(data = uncensored_df, obj_set = test_set, path = f_path, name = paste("e2_test", sep = "_") )
writeObjects(data = uncensored_df, obj_set = val_set, path = f_path, name = paste("e2_val",  sep = "_") )

rm(train_set, test_set, val_set)
