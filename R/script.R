
connect_to_db <- function() {
  library(DBI)
  db <- "Training"  #name of  db
  host_db <- "localhost"
  db_port <- "5432"
  db_user <- "postgres"
  #dbListTables(con) 
  return(dbConnect(RPostgres::Postgres(), dbname = db, host=host_db, port=db_port, user=db_user))
}

con <- connect_to_db()

# All workouts of a specific athlete
task01 <- function(athleteID) {
  return ( dbGetQuery(con, paste('SELECT Courses.Designation, Completed.Date, Completed.StartTime, Completed.EndTime FROM Completed JOIN Courses ON Courses.TNr = Completed.TNr WHERE completed.id = ', athleteID, ' ;')))
   
}

task01(1)

# Average over training duration of a certain athlete overall trainings
task02 <- function(athleteID) {
  return(dbGetQuery(con, paste('SELECT AVG(EndTime-StartTime) as average FROM Completed WHERE id = ', athleteID, ' ;' )) )
}

task02(1)

# Average of the training duration of a specific training of an athlete
task03 <- function(athleteID, trainingID) {
  return(dbGetQuery(con, paste('SELECT AVG(EndTime-StartTime) as average FROM Completed WHERE id = ', athleteID, 'and TNr = ', trainingID, ' ;' )) )
}

task03(1,1)

# Average of the training duration of a certain training over all athletes
task04 <- function(trainingID) {
  return(dbGetQuery(con, paste('SELECT AVG(EndTime-StartTime) as average FROM Completed WHERE TNr = ', trainingID, ' ;' )) )
}

task04(1)

# Median of the training duration of a certain training over all athletes
task05 <- function(trainingID) {
  durations <- dbGetQuery(con, paste('SELECT EXTRACT(EPOCH FROM (EndTime - StartTime))/60 as duration FROM Completed WHERE TNr = ', trainingID, ' ;' ))
  print(durations)
  
  return (median(durations))
}

task05(1)


# Standard deviation of the training duration of a certain training over all athletes
task06 <- function(trainingID) {
  return(dbGetQuery(con, paste('SELECT STDDEV(EXTRACT(EPOCH FROM (EndTime - StartTime))/60) as stdDev FROM Completed WHERE TNr = ', trainingID, ' ;' )) )
}

task06(1)


# Draw appropriate diagrams to visualize the data using ggplot
# All training duration values of a specific training
task07 <- function(trainingID) {
  library(ggplot2)
  durations <- dbGetQuery(con, paste('SELECT EXTRACT(EPOCH FROM (EndTime - StartTime))/60 as duration FROM Completed WHERE TNr = ', trainingID, ' ;' ))
  head(durations)
  plot = ggplot(durations, aes(x = duration))
  print(plot + geom_boxplot() + geom_dotplot(binaxis = "x", stackdir = "center", dotsize = 0.5))
  #return (durations)
}
task07(2)

# Draw appropriate diagrams to visualize the data using ggplot
# Average of the training duration over all athletes (i.e. per athlete average of the training duration over all trainings)
task08 <- function() {
  library(ggplot2)
  durations <- dbGetQuery(con, paste('SELECT id, avg(EXTRACT(EPOCH FROM (EndTime - StartTime))/60) as avgDuration FROM Completed GROUP BY id' ))
  
  plot = ggplot(durations, aes(x = id, y = avgduration))
  print(plot + geom_col())
  #return (durations)
}

task08()
