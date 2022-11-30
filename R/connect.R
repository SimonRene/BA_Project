
con<-dbConnect(RPostgres::Postgres())

library(DBI)

db <- 'Training'  #provide the name of your db

host_db <- 'localhost' #i.e. # i.e. 'ec2-54-83-201-96.compute-1.amazonaws.com'  

db_port <- '5432'  # or any other port specified by the DBA

db_user <- 'postgres'

con <- dbConnect(RPostgres::Postgres(), dbname = db, host=host_db, port=db_port, user=db_user)  

dbListTables(con) 



# All workouts of a specific athlete
task01 <- function(athleteID) {
  return ( dbGetQuery(con, paste('SELECT Courses.Designation, Completed.Date, Completed.StartTime, Completed.EndTime FROM Completed JOIN Courses ON Courses.TNr = Completed.TNr WHERE completed.id = ', athleteID, ' ;')))
   
}

task01(1)

# all workouts for specific athlete
task02 <- function(athleteID) {
  return(dbGetQuery(con, paste('SELECT AVG(EndTime-StartTime) as average FROM Completed WHERE id = ', athleteID, ' ;' )) )
}

task02(1)

# all workouts for specific athlete
task03 <- function(athleteID, trainingID) {
  return(dbGetQuery(con, paste('SELECT AVG(EndTime-StartTime) as average FROM Completed WHERE id = ', athleteID, 'and TNr = ', trainingID, ' ;' )) )
}

task03(1,1)

# all workouts for specific athlete
task04 <- function(trainingID) {
  return(dbGetQuery(con, paste('SELECT AVG(EndTime-StartTime) as average FROM Completed WHERE TNr = ', trainingID, ' ;' )) )
}

task04(1)

# all workouts for specific athlete
task05 <- function(trainingID) {
  durations <- dbGetQuery(con, paste('SELECT (EndTime-StartTime) as duration FROM Completed WHERE TNr = ', trainingID, ' ;' ))
  print(durations)
  
  return (median(durations))
}

task05(1)


# all workouts for specific athlete
task06 <- function(trainingID) {
  return(dbGetQuery(con, paste('SELECT STDDEV(EXTRACT(EPOCH FROM (EndTime - StartTime))/60) as stdDev FROM Completed WHERE TNr = ', trainingID, ' ;' )) )
}

task06(1)


# all workouts for specific athlete
task07 <- function(trainingID) {
  library(ggplot2)
  durations <- dbGetQuery(con, paste('SELECT EXTRACT(EPOCH FROM (EndTime - StartTime))/60 as duration FROM Completed WHERE TNr = ', trainingID, ' ;' ))
  
  #durations$id <- as.factor(durations$id)
  
  head(durations)
  
  plot = ggplot(durations, aes(x = duration))
  print(plot + geom_boxplot() + geom_dotplot(binaxis = "x", stackdir = "center", dotsize = 0.5))
  
  
  return (durations)
}

task07(1)


task08 <- function() {
  library(ggplot2)
  durations <- dbGetQuery(con, paste('SELECT id, avg(EXTRACT(EPOCH FROM (EndTime - StartTime))/60) as avgDuration FROM Completed GROUP BY id' ))
  
  #durations$id <- as.factor(durations$id)
  
  head(durations)
  plot = ggplot(data, aes(x = id, y = avgduration))
  print(plot + geom_col())
  
  
  return (durations)
  #'SELECT id, avg(EXTRACT(EPOCH FROM (EndTime - StartTime))/60) as avgDuration FROM Completed GROUP BY id'
}

task08()
