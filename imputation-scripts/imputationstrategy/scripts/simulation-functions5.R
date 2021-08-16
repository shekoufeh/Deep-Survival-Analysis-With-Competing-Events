# subdistribution for type 1 
cdf1 <- function(t, p, eta){
  1-(1-p*(1-exp(-t)))^(exp(eta))
}

# probability for type 1
prob1 <- function(p, eta){
  1-(1-p)^exp(eta)
}

# inverse subdistribution for type 1 
invcdf1 <- function(p, u, eta, p1){
  -log(((1-p1*u)^(exp(-eta))-1+p)/p)
}

# discrete probability of censoring 
cens_dist <- function(b, limits){
  b_pot <- b^((length(limits)+1):1)
  ps    <- b_pot/sum(b_pot)
}

# one discrete observation 
all_disc_data <- function(X, beta1, beta2, p, b, limits){
  
  valid <- FALSE 
  while(!valid){
    n    <- nrow(X)
    eta1 <- X%*%beta1
    eta2 <- X%*%beta2
  
    p1  <- prob1(p, eta1)
    ev  <- sapply(1:n, function(j) rbinom(1,1,1-p1[j])+1)
  
    u1  <- runif(n, 0, 1)
    t1  <- invcdf1(p, u1, eta1, p1)
    t2  <- sapply(1:n, function(j) rexp(1, rate=exp(eta2[j])))

    t <- ifelse(ev==1, t1, t2)

    t_disc <- sapply(1:n, function(j) findInterval(t[j],limits)+1)
    C_disc <- sample(1:(length(limits)+1), n, prob=cens_dist(b, limits), replace=TRUE)
  
    time   <- sapply(1:n, function(j) min(C_disc[j], t_disc[j]))
  
    status <- ifelse(C_disc<t_disc, 0, ev)
    if(length(table(status))==3){
      valid <- TRUE
    }
  }
  
  t_data <- data.frame(time=time, status=status, C=C_disc)
  e_data <- model.matrix(~as.factor(status), data=t_data)[,-1]

  disc_data <- cbind(e_data, t_data, X)
  disc_data <- as.data.frame(disc_data)
  names(disc_data)[c(1:2)] <- c("e1","e2")
  
  return(disc_data)
}



