from sqlalchemy import create_engine

class myManager:
    def manage(self):
        print("MANAGING...")

    
    def initDB(self):
        self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)

        #engine = create_engine("postgresql://postgres@localhost/BAdb", echo=True, future=True)

        athleteTableFile = open("createTableAthletes.txt", mode='r', encoding='utf-8')
        athleteTableText = athleteTableFile.read()
        athleteTableFile.close()

        courseTableFile = open("createTableCourses.txt", mode='r', encoding='utf-8')
        courseTableText = courseTableFile.read()
        courseTableFile.close()

        completedTableFile = open("createTableCompleted.txt", mode='r', encoding='utf-8')
        completedTableText = completedTableFile.read()
        completedTableFile.close()


        # "commit as you go"
        with self.engine.connect() as conn:
            #conn.execute(("CREATE TABLE Persons3 (PersonID int,LastName varchar(255));"))
            #conn.execute((athleteTableText))
            #conn.execute((courseTableText))
            conn.execute((completedTableText))
            #conn.commit()
    
    def addTestData(self):
        self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        coursesTestFile = open("addTestData02.txt", mode='r', encoding='utf-8')
        coursesTestText = coursesTestFile.read()
        coursesTestFile.close()

        athletesTableFile = open("addTestData01.txt", mode='r', encoding='utf-8')
        athletesTestText = athletesTableFile.read()
        athletesTableFile.close()

        completedTableFile = open("addTestData03.txt", mode='r', encoding='utf-8')
        completedTestText = completedTableFile.read()
        completedTableFile.close()


        # "commit as you go"
        with self.engine.connect() as conn:
            #conn.execute(("CREATE TABLE Persons3 (PersonID int,LastName varchar(255));"))
            conn.execute((athletesTestText))
            conn.execute((coursesTestText))
            conn.execute((completedTestText))

    def getCourseNumbers(self):
        self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        courseNumbersSQL = "getCourseNumbers.txt"
        courseNumbersSQLFile = open("getCourseNumbers.txt", mode='r', encoding='utf-8')
        courseNumbersSQLText = courseNumbersSQLFile.read()
        courseNumbersSQLFile.close()
        courseNumbers = []
        with self.engine.connect() as conn:
            #conn.execute(("CREATE TABLE Persons3 (PersonID int,LastName varchar(255));"))
            data1 = conn.execute((courseNumbersSQLText))
            numbers = data1.fetchall()
            for n in numbers:
                courseNumbers.append(n[0])
        return courseNumbers
    
    def getAthleteNumbers(self):
        self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        courseNumbersSQLFile = open("getAthleteNumbers.txt", mode='r', encoding='utf-8')
        courseNumbersSQLText = courseNumbersSQLFile.read()
        courseNumbersSQLFile.close()
        courseNumbers = []
        with self.engine.connect() as conn:
            #conn.execute(("CREATE TABLE Persons3 (PersonID int,LastName varchar(255));"))
            data1 = conn.execute((courseNumbersSQLText))
            numbers = data1.fetchall()
            for n in numbers:
                courseNumbers.append(n[0])
        return courseNumbers
    
    def addAthlete(self, Name, Weight, Size, Gender):
        self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        addAthleteFile = open("addAthlete.txt", mode='r', encoding='utf-8')
        addAthleteText = addAthleteFile.read()
        addAthleteFile.close()
        addAthleteFormated = addAthleteText.format(Name,Weight,Size,Gender)

        with self.engine.connect() as conn:
            #conn.execute(("CREATE TABLE Persons3 (PersonID int,LastName varchar(255));"))
            conn.execute((addAthleteFormated))
    
    def addCourse(self, Designation):
        if (not hasattr(self,'engine')):
            self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        addCourseFile = open("addCourse.txt", mode='r', encoding='utf-8')
        addCourseText = addCourseFile.read()
        addCourseFile.close()
        addCourseFormated = addCourseText.format(Designation)

        with self.engine.connect() as conn:
            #conn.execute(("CREATE TABLE Persons3 (PersonID int,LastName varchar(255));"))
            conn.execute((addCourseFormated))
    
    def deleteCourse(self, TNr):
        if (not hasattr(self,'engine')):
            self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        deleteCourseFile = open("deleteCourse.txt", mode='r', encoding='utf-8')
        deleteCourseText = deleteCourseFile.read()
        deleteCourseFile.close()
        deleteCourseFormated = deleteCourseText.format(TNr)

        with self.engine.connect() as conn:
            conn.execute((deleteCourseFormated))

    def deleteAthlete(self, ID):
        if (not hasattr(self,'engine')):
            self.engine = create_engine('postgresql://postgres@localhost/Training', pool_pre_ping=True)
        deleteAthleteFile = open("deleteAthlete.txt", mode='r', encoding='utf-8')
        deleteAthleteText = deleteAthleteFile.read()
        deleteAthleteFile.close()
        deleteAthleteFormated = deleteAthleteText.format(ID)

        with self.engine.connect() as conn:
            conn.execute((deleteAthleteFormated))