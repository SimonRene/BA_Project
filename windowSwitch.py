
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import Grid


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
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

        # ID selector
        variableID = tk.StringVar(gridFrame)
        variableID.set("001") # default value
        idList = ["001", "002"]
        entryID = tk.OptionMenu(gridFrame, variableID, *idList)
        label03 = tk.Label(gridFrame, text="ID", font=controller.title_font)
        label03.grid(row=0,column=2)
        entryID.grid(row=0,column=3)

        # Button - Create Athlete
        button = tk.Button(gridFrame, text="Create Athlete",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3,column=1)

        # Button - Delete Athlete
        button02 = tk.Button(gridFrame, text="Delete Athlete",
                           command=lambda: controller.show_frame("StartPage"))
        button02.grid(row=1,column=3)
        
        # Button - Back to Main Menue
        backButton = tk.Button(gridFrame, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        backButton.grid(row=5,column=0)

        gridFrame.pack(padx=20,pady=20)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Create Course", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter training data", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()