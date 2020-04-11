
# import subprocess
#
# subprocess.call("ssh -p24 jundic@csil-cpu1.csil.sfu.ca", shell = True)

import sys
import os
import psycopg2

def connectToDatabase():
    # user = input("Please put in your user name\n")
    # password = input("Please put in your password\n")
    # host = "localhost"
    # database = "cmpt354_jundic"

    try:
        # connection = psycopg2.connect(user = "jundic",
        #                               password = "ci...",
        #                               host = "cs-db1.csil.sfu.ca",
        #                               database = "cmpt354-jundic")

        connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      database = "cmpt354_jundic")

        cursor = connection.cursor()
        print("You are successfully connected to cmpt354_jundic!\n")

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


def printMenu():
        print("Thanks for rubbing the lamp! What would you like to do my dear master?\n")
        print("Press 1 to find all the competitions by a specific month --->(ID, titile) will be returned")
# Q1 (20 points) Find all competitions (calls for grant proposals) open at a user-specified month, which
# already have at least one submitted large proposal. For a proposal to be large, it has to request more
# than $20,000 or to have more than 10 participants, including the principle investigator. Return both
# IDs and the titles.

        print("Press 2 to find all the competitions by specific areas")
# Q2 (10 points) Next, modify your program for Q1 by allowing the user to specify the areas (e.g., biology
# and chemistry) (s)he is interested in, and only displaying the competitions where the submitted large
# proposals have principle investigators specified by the user.

        print("Press 3 to find the proposal(s) that request the largest amount of money by a specific area")
# Q3 (10 points) For a user-specified area, find the proposal(s) that request(s) the largest amount of
# money.

        print("Press 4 to find the proposal(s) that are awarded the largest amount before a specific date")
# Q4 (10 points) For a user-specified date, find the proposals submitted before that date that are awarded
# the largest amount of money.


        print("Press 5 to find the average requested/awarded discrepancy by a specific area")
# Q5 (10 points) For an area specified by the user, output its average requested/awarded discrepancy,
# that is, the absolute value of the difference between the amounts.


        print('''Press 6 to assign a set of reviewers to review a specific grant application by a specific ID.
                 A list of reviewers who are not in conflict with the proposal being reviewed
                 and have not reached the max of 3 proposals will be returned.''')
# Q6 (30 points) Reviewer assignment: Provide the user with the option of assigning a set of reviewers to
# review a specific grant application (research proposal), one proposal at a time. The proposal ID
# should be specified by the user. Before doing the reviewers assignment, the user should be able to
# request and receive a list of reviewers who are not in conflict with the proposal being reviewed,
# and who still have not reached the maximum of three proposals to review.

        print('''Press 7 to check a specific room is availabe at a specific date.
                 If yes, enter 3 competitions(calls) IDs to be discussed on that day
                 Otherwise, 'Impossible' will be returned''')
# Q7 (30 points) Meeting scheduling: Your application should check if the user-entered room is available
# at a the user-entered date. If yes, the user should be prompted to enter 3 competitions (calls)
# IDs to be discussed and decided on that day. If a competition cannot be scheduled to be discussed
# on that day (because some of the reviewers are not available), then the user should be prompted
# that scheduling a discussion on that particular competition is impossible on that day (a simplified
# version just returns “Impossible”). Here, for a reviewer “not to be available” means that he or she
# is scheduled to be in another room on the same day
        print("Press 8 to EXIT the program ...");
        print("Press 0 to see the menu again");


def queryOne():
    print("from q1")

def queryTwo():
    print("from q2")

def queryThree():
    print("from q3")

def queryFour():
    print("from q4")

def queryFive():
    print("from q5")

def querySix():
    print("from q6")

def querySeven():
    print("from q7")





def main():
    # connectToDatabase();
    printMenu()
    while True:
        response = input("Prompt ==> ")
        while (not (response == '0' or response == '1' or response == '2' or response == '3' or response == '4' or response == '5' or response == '6' or response == '7' or response == '8')):
            response = input("Invalid command! Trying again: Prompt ==> ")
        if response == '0':
            printMenu()
        elif response == '1':
            queryOne()
        elif response == '2':
            queryTwo()
        elif response == '3':
            queryThree()
        elif response == '4':
            queryFour()
        elif response == '5':
            queryFive()
        elif response == '6':
            querySix()
        elif response == '7':
            querySeven()
        elif response == '8':
            print("I am going back to the lamp my master, rub the lamp to see me again next time!")
            return

main()
