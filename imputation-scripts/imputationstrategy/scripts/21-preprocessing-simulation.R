# Only genereate 1 dataset

# desired output:
# data_raw:   time | x | status
# obj_List: obj
# names: colnames


# load R packages 
library("tidyverse")
library("discSurv")

# input preprocessing functions
source("scripts/21-functions-imputation.R")
source("scripts/simulation-functions5.R")

eventCols <- c("e1", "e2")
eoi <- "e1"
timeCol <- "time"

one_sim_data <- function(seed, betas1, betas2, n, p, b, writeBeforeCensoring = FALSE ){
  # create one dataset and do not use loops and multiple data sets in a simulation setting.
  library(discSurv)
  # load required files for simulation (from Berger et al)
  source("scripts/simulation-functions_I.R")
  source("scripts/simulation-functions5.R")

  
  # compute quantiles 
  limits <- get_limits(p)
  
  # draw X
  set.seed(seed)
  x1 <- rnorm(n)
  x2 <- rnorm(n)
  x3 <- rbinom(n, 1, 0.5)
  x4 <- rbinom(n, 1, 0.5)
  X  <- cbind(x1, x2, x3, x4)
  
  # generate data set 
  valid <- FALSE
  while(!valid){
    data_disc <- all_disc_data(X, betas1, betas2, p, b, limits)
    if(length(table(data_disc[, "status"])) == 3){
      valid <- TRUE
    }
  }
  
  return(data_disc)
}


createSampleddata <- function(  p = 0.5, b = 0.91, n = 30000,  seed = 606585, seed2 = 1){
  # Function first creates a dataset as in Berger & Schmid Simulation approach. Within this
  # p: Event rate  of type 1 events (before censoring)
  # b: parameter for censoring wehere b = 1 euals medium cesoring ( censoring rate, rate of status 0 events = 0.5)
  
  # set seed 
  set.seed(seed)
  
  # create paths
  f_path <- paste(getwd(),"/createddata/simulation/raw/", seed, "/", sep ="")
  dir.create(f_path, showWarnings = FALSE)
  
  ### generate dataset
  # true coefficients 
  b1 <- c(0.4, -0.4, 0.2, -0.2)
  b2 <- c(-0.4, 0.4, -0.2, 0.2)
  
  # generate sampling dataset
  data_sim <- one_sim_data(seed = seed, betas1 = b1, betas2 = b2, n = 30000, p = p ,  b = b)
  data_sim$C <- NULL
  data_sim$obj <- 1:nrow(data_sim)
  print(cens_rate <- sum(data_sim$status==0)/nrow(data_sim))
  print(e1_rate <- sum(data_sim$status==1)/nrow(data_sim))
  print(e2_rate <- sum(data_sim$status==2)/nrow(data_sim))
  
  # TODO stratified Sampling
  ## Split in Train, Test & Validation
  # sample from censored, event 1 and event 2
  if(exists("train_set")| exists("test_set") | exists("val_set")){
    rm(train_set, test_set, val_set)
  }
  
  for(stat in sort(unique(data_sim$status))){
    obj_list <- unique(data_sim$obj[data_sim$status == stat])
    
    if(! exists("train_set")){
      train_set <- sample(obj_list, length(obj_list) *0.5+1)
      test_set <- sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*2/3+1)
      val_set <- obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))]
    }else{
      train_set <- c(train_set, sample(obj_list, length(obj_list) *0.5))
      test_set <- c(test_set, sample(obj_list[!(obj_list %in% train_set)], length(obj_list[!(obj_list %in% train_set)])*2/3))
      val_set <- c(val_set, obj_list[!((obj_list %in% train_set)| (obj_list %in% test_set))])
    }
  }
  
  # round features so that they can be fit into the model
  
  for(coln in c("x1", "x2")){
    data_sim[, coln] <- round(data_sim[, coln]/0.05) *0.05
  }
  
  
  # write dataset before sampling the censoring times
  writeObjects(data = data_sim[, c("obj", "time", "status", "x1", "x2", "x3", "x4")], obj_set = train_set, path = f_path, name = paste("uncensored_train", p, b, seed, seed2, sep = "_") )
  writeObjects(data = data_sim[, c("obj", "time", "status", "x1", "x2", "x3", "x4")], obj_set = test_set, path = f_path, name = paste("uncensored_test", p, b, seed, seed2, sep = "_") )
  writeObjects(data = data_sim[, c("obj", "time", "status", "x1", "x2", "x3", "x4")], obj_set = val_set, path = f_path, name = paste("uncensored_val", p, b, seed, seed2, sep = "_") )
  
  #break()
  data_sim$obj <- NULL
  
  ## Sampling of censoring time points strategy
  # Create raw dataframe
  df_sample_syn <- DRSA_createSampledRawOutput21(dataS = data_sim, eventCols = eventCols, eoi = eoi, timeCol = timeCol, seed2 = seed2)
  
  # new status
  df_sample_syn$status <- as.numeric(data_sim[, eoi] == 1)
  
  # drop columns
  df_sample_syn[, c("subDistWeights", "v_samplegew", "y", eventCols, "time", "day")] <- NULL
  # rename
  df_sample_syn <- df_sample_syn %>% rename(time = timeInt) %>% arrange(obj) %>% data.frame()
  
  print(paste("Size of Training Set:", length(unique(train_set))))
  
  # write sampled objects
  writeObjects(data = df_sample_syn, obj_set = train_set, path = f_path, name = paste("train", p, b, seed, seed2, sep = "_") )
  writeObjects(data = df_sample_syn, obj_set = test_set, path = f_path, name = paste("test", p, b, seed, seed2, sep = "_") )
  writeObjects(data = df_sample_syn, obj_set = val_set, path = f_path, name = paste("val", p, b, seed, seed2, sep = "_") )
}


for(p in c(0.2, 0.4, 0.8)){
  for(seed2 in  c(1, 12, 123, 1234, 4123, 5123, 6123, 7123, 8123, 9123)  ){
    print(paste("p:", p, "    seed2:", seed2))
    try(createSampleddata(  p = p, b = 1, n = 30000,  seed = 606585, seed2 = seed2))
  }
}

