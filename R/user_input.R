# import necessary libraries
library(DBI)
library(RPostgreSQL)
library(ggplot2)

# Specify database parameters
dsn_database = "postgresql://postgres@localhost/Training"   # Specify the database location
dsn_hostname = "localhost"                                  # Specify the host. e.g. localhost
dsn_port = "5432"                                           # Specify the port number. e.g. 1234
dsn_uid = "postgres"                                        # Specify the username. e.g. "admin"
# dsn_pwd = ""                                                Specify the password. Currently, no password has been set.

# Try connecting to the database
tryCatch({
  drv <- dbDriver("PostgreSQL")
  print("Connecting to Database…")
  connec <- dbConnect(drv, 
                      dbname = dsn_database,
                      host = dsn_hostname, 
                      port = dsn_port,
                      user = dsn_uid,
                      password = dsn_pwd)
  
  print("Database Connected!")
},

# Return an error if the connection cannot be established
error=function(cond) {
  print("Unable to connect to Database.")
})

# Function for exercise 1
workouts_specific_athlete <- function(id){
  query <- paste0("select a.id, a.tnr, a.date, a.starttime, a.endtime, b.designation
  from completed as a join courses as b on a.tnr=b.tnr where a.id=",id,";")
  df <- dbGetQuery(connec, query)
  return(df)
}

# Function for exercise 2
avg_duration_athlete <- function(id){
  query <- paste0("select AVG(endtime-starttime) as average from completed where id=", id, ";")
  df <- dbGetQuery(connec, query);
  return(df)
}

# Function for exercise 3
avg_duration_athlete_training <- function(id, tnr){
  query <- paste0("select AVG(endtime-starttime) as average from completed where id=",id," and tnr=",tnr,";")
  df <- dbGetQuery(connec, query);
  return(df)
}

# Function for exercise 4
avg_duration_training <- function(tnr){
  query <- paste0("select AVG(endtime-starttime) as average from completed where tnr=", tnr, ";")
  df <- dbGetQuery(connec, query);
  return(df)
}

# Function for exercise 5
median_duration_training <- function(tnr){
  query <- paste0("select PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (endtime-starttime)) as median 
                 from completed where tnr=", tnr, ";")
  df <- dbGetQuery(connec, query);
  return(df)
}

# Function for exercise 6
std_duration_training <- function(tnr){
  query <- paste0("SELECT stddev(EXTRACT(EPOCH FROM (endtime-starttime))/60) as stddev from completed where tnr=", tnr, ";")
  df <- dbGetQuery(connec, query);
  return(df)
}

# Function for exercise 7
visualization_training_durations <- function(tnr){
  query <- paste0("SELECT (EXTRACT(EPOCH FROM (endtime-starttime))/60) as minutes from completed where tnr=", tnr, ";")
  df <- dbGetQuery(connec, query);
  p <- ggplot(df, aes(x="athlete", y=minutes)) + geom_boxplot() + geom_dotplot(binaxis='y', stackdir='center', stackratio=1.5, dotsize=1.2)
  return(p)
}

# Function for exercise 8
visualization_avg_training_durations_per_athlete <- function(tnr){
  query <- paste0("SELECT id, avg(EXTRACT(EPOCH FROM (endtime-starttime))/60) as minutes from completed group by id;")
  df <- dbGetQuery(connec, query);
  p <- ggplot(df, aes(x=factor(id), y=minutes)) + geom_bar(stat = "identity")
  return(p)
}

# Function to retrieve and process user inputs
start_function <- function() {

  # Generate a menu for the user to select which task should be executed
  selection <- menu(c("Workouts of specific athlete", "Average training duration (specific athlete over all trainings)", 
                      "Average training duration (specific training of specific athlete)", 
                      "Average training duration (specific training)", 
                      "Median training duration (specific training)", 
                      "Standard deviation of the training duration (specific training)", 
                      "Visualization of training durations (specific training)", 
                      "Visualization of the training duration over all athletes (average over all trainings per athlete)",
                      "Exit"), title="\n What would you like to do?")
  
  
  # Execute the selected task by retrieving additional user input if necessary, 
  # calling the specific function and printing the output
  if (selection==1){
    id <- readline(prompt="Enter athlete id: ")
    result <- workouts_specific_athlete(id)
    print(result)
    start_function()
  }
  else if (selection==2){
    id <- readline(prompt="Enter athlete id: ")
    result <- avg_duration_athlete(id)
    print(result)
    start_function()
  }
  else if (selection==3){
    id <- readline(prompt="Enter athlete id: ")
    tnr <- readline(prompt="Enter training id: ")
    result <- avg_duration_athlete_training(id, tnr)
    print(result)
    start_function()
  }
  else if (selection==4){
    tnr <- readline(prompt="Enter training id: ")
    result <- avg_duration_training(tnr)
    print(result)
    start_function()
  }
  else if (selection==5){
    tnr <- readline(prompt="Enter training id: ")
    result <- median_duration_training(tnr)
    print(result)
    start_function()
  }
  else if (selection==6){
    tnr <- readline(prompt="Enter training id: ")
    result <- std_duration_training(tnr)
    print(result)
    start_function()
  }
  else if (selection==7){
    tnr <- readline(prompt="Enter training id: ")
    result <- visualization_training_durations(tnr)
    print(result)
    start_function()
  }
  else if (selection==8){
    result <- visualization_avg_training_durations_per_athlete()
    print(result)
    start_function()
  }
}

start_function()

dbDisconnect(connec)

# use source("path/to/script/user_input.R", echo=TRUE) to import the script from the RStudio console
