# 06.08.2021
# Function for imputation of competing event times
require(tidyverse)

DRSA_createSampledRawOutput21 <- function(dataS = dataS, eventCols = c("e1", "e2"), eoi = "e1", timeCol = "time", seed2 = "1234"){
  set.seed(seed2)
  # initialize dataframe
  df_sample <-  data.frame(matrix(nrow = 0, ncol = ncol(dataS)+5 ) ) 
  names(df_sample) <- c("obj", "timeInt", "y", names(dataS), "subDistWeights", "v_samplegew") #
  
  for(eventofInerest in eoi){ # 
    # build augmented data matrix 
    dataLongSV <-
      dataLongSubDist(dataSet = dataS, timeColumn = timeCol, eventColumns = eventCols, eventFocus = eventofInerest) %>%
      group_by(obj) %>% 
      arrange(timeInt) %>% 
      mutate( v_samplegew =  (subDistWeights- rev(lag(rev(subDistWeights)))),
              maxt = max(as.numeric(timeInt))) %>% 
      # new version:
      # mutate(v_samplegew = ifelse(timeInt == maxt, subDistWeights, v_samplegew))%>%
      # old version:
      mutate( v_samplegew =   ( lag(subDistWeights) - subDistWeights)) %>%
      select(-maxt) %>%
      data.frame() 
    
    obj_list <- unique(dataLongSV$obj)
    
    # add subjects with events of interest to final df
    df <- cbind(dataLongSV[which(dataLongSV[, eventofInerest] == 1  &
                                   dataLongSV$timeInt == dataLongSV[,timeCol]), ])
    
    # add complete censored subjects
    tmp <- cbind(dataLongSV[which(rowSums(dataLongSV[, eventCols]) == 0 &
                                    dataLongSV$timeInt == dataLongSV[,timeCol]),])
    
    df <- rbind(df, tmp)
    
    
    # only impute subjects with competing event
    obj_list <- obj_list[!(obj_list %in% df$obj)]
    print(paste("Impute" , length(obj_list), "objects for event ", eventofInerest ))
    
    for (obj in obj_list) {
      tmp_subset <- dataLongSV[dataLongSV$obj == obj, ] 
      #tmp_subset$v_samplegew[is.na(tmp_subset$v_samplegew)] <- 0 # set v_ik = 0
      
      t_max <- max(as.numeric(tmp_subset$timeInt))
      
      if( (unique(tmp_subset[ ,timeCol]) != t_max) & sum(tmp_subset$v_samplegew)>0  ){
        #sampling
        t_tmp <- sample(tmp_subset$timeInt, 1, prob = tmp_subset$v_samplegew)
      }else{
        t_tmp <- t_max
      }
      
      tmp <-cbind(tmp_subset[tmp_subset$timeInt == t_tmp, ])
      
      df <- rbind(df, tmp)
    }
    df_sample <- rbind(df_sample, df)
  }
  return(df_sample)
}


# Write 3 files with colnames and row names
writeObjects <- function(data, obj_set, path, name ){
  write.table(x= data[data$obj %in% obj_set, -1 ],
              file = paste(path, "data_raw_", name, ".csv", sep = ""),
              sep =",",
              col.names = FALSE,
              row.names = FALSE,
              quote = FALSE)
  write.table(x= data[data$obj %in% obj_set, 1 ],
              file = paste(path, "obj_List_", name, ".csv", sep = ""),
              sep =",",
              col.names = FALSE,
              row.names = FALSE,
              quote = FALSE)
  write.table(x= names(data),
              file = paste(path, "names_", name, ".csv", sep = ""),
              sep =",",
              col.names = FALSE,
              row.names = TRUE)
}