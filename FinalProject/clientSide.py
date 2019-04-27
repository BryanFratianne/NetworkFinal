from socket import *        # for use of socket
from tkinter import *
from tkinter import ttk
import tkinter.messagebox


def checkAllRanks(clientSocket):
    request = "CheckAllRanks\r \n"
    clientSocket.send(request.encode())
    response = clientSocket.recv(4096).decode("ascii")
    print("The current standings are: \n\n" + response + "\n")


def checkSpecificRank(clientSocket, team):
    request = "CheckSpecificRank\t" + team + "\r \n"
    clientSocket.send(request.encode())

    response = clientSocket.recv(4096).decode("ascii")

    if response != "TeamNameNotFound":
        print("Info for your current team: \n\n" + response + "\n")
    else:
        print("Sorry, that team name was no  found. \n\n")


def checkFullSchedule(clientSocket):
    request = "CheckFullSchedule\r\n"
    clientSocket.send(request.encode())

    response = clientSocket.recv(4096).decode("ascii")
    tkinter.messagebox.showinfo("Full Schedule", response)


def checkSpecificSchedule(clientSocket, team):

    request = "CheckSpecificRank\t" + team + "\r \n"
    clientSocket.send(request.encode())

    response = clientSocket.recv(4096).decode("ascii")

    if response != "TeamNameNotFound":
        print("Info for your current team: \n\n" + response + "\n")
    else:
        print("Sorry, that team name was no  found. \n\n")


def adjustScore(clientSocket):

    gameNum = input("enter game number: ")
    request = "adjustScore\t" + gameNum + "\r\n"

    clientSocket.send(request.encode())
    response = clientSocket.recv(4096).decode("ascii")

    if response != "GameNotFound":
        gameScore = input("enter the games score")
        clientSocket.send(gameScore.encode())
    else:
        print("Sorry, that game doesnt exist")


def clientMain():
    # Define  a server port number and server address
    serverName = "127.0.0.1"  # Use the same computer for test
    serverPort = 20120
    service = True

    while service:
        # Create a client TCP socket to connect with the server
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        window = Tk()
        window.title("Tournament App")

        # Window title label
        title = Label(window, text="Welcome to the Tournament App", font=("Helvetica", 40), bg="#ececec")
        title.pack(expand=1, fill="both")
        devs = Label(window, text="Developed by Josh Kraemer, Bryan Fratianne, and Alfredo Gomez",
                     font=("Helvetica", 20), bg="#ececec")
        devs.pack(expand=1, fill="both")

        # Size window to 700px X 500px
        window.geometry('700x500')

        # code for the tabs to cycle through functions
        tab_control = ttk.Notebook(window)

        # code to add tabs to the menu
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Check Rank')
        tab_control.add(tab2, text='Check Schedule')
        tab_control.add(tab3, text='Adjust Score')

        # Labels and positioning for the tabs
        tab1Lbl = Label(tab1, text="Check Rank", font=("Helvetica", 24), bg="#ececec")
        tab1Lbl.grid(column=0, row=0)

        # Internal widgets for the first function "CheckRank"
        rankResults = Label(tab1, text="Enter team name above: ", font=("Helvetica", 24), bg="#ececec")
        rankResults.grid(column=0, row=5)
        tab_control.pack(expand=1, fill="both")
        # input widget for the "CheckRank" function
        rankTxt = Entry(tab1, width=10, bg="#ececec")
        rankTxt.grid(column=0, row=1)

        # clicked and clear functions for the "CheckRank" function
        def rankClicked():

            inputV = str(rankTxt.get)
            res = "Rank results for: " + inputV

            rankResults.configure(text=res)
            checkSpecificRank(clientSocket, inputV)

        def rankClear():
            clearTxt = ""
            rankResults.configure(text="Enter team name above: ")

        rankBtn = Button(tab1, text="Check Rank", command=rankClicked, bg="#ececec")
        rankBtn.grid(column=0, row=4)

        rankAllBtn = Button(tab1, text="Check all Ranks", command=checkAllRanks, bg="#ececec")
        rankAllBtn.grid(column=1, row=4)

        rankClearBtn = Button(tab1, text="Clear", command=rankClear, bg="#ececec")
        rankClearBtn.grid(column=2, row=4)

        # Internal widgets for the second function "CheckSchedule"
        tab2Lbl = Label(tab2, text="Check Schedule", font=("Helvetica", 24), bg="#ececec")
        tab2Lbl.grid(column=0, row=0)

        scheduleResults = Label(tab2, text="Enter team name above: ", font=("Helvetica", 24), bg="#ececec")
        scheduleResults.grid(column=0, row=5)

        # input widget for the "CheckSchedule" function
        scheduleTxt = Entry(tab2, width=10, bg="#ececec")
        scheduleTxt.grid(column=0, row=1)

        # clicked and clear functions for the "CheckSchedule" function
        def scheduleClicked():
            res = "Schedule results for: " + scheduleTxt.get()
            scheduleResults.configure(text=res)
            checkSpecificSchedule(clientSocket, scheduleTxt.get())

        def scheduleClear():
            clearTxt = ""
            scheduleResults.configure(text="Enter team name above: ")

        scheduleBtn = Button(tab2, text="Check Schedule", command=scheduleClicked, bg="#ececec")
        scheduleBtn.grid(column=0, row=4)

        checkFullScheduleBtn = Button(tab2, text="Check the full schedule", command=checkFullSchedule(clientSocket),
                                      bg="#ececec")
        checkFullScheduleBtn.grid(column=1, row=4)

        scheduleClearBtn = Button(tab2, text="Clear", command=scheduleClear, bg="#ececec")
        scheduleClearBtn.grid(column=2, row=4)

        # Internal widgets for the third function "Adjust Score"
        tab3Lbl = Label(tab3, text="Adjust Score", font=("Helvetica", 24), bg="#ececec")
        tab3Lbl.grid(column=0, row=0)

        gameNum = Label(tab3, text="Enter game number and score above: ", font=("Helvetica", 24), bg="#ececec")
        gameNum.grid(column=0, row=5)

        # input widget for the "AdjustScore" function
        gameTxt = Entry(tab3, width=10, bg="#ececec")
        gameTxt.grid(column=0, row=1)

        scoreTxt = Entry(tab3, width=10, bg="#ececec")
        scoreTxt.grid(column=1, row=1)

        # clicked and clear functions for the "CheckSchedule" function
        def adjustClicked():
            res = "Adjustment results for game: " + gameTxt.get()
            gameNum.configure(text=res)

        def adjustClear():
            clearTxt = ""
            gameNum.configure(text="Enter game number and score above: ")

        adjustBtn = Button(tab3, text="Adjust Score", command=adjustClicked, bg="#ececec")
        adjustBtn.grid(column=0, row=4)

        adjustClearBtn = Button(tab3, text="Clear", command=adjustClear, bg="#ececec")
        adjustClearBtn.grid(column=1, row=4)

        window.mainloop()


clientMain()
