
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import Grid

import myManager

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.man = myManager.myManager()
        self.man.initDB()

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageFour")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.refresh()
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main window - training management", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10,padx=50)

        button1 = tk.Button(self, text="Create Athlete",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Create Course",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Enter training data \n(Complete)",
                            command=lambda: controller.show_frame("PageThree"))
        button1.pack()
        button2.pack()
        button3.pack()

    def refresh(self):
        pass


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Window Title
        label = tk.Label(self, text="Create Athlete", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        gridFrame = tk.Frame(self)
        
        # Gender selector
        variableGender = tk.StringVar(gridFrame)
        variableGender.set("female") # default value
        genderList = ["female", "male"]
        entryGender = tk.OptionMenu(gridFrame, variableGender, *genderList)
        label01 = tk.Label(gridFrame, text="Gender", font=controller.title_font)
        label01.grid(row=0,column=0)
        #entry01 = tk.Entry(gridFrame)
        entryGender.grid(row=0,column=1,ipadx=30)

        # Name Field
        label02 = tk.Label(gridFrame, text="Name", font=controller.title_font)
        label02.grid(row=1,column=0)
        entry02 = tk.Entry(gridFrame)
        entry02.grid(row=1,column=1)

        # Weight Field
        labelWeight = tk.Label(gridFrame, text="Weight", font=controller.title_font)
        labelWeight.grid(row=2,column=0)
        entry03 = tk.Entry(gridFrame)
        entry03.grid(row=2,column=1)

        # Size Field
        label04 = tk.Label(gridFrame, text="Size", font=controller.title_font)
        label04.grid(row=3,column=0)
        entry04 = tk.Entry(gridFrame)
        entry04.grid(row=3,column=1)

        # ID selector
        self.variableID = tk.StringVar(gridFrame)
        athleteNumbers = controller.man.getAthleteNumbers()
        self.noAthletes = False
        if(len(athleteNumbers) == 0):
            self.noAthletes = True
            athleteNumbers = ["0"]
        self.variableID.set(athleteNumbers[0]) # set default value of drop down
        self.entryID = tk.OptionMenu(gridFrame, self.variableID, *athleteNumbers)
        self.label03 = tk.Label(gridFrame, text="ID", font=controller.title_font)
        self.noAthleetesLable = tk.Label(gridFrame, text="No Athletes available.", font=controller.title_font)
        if self.noAthletes:
            self.noAthleetesLable.grid(row=0,column=2)
        else:
            self.label03.grid(row=0,column=2)
            self.entryID.grid(row=0,column=3)

        # Button - Create Athlete
        button = tk.Button(gridFrame, text="Create Athlete",
                           command=lambda: (controller.man.addAthlete(entry02.get(),entry03.get(),entry04.get(),variableGender.get()), self.refresh()))
        button.grid(row=4,column=1)

        # Button - Delete Athlete
        self.deleteButton = tk.Button(gridFrame, text="Delete Athlete",
                           command=lambda: (controller.man.deleteAthlete(self.variableID.get()), self.refresh()))
        if not (self.noAthletes):
            self.deleteButton.grid(row=1,column=3)
        
        # Button - Back to Main Menue
        backButton = tk.Button(gridFrame, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        backButton.grid(row=5,column=0)

        gridFrame.pack(padx=20,pady=20)

    # refresh the ui when data has been changed (new athlete created or athlete deleted)
    def refresh(self):
        # get current athlete IDs from db
        athleteNumbers = self.controller.man.getAthleteNumbers()

        # check whether there are athletes available
        if(len(athleteNumbers) == 0):
            self.noAthletes = True
            athleteNumbers = ["0"]
        else:
            self.noAthletes = False
        self.variableID.set(athleteNumbers[0]) # set default value of drop down

        # remove current athlete IDs from dropdown
        menu = self.entryID["menu"]
        menu.delete(0, "end")

        # are there athletes available in the db
        if not self.noAthletes:
            # athletes available -> show athletes IDs in dropdown
            self.noAthleetesLable.grid_remove()
            self.label03.grid(row=0,column=2)
            self.entryID.grid(row=0,column=3)
            self.deleteButton.grid(row=1,column=3)
        else:
            # no athletes available -> show label no athletes available
            self.noAthleetesLable.grid(row=0,column=2)
            self.label03.grid_remove()
            self.entryID.grid_remove()
            self.deleteButton.grid_remove()
        # add current athlete IDs to dropdown
        for string in athleteNumbers:
            menu.add_command(label=string, 
                             command=lambda value=string: self.variableID.set(value))


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # window title
        label = tk.Label(self, text="Create Course", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        gridFrame = tk.Frame(self)
        
        # Designation Field
        label01 = tk.Label(gridFrame, text="Designation", font=controller.title_font)
        label01.grid(row=0,column=0)
        entry01 = tk.Entry(gridFrame)
        entry01.grid(row=0,column=1,ipadx=30)

        # Description Field
        label02 = tk.Label(gridFrame, text="Description", font=controller.title_font)
        label02.grid(row=1,column=0)
        entry02 = tk.Entry(gridFrame)
        entry02.grid(row=1,column=1)

        # TNr selector dropdown
        self.variableID = tk.StringVar(gridFrame)
        courseNumbers = controller.man.getCourseNumbers()
        self.noCourses = False
        if(len(courseNumbers) == 0):
            self.noCourses = True
            courseNumbers = ["0"]
        self.variableID.set(courseNumbers[0]) # set default value of dropdown
        self.entryID = tk.OptionMenu(gridFrame, self.variableID, *courseNumbers)
        self.label03 = tk.Label(gridFrame, text="TNr", font=controller.title_font)
        self.noCoursesLable = tk.Label(gridFrame, text="No Courses available.", font=controller.title_font)
        if self.noCourses:
            self.noCoursesLable.grid(row=0,column=2)
        else:
            self.label03.grid(row=0,column=2)
            self.entryID.grid(row=0,column=3)

        # Button - Create Course
        button = tk.Button(gridFrame, text="Create Course",
                           command=lambda:( controller.man.addCourse(entry01.get(), entry02.get()), self.refresh() ))
        button.grid(row=3,column=1)

        # Button - Delete Course
        self.deleteButton = tk.Button(gridFrame, text="Delete Course",
                           command=lambda: (controller.man.deleteCourse(self.variableID.get()), self.refresh() ))
        if not self.noCourses:
            self.deleteButton.grid(row=1,column=3)
        
        # Button - Back to Main Menue
        backButton = tk.Button(gridFrame, text="Back",
                           command=lambda: (controller.show_frame("StartPage")))
        backButton.grid(row=5,column=0)

        gridFrame.pack(padx=20,pady=20)
    
    # refresh the ui when data has changes (new course created or course deleted)
    def refresh(self):
        # get current course TNrs from db
        courseNumbers = self.controller.man.getCourseNumbers()
        # check whether there are courses available
        if(len(courseNumbers) == 0):
            self.noCourses = True
            courseNumbers = ["0"]
        else:
            self.noCourses = False
        self.variableID.set(courseNumbers[0]) # set default value of dropdown

        # clear the content of the dropdown
        menu = self.entryID["menu"]
        menu.delete(0, "end")

        # are there courses stored in the db
        if not self.noCourses:
            # courses available -> show dropdown of TNr of available courses
            self.noCoursesLable.grid_remove()
            self.label03.grid(row=0,column=2)
            self.entryID.grid(row=0,column=3)
            self.deleteButton.grid(row=1,column=3)
        else:
            # no courses available -> show label "no courses available"
            self.noCoursesLable.grid(row=0,column=2)
            self.label03.grid_remove()
            self.entryID.grid_remove()
            self.deleteButton.grid_remove()
        # add current course TNrs to dropdown
        for string in courseNumbers:
            menu.add_command(label=string, 
                             command=lambda value=string: self.variableID.set(value))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # window title
        label = tk.Label(self, text="Enter training data", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        gridFrame = tk.Frame(self)

        # Date Field
        label01 = tk.Label(gridFrame, text="Date", font=controller.title_font)
        label01.grid(row=0,column=0)
        entry01 = tk.Entry(gridFrame)
        entry01.grid(row=0,column=1,ipadx=30)

        # StartTime Field
        label02 = tk.Label(gridFrame, text="Start Time", font=controller.title_font)
        label02.grid(row=1,column=0)
        entry02 = tk.Entry(gridFrame)
        entry02.grid(row=1,column=1)

        # EndTime Field
        label03 = tk.Label(gridFrame, text="End Time", font=controller.title_font)
        label03.grid(row=2,column=0)
        entry03 = tk.Entry(gridFrame)
        entry03.grid(row=2,column=1)

        # Athlete ID selector dropdown
        self.variableAthleteID = tk.StringVar(gridFrame)
        athleteNumbers = controller.man.getAthleteNumbers()
        self.noAthletes = False
        if(len(athleteNumbers) == 0):
            self.noAthletes = True
            athleteNumbers = ["0"]
        self.variableAthleteID.set(athleteNumbers[0]) # default value
        self.entryAthleteID = tk.OptionMenu(gridFrame, self.variableAthleteID, *athleteNumbers)
        self.labelAthleteID = tk.Label(gridFrame, text="Athlete ID", font=controller.title_font)
        self.noAthleetesLable = tk.Label(gridFrame, text="No Athletes available.", font=controller.title_font)
        if self.noAthletes:
            self.noAthleetesLable.grid(row=0,column=2)
        else:
            self.labelAthleteID.grid(row=0,column=2)
            self.entryAthleteID.grid(row=0,column=3)

        # Course TNr selector dropdown
        self.variableCourseTNr = tk.StringVar(gridFrame)
        courseNumbers = controller.man.getCourseNumbers()
        self.noCourses = False
        if(len(courseNumbers) == 0):
            self.noCourses = True
            courseNumbers = ["0"]
        self.variableCourseTNr.set(courseNumbers[0]) # default value
        self.entryCourseID = tk.OptionMenu(gridFrame, self.variableCourseTNr, *courseNumbers)
        self.labelCourseTNr = tk.Label(gridFrame, text="Course No", font=controller.title_font)
        self.noCoursesLable = tk.Label(gridFrame, text="No Courses available.", font=controller.title_font)
        if self.noCourses:
            self.noCoursesLable.grid(row=1,column=2)
        else:
            self.labelCourseTNr.grid(row=1,column=2)
            self.entryCourseID.grid(row=1,column=3)

        # Button - Save Training Data
        self.saveTrainingButton = tk.Button(gridFrame, text="Save Training Data",
                           command=lambda:( controller.man.addCompleted(self.variableAthleteID.get(), self.variableCourseTNr.get(), entry01.get(), entry02.get(), entry03.get()) ))
        self.saveTrainingButton.grid(row=2,column=2,columnspan=2)

        # Button - Delete Training Data
        self.deleteTrainingButton = tk.Button(gridFrame, text="Delete Training Data",
                           command=lambda: controller.show_frame("PageFour"))
        self.deleteTrainingButton.grid(row=3,column=2,columnspan=2)

        # Button - Back to Main Menue
        button = tk.Button(gridFrame, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=5,column=0)
        gridFrame.pack(padx=20,pady=20)
    
    def refresh(self):
        # get current athlete and course ID from db
        courseNumbers = self.controller.man.getCourseNumbers()
        athleteNumbers = self.controller.man.getAthleteNumbers()

        # check whether there are courses available
        if(len(courseNumbers) == 0):
            self.noCourses = True
            courseNumbers = ["0"]
        else:
            self.noCourses = False
        # check whether there are athletes available
        if(len(athleteNumbers) == 0):
            self.noAthletes = True
            athleteNumbers = ["0"]
        else:
            self.noAthletes = False
        
        self.variableCourseTNr.set(courseNumbers[0]) # set default value for dropdown
        self.variableAthleteID.set(athleteNumbers[0]) # set default value for dropdown

        # cleear content of dropdown menues
        menuCourse = self.entryCourseID["menu"]
        menuCourse.delete(0, "end")
        menuAthlete = self.entryAthleteID["menu"]
        menuAthlete.delete(0, "end")

        # are there courses available?
        if not self.noCourses:
            # courses available -> show dropdown with course TNrs
            self.noCoursesLable.grid_remove()
            self.labelCourseTNr.grid(row=1,column=2)
            self.entryCourseID.grid(row=1,column=3)
        else:
            # no athletes courses -> show label "no courses available"
            self.noCoursesLable.grid(row=1,column=2)
            self.labelCourseTNr.grid_remove()
            self.entryCourseID.grid_remove()
        
        # are there athletes available?
        if not self.noAthletes:
            # athletes available -> show dropdown with athlete IDs
            self.noAthleetesLable.grid_remove()
            self.labelAthleteID.grid(row=0,column=2)
            self.entryAthleteID.grid(row=0,column=3)
        else:
            # no athletes available -> show label "no athletes available"
            self.noAthleetesLable.grid(row=0,column=2)
            self.labelAthleteID.grid_remove()
            self.entryAthleteID.grid_remove()

        # are courses or athletes available?
        if not (self.noCourses or self.noAthletes):
            # courses available AND athletes available -> show buttons to create or delete new Trainings)
            self.saveTrainingButton.grid(row=2,column=2,columnspan=2)
            self.deleteTrainingButton.grid(row=3,column=2,columnspan=2)
        else:
            # no courses available or no athletes available -> remove buttons to create ot delete trainings
            # (delete Button also removed, because there are no trainings to be deleted when there are no athletes or courses available
            self.saveTrainingButton.grid_remove()
            self.deleteTrainingButton.grid_remove()
        
        # add course TNrs in dropdown
        for string in courseNumbers:
            menuCourse.add_command(label=string, 
                             command=lambda value=string: self.variableCourseTNr.set(value))
        # add athlete IDs in dropdown
        for string in athleteNumbers:
            menuAthlete.add_command(label=string, 
                             command=lambda value=string: self.variableAthleteID.set(value))

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # window title
        label = tk.Label(self, text="Delete training data", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        gridFrame = tk.Frame(self)

        trainingDatesText = self.createList()

        self.trainingDatesStringVar = tk.StringVar(gridFrame)
        self.trainingDatesStringVar.set(trainingDatesText)
        self.listView = tk.Listbox(gridFrame,width=50,height=12,listvariable=self.trainingDatesStringVar)
        self.listView.grid(row=0,column=0,columnspan=2)

        # ToDo - make scrollbar usable
        scroll = tk.Scrollbar(
            gridFrame,
            orient='vertical',
            command=self.listView.yview
            )
        scroll.grid(row=0,column=2,sticky='ns')
        #self.listView.yview_scroll(number=10 ,what='units')

        self.listView.config(yscrollcommand = scroll.set)
  
        scroll.config(command = self.listView.yview)

        # Button - Delete Training data
        self.deleteTrainingButton = tk.Button(gridFrame, text="Delete Training Data",
                           command=lambda: (self.deleteTrainingDate(), self.refresh() ))
        self.deleteTrainingButton.grid(row=5,column=1,columnspan=1)

        # Button - Back
        button = tk.Button(gridFrame, text="Back",
                           command=lambda: controller.show_frame("PageThree"))
        button.grid(row=5,column=0)
        gridFrame.pack(padx=20,pady=20)
    
    # delete the Training date selected in the list view
    def deleteTrainingDate(self):
        id = self.listView.curselection()
        self.controller.man.deleteCompleted(self.trainingDates[id[0]][0])
    
    # get the current training dates from db and make a usable List for ListView
    def createList(self):
        self.trainingDates = self.controller.man.getTrainingDates()

        trainingDatesText = []
        for tD in self.trainingDates:
            dateText = tD[3] + " " + tD[4] + " " + tD[5] + " ("  + str(tD[6]) + " - "  + str(tD[7]) + ")"
            trainingDatesText.append(dateText)
        return trainingDatesText

    # refresh the ui when data has been changed (training date deleted)
    def refresh(self):
        listText = self.createList()
        self.trainingDatesStringVar.set(listText)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()