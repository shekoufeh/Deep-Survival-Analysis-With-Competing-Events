#0-preprocessing-CRASH2

# load R packages 
library("tidyverse")
library("discSurv")
library("mgcv")


# input preprocessing functions
source("scripts/21-functions-imputation.R")



# Preprocessing Script by Berger & Schmid for CRASH 2 creates crashD datasets
for(version_ in c("CRASH2da", "CRASH2bo")){# "CRASH2",
  f_path <- paste(getwd(),"/createddata/",version_,"/raw/", sep ="")
  dir.create(f_path, showWarnings = FALSE)
  
  #version_ <- "CRASH2bo" #"CRASH2bo"
  if(version_ =="CRASH2"){
    load("data/CRASH2/crash2-data.rda")
    crashD$obj <- 1:nrow(crashD)
  }else if(version_ == "CRASH2bo"){
    crashD <- read.csv("data/CRASH2bo/crash2bo.csv")
    # crashD$obj <- crashD$X
    crashD$obj <- 1:nrow(crashD)
    crashD$X <- NULL
  }else if(version_ == "CRASH2da"){
    crashD <- read.csv("data/CRASH2da/crash2da.csv")
    #crashD$obj <- crashD$X
    crashD$obj <- 1:nrow(crashD)
    crashD$X <- NULL
  }
  crashD <- crashD[, c("time", "status", "isex", "iage", "ninjurytime", "iinjurytype", "isbp", "ihr", "irr","igcs", "obj")]
  seed <- 606585
  seed2 <- 1
  crashD$e1 <- (crashD$status == 1) *1.0
  crashD$e2 <- (crashD$status > 1) *1.0
  rm(train_set)
  set.seed(seed)
  eoi <- "e1"
  timeInt <- "time"
  eventCols <- c("e1", "e2")
  
  
  # sample train and test
  for(stat in sort(unique(crashD$status))){
    obj_list <- unique(crashD$obj[crashD$status == stat])
    # sample for each status
    if(! exists("train_set")){
      train_set <- sample(obj_list, length(obj_list) *0.5)
      test_set <- sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*2/3)
      val_set <- obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))]
    }else{
      train_set <- c(train_set, sample(obj_list, length(obj_list) *0.5))
      test_set <- c(test_set, sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*2/3))
      val_set <- c(val_set, obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))])
    }
  }
  crashD$obj <- NULL
  
  for(seed2 in c(1, 12, 123, 1234, 4123, 5123, 6123, 7123, 8123, 9123 )){
    df_sample_syn <- DRSA_createSampledRawOutput21(dataS = crashD, eventCols = c("e1", "e2"), eoi = "e1", timeCol = "time", seed2 = seed2)
    
    # new status
    df_sample_syn$status <- as.numeric(crashD[, eoi] == 1)
    
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
  
  # write additional test sets
  
  
  uncensored_df <- crashD
  uncensored_df$status <- uncensored_df$e1 *1 + uncensored_df$e2 *2
  uncensored_df[, c("e1", "e2")] <- NULL
  uncensored_df$obj <- 1:nrow(uncensored_df)
  # oder names like with sampled data
  uncensored_df <- uncensored_df[, names(df_sample_syn)[(!names(df_sample_syn) %in%  c("e1", "e2"))]]
  
  # obj must be in first column
  writeObjects(data = uncensored_df, obj_set = train_set, path = f_path, name = paste("uncensored_train", sep = "_") )
  writeObjects(data = uncensored_df, obj_set = test_set, path = f_path, name = paste("uncensored_test", sep = "_") )
  writeObjects(data = uncensored_df, obj_set = val_set, path = f_path, name = paste("uncensored_val",  sep = "_") )
  
}
  