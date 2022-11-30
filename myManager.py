from sqlalchemy import create_engine

SQL = 'postgresql://postgres@localhost/Training'

class myManager:

    def initDB(self):
        self.engine = create_engine(SQL, pool_pre_ping=True)

        # check which tables are available
        with self.engine.connect() as conn:
            athleteTableAvailable = self.engine.dialect.has_table(conn,"athletes")
            coursesTableAvailable = self.engine.dialect.has_table(conn, "courses")
            completedTableAvailable = self.engine.dialect.has_table(conn, "completed")

        if (athleteTableAvailable and coursesTableAvailable and completedTableAvailable):
            return

        # read SQL queries from files to create tables that are not available
        if(not athleteTableAvailable):
            athleteTableFile = open("createTableAthletes.txt", mode='r', encoding='utf-8')
            athleteTableText = athleteTableFile.read()
            athleteTableFile.close()

        if(not coursesTableAvailable):
            courseTableFile = open("createTableCourses.txt", mode='r', encoding='utf-8')
            courseTableText = courseTableFile.read()
            courseTableFile.close()

        if(not completedTableAvailable):
            completedTableFile = open("createTableCompleted.txt", mode='r', encoding='utf-8')
            completedTableText = completedTableFile.read()
            completedTableFile.close()
        
        # execute the SQL queries
        with self.engine.connect() as conn:
            if not athleteTableAvailable:
                conn.execute((athleteTableText))
            if not coursesTableAvailable:
                conn.execute((courseTableText))
            if not completedTableAvailable:
                conn.execute((completedTableText))

    # get a list of all course TNrs
    def getCourseNumbers(self):
        self.engine = create_engine(SQL, pool_pre_ping=True)
        courseNumbersSQLFile = open("getCourseNumbers.txt", mode='r', encoding='utf-8')
        courseNumbersSQLText = courseNumbersSQLFile.read()
        courseNumbersSQLFile.close()
        courseNumbers = []
        with self.engine.connect() as conn:
            data1 = conn.execute((courseNumbersSQLText))
            numbers = data1.fetchall()
            for n in numbers:
                courseNumbers.append(n[0])
        return courseNumbers
    
    # get a list of all athlete IDs
    def getAthleteNumbers(self):
        self.engine = create_engine(SQL, pool_pre_ping=True)
        courseNumbersSQLFile = open("getAthleteNumbers.txt", mode='r', encoding='utf-8')
        courseNumbersSQLText = courseNumbersSQLFile.read()
        courseNumbersSQLFile.close()
        courseNumbers = []
        with self.engine.connect() as conn:
            data1 = conn.execute((courseNumbersSQLText))
            numbers = data1.fetchall()
            for n in numbers:
                courseNumbers.append(n[0])
        return courseNumbers
    
    # get a table of all training dates and corresponding data
    def getTrainingDates(self):
        self.engine = create_engine(SQL, pool_pre_ping=True)
        courseNumbersSQLFile = open("getTrainingDates.txt", mode='r', encoding='utf-8')
        courseNumbersSQLText = courseNumbersSQLFile.read()
        courseNumbersSQLFile.close()
        with self.engine.connect() as conn:
            data1 = conn.execute((courseNumbersSQLText))
            dates = data1.fetchall()
        return dates
    
    #add the athlete
    def addAthlete(self, Name, Weight, Size, Gender):
        self.engine = create_engine(SQL, pool_pre_ping=True)
        addAthleteFile = open("addAthlete.txt", mode='r', encoding='utf-8')
        addAthleteText = addAthleteFile.read()
        addAthleteFile.close()
        addAthleteFormated = addAthleteText.format(Name,Weight,Size,Gender)

        with self.engine.connect() as conn:
            conn.execute((addAthleteFormated))
    
    # add the course
    def addCourse(self, Designation, Description):
        if (not hasattr(self,'engine')):
            self.engine = create_engine(SQL, pool_pre_ping=True)
        addCourseFile = open("addCourse.txt", mode='r', encoding='utf-8')
        addCourseText = addCourseFile.read()
        addCourseFile.close()
        addCourseFormated = addCourseText.format(Designation, Description)

        with self.engine.connect() as conn:
            conn.execute((addCourseFormated))
    
    # add the Traing Date
    def addCompleted(self, ID, TNr, Date, StartTime, EndTime):
        self.engine = create_engine(SQL, pool_pre_ping=True)
        addCompletedFile = open("addCompleted.txt", mode='r', encoding='utf-8')
        addCompletedText = addCompletedFile.read()
        addCompletedFile.close()
        addCompletedFormated = addCompletedText.format(ID,TNr,Date,StartTime,EndTime)

        with self.engine.connect() as conn:
            conn.execute((addCompletedFormated))

    # delete the course with TNr from the db
    def deleteCourse(self, TNr):
        if (not hasattr(self,'engine')):
            self.engine = create_engine(SQL, pool_pre_ping=True)
        deleteCourseFile = open("deleteCourse.txt", mode='r', encoding='utf-8')
        deleteCourseText = deleteCourseFile.read()
        deleteCourseFile.close()
        deleteCourseFormated = deleteCourseText.format(TNr)

        with self.engine.connect() as conn:
            conn.execute((deleteCourseFormated))

    # delete the athlete with ID from the db
    def deleteAthlete(self, ID):
        if (not hasattr(self,'engine')):
            self.engine = create_engine(SQL, pool_pre_ping=True)
        deleteAthleteFile = open("deleteAthlete.txt", mode='r', encoding='utf-8')
        deleteAthleteText = deleteAthleteFile.read()
        deleteAthleteFile.close()
        deleteAthleteFormated = deleteAthleteText.format(ID)

        with self.engine.connect() as conn:
            conn.execute((deleteAthleteFormated))

    # delete the Training Date with completedID from the db
    def deleteCompleted(self, completedID):
        if (not hasattr(self,'engine')):
            self.engine = create_engine(SQL, pool_pre_ping=True)
        deleteCourseFile = open("deleteCompleted.txt", mode='r', encoding='utf-8')
        deleteCourseText = deleteCourseFile.read()
        deleteCourseFile.close()
        deleteCourseFormated = deleteCourseText.format(completedID)

        with self.engine.connect() as conn:
            conn.execute((deleteCourseFormated))