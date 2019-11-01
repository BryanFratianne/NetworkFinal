import csv
from socket import *  # for use of socket
from _thread import *


def checkAllRanks(connectionSocket):
    result = ""
    with open("teams.txt", newline='') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            result += str(row[0]) + str(row[3])
            "\n"
    connectionSocket.send(result.encode())


def checkSpecificRank(connectionSocket, desiredTeam):
    result = ""  # Small explanation for how csv works for reading files
    with open("teams.txt", newline='') as f:  # Opens the file
        reader = csv.reader(f,
                            delimiter="\t")
        # Sets a reader for the file, while setting the delimiter for different options in a row as a tab.
        for row in reader:  # Goes through each row in the file, with a loop.
            if row[0] == desiredTeam:
                # row[0] means the first item in the row, items seperated by tabs, the defined delimiter.
                # In the Teams text file, the first item of each row will be the team name.
                result = str(row[0]) + str(row[3]) + "\n"  # row[3] holds their overall rank
                break  # Break the loop, since we don't need to go farther and Python doesn't have a way of just going to one line in a file :/
                # All the breaks during CSV reading loops are here for this exact reason.

    if result == "":
        result = "TeamNameNotFound"  # Catch for if the name is not found and send an error message.
    connectionSocket.send(result.encode())


def adjustScore(connectionSocket, gameNum):
    result = ""
    with open("games.txt", newline='') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if reader.line_num == gameNum:
                result = row
                break

    if result == "":
        result = "GameNumNotFound"  # Catch for if the name is not found and send an error message.
        connectionSocket.send(result.encode())
    else:
        connectionSocket.send(result.encode())
        newScore = connectionSocket.recv(1024).decode()
        with open("games.txt", newline='') as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                if reader.line_num == gameNum:  # The game number is based on the row of the game column
                    row[
                        2] = newScore
                    # Column 2 in games file has the score - There is one score per game shared between players
                    changeAverageScore(row[0], newScore)
                    changeAverageScore(row[1], newScore)  # Columns 0 and 1 contain the names of the two teams
                    updateRankings()
                    break


def changeAverageScore(desiredTeam, score):  # Function to update the designated teams score
    with open("teams.txt", newline='') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if row[0] == desiredTeam:
                row[1] += score  # Add the new score to their total, in row[1]
                row[2] += 1  # Add 1 to their total games played, in row[2]


def updateRankings():  # Function to update the rankings between all players
    with open("teams.txt", newline='') as f:
        teamCount = sum(1 for row in f)  # Sums up the total number of teams based on the lines in the teams file.
        scoreList = [0] * teamCount  # create list to hold the list of average scores.
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            scoreList[reader.line_num] = row[1] / row[2]  # Set each teams score in the list to their average.
        scoreList.sort()
        for row in reader:
            for i in range(teamCount):
                if (row[1] / row[2]) == scoreList[i]:  # Find the teams score in the sorted list of scores
                    row[3] = i + 1  # Set their rank to the position of the score in the sorted list. (Plus one)
                    break


def checkFullSchedule(connectionSocket):
    result = ""
    with open("games.txt", newline='') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            result += str(row) + "\n"
    connectionSocket.send(result.encode())


def checkSpecificSchedule(connectionSocket, desiredTeam):
    result = ""
    with open("games.txt", newline='') as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if desiredTeam in (row[1], row[2]):
                result += str(row) + "\n"
    connectionSocket.send(result.encode())
    if result == "":
        result = "TeamNameNotFound"  # Catch for if the name is not found and send an error message.
    connectionSocket.send(result.encode())


def newServerThread(connectionSocket):
    # Obtain the request from the client
    clientRequest = connectionSocket.recv(1024).decode()
    # Check the method
    methodName = clientRequest.split("\t")[0].strip()
    connected = True
    while connected is True:
        if methodName == "checkAllRanks":
            checkAllRanks(connectionSocket)

        elif methodName == "CheckSpecificRank":
            desiredTeam = clientRequest.split("\t")[1].strip()
            checkSpecificRank(connectionSocket, desiredTeam)

        elif methodName == "adjustScore":
            gameNum = clientRequest.split("\t")[1].strip()
            adjustScore(connectionSocket, gameNum)

        elif methodName == "CheckFullSchedule":
            checkFullSchedule(connectionSocket)

        elif methodName == "CheckSpecificSchedule":
            desiredTeam = clientRequest.split("\t")[1].strip()
            checkSpecificSchedule(connectionSocket, desiredTeam)

        elif methodName == "Exit":
            connected = False

    # Close the socket
    connectionSocket.close()


def serverMain():
    # Create a server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Define  a server port number and bind it to the server socket
    serverPort = 8080
    # Let the server socket start to listen to incoming connection requests
    serverSocket.bind(("", serverPort))
    serverSocket.listen(10)
    print("Connected!")
    # Create an infinite loop to process all connection requests
    while True:
        # Create a connection socket for each connection request received
        connectionSocket, addr = serverSocket.accept()
        print("from ", addr)
        start_new_thread(newServerThread, (connectionSocket))


serverMain()
