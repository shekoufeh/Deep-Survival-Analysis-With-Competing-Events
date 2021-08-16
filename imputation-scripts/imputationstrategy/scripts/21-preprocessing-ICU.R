#libraries
library(tidyverse)
library("discSurv")

source("scripts/21-functions-imputation.R")

load("data/ICU/data.rda")
icu <- data

df_icu <- icu %>% 
  mutate(obj = row_number()) %>%
  mutate(status = e1*1 + e2*2 ) %>%
  select(obj, status, everything()) %>%
  mutate(across("age", ~round(., 1))) %>%
  mutate(day = round(day,0))

# chose event of interest variable
eoi <- "e2"
eventCols <-  c("e1", "e2")
timeCol <- "day"

# create path
f_path <- paste(getwd(),"/createddata/ICU/raw/", sep ="")
dir.create(f_path, showWarnings = FALSE)

rm(train_set, test_set, val_set)

set.seed(606585)
# sample train and test
for(stat in sort(unique(df_icu$status))){
  obj_list <- unique(df_icu$obj[df_icu$status == stat])
  # sample for each status
  if(! exists("train_set")){
    train_set <- sample(obj_list, length(obj_list) *0.6)
    test_set <- sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*5/8 )
    val_set <- obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))]
  }else{
    train_set <- c(train_set, sample(obj_list, length(obj_list) *0.6))
    test_set <- c(test_set, sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*5/8+1))
    val_set <- c(val_set, obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))])
  }
}

dataset <- df_icu
data_names <- c("status","e1", "e2","time","age", "SAPS_II","female","intubation","pneumonia","LRT","harn",
                "other_inf", "hospital","elective","emergency","card_pul", "neurological", "met_ren")
rm(df_icu, icu, data)  


dataset$obj <- NULL

for(seed2 in c(1, 12, 123, 1234, 4123, 5123, 6123, 7123, 8123, 9123 )){
  df_sample_syn <- DRSA_createSampledRawOutput21(dataS = dataset, eventCols = eventCols, eoi = eoi, timeCol = timeCol, seed2 = seed2)
  
  # new status
  df_sample_syn$status <- as.numeric(dataset[, eoi] == 1)
  
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

uncensored_df <- dataset
names(uncensored_df) <- data_names
uncensored_df$status <- uncensored_df$e1 *1 + uncensored_df$e2 *2
uncensored_df[, timeCol] <- NULL
uncensored_df$obj <- 1:nrow(uncensored_df)
# oder names like with sampled data
uncensored_df <- uncensored_df[, names(df_sample_syn)]

# obj must be in first column
writeObjects(data = uncensored_df, obj_set = train_set, path = f_path, name = paste("uncensored_train", sep = "_") )
writeObjects(data = uncensored_df, obj_set = test_set, path = f_path, name = paste("uncensored_test", sep = "_") )
writeObjects(data = uncensored_df, obj_set = val_set, path = f_path, name = paste("uncensored_val",  sep = "_") )



