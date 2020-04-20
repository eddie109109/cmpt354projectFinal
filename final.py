import psycopg2


def createTableFunction():
    create_table_query = '''
            CREATE TABLE researcher(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(30) NOT NULL,
            lastname VARCHAR(30) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            organization VARCHAR(10)
            );

            CREATE TYPE callstatus AS ENUM('open','closed','paused','cancelled');

            CREATE TABLE call(
            id SERIAL PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            deadline DATE NOT NULL,
            description VARCHAR(250),
            area VARCHAR(30) NOT NULL,
            status callstatus DEFAULT 'open'
            );

            CREATE TYPE appstatus AS ENUM('submitted','awarded','denied');

            CREATE TABLE proposal(
            id SERIAL PRIMARY KEY,
            callid INT REFERENCES call(id) NOT NULL,
            pi INT REFERENCES researcher(id) NOT NULL,
            status appstatus DEFAULT 'submitted' NOT NULL,
            amount NUMERIC(14,2),
            requestamount NUMERIC(14,2)
            );

            CREATE TABLE collaborator(
            id SERIAL PRIMARY KEY,
            proposalid INT REFERENCES proposal(id) NOT NULL,
            researcherid INT REFERENCES researcher(id) NOT NULL,
            ispi BOOLEAN DEFAULT 'false' NOT NULL
            );

            CREATE TABLE conflict(
            id SERIAL PRIMARY KEY,
            researcher1 INT REFERENCES researcher(id) NOT NULL,
            researcher2 INT REFERENCES researcher(id) NOT NULL,
            reason VARCHAR(50),
            expiry DATE
            );

            CREATE TABLE review(
            id SERIAL PRIMARY KEY,
            reviewerid INT REFERENCES researcher(id) NOT NULL,
            proposalid INT REFERENCES proposal(id) NOT NULL,
            deadline DATE NOT NULL,
            submitted BOOLEAN DEFAULT 'false' NOT NULL
            );
            '''
    return create_table_query


def insertDataQuery():
    insert_data_query = '''
                        INSERT INTO researcher VALUES
                        (1,'Name','Lastname1','email1@sfu.ca','SFU'),
                        (2,'Name','Lastname2','email2@uvic.ca','UVIC'),
                        (3,'Name','Lastname3','email3@sfu.ca','SFU'),
                        (4,'Name','Lastname4','email4@uvic.ca','UVIC');
                        (5,'Name','Lastname5','email5@uvic.ca','UVIC');

                        INSERT INTO call VALUES
                        (1,'Canadian Inovation','2018-07-16',NULL,'computer science',DEFAULT),
                        (2,'Some Title','2018-03-03',NULL,'biology',DEFAULT),
                        (3,'Reduce Carbon Footprint','2018-12-30',NULL,'engineering','closed');
                        (4,'Environmental Issue','2018-02-03',NULL,'engineering',DEFAULT);

                        INSERT INTO proposal VALUES
                        (DEFAULT,2,1,'awarded',28000.00,25000),
                        (DEFAULT,1,2,'denied',NULL,10000.00),
                        (DEFAULT,3,3,'awarded',50000.00,30000.00);
                        (DEFAULT,4,4,'awarded',40000.00,40000.00);

                        INSERT INTO collaborator VALUES
                        (1,10,5,'t'),
                        (2,12,1,'f'),
                        (3,12,4,'t'),
                        (4,12,5,'t');

                        INSERT INTO conflict VALUES
                        (DEFAULT,1,2,'co-authered paper',now() + interval '2 year'),
                        (DEFAULT,4,5,'related',NULL),
                        (DEFAULT,3,7,'Same Department',NULL);

                        INSERT INTO review VALUES
                        (DEFAULT,6,3,now(),'t'),
                        (DEFAULT,7,1,now() + interval '2 week','f'),
                        (DEFAULT,6,1,now() + interval '2 week','t'),
                        (DEFAULT,1,2,now(),'t');
                        '''
    return insert_data_query


def createALLTables():
    # user = input("Please put in your user name\n")
    # password = input("Please put in your password\n")
    # host = "localhost"
    # database = "cmpt354_jundic"

    try:
        # connection = psycopg2.connect(user = "jundic",
        #                               password = "ci...",
        #                               host = "cs-db1.csil.sfu.ca",
        #                               database = "cmpt354-jundic")

        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()
        create_table_query = createTableFunction()
        insert_data_query = insertDataQuery()
        cursor.execute(create_table_query)
        cursor.execute(insert_data_query)
        connection.commit()
        print("All the tables created successfully in PostgreSQL! ")
        print("You are successfully connected to cmpt354_jundic!\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def printMenu():
    print("Thanks for rubbing the lamp! What would you like to do my dear master?\n")
    print("Press 1 to find all the competitions(calls) by a specific month --->(ID, titile) will be returned")
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
    print("Press 8 to EXIT the program ...")
    print("Press 0 to see the menu again")


def queryOne():
    selectedMonth = input("Please enter a month in NUMERIC form (esp: 1, 2...): Prompt ==> ")
    while (not (selectedMonth == '1' or selectedMonth == '2' or selectedMonth == '3' or selectedMonth == '4' or selectedMonth == '5' or selectedMonth == '6' or selectedMonth == '7' or selectedMonth == '8'or selectedMonth == '9' or selectedMonth == '10' or selectedMonth == '11' or selectedMonth == '12')):
        selectedMonth = input(
            "Invalid command! enter a month in NUMERIC form (esp: 1, 2...) Trying again: Prompt ==> ")
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        selectAll = '''
                    with month as (
                    select * from (select id, extract(month from deadline) from call) as month where month.date_part >= %s)
                    select DISTINCT call.id, call.title
                    from call, proposal, month, collaborator
                    where call.id = proposal.callid AND month.id = call.id AND
                    (proposal.requestamount > 20000.00 OR (select COUNT(collaborator.proposalid) from collaborator) >= 10);
                   '''
        cursor.execute(selectAll, (selectedMonth,))

        # print("Selecting rows from mobile table using cursor.fetchall")
        records = cursor.fetchall()

        print("Printing the result:")

        if len(records) == 0:
            print("There are no records matching your criteria!")
        else:
            for row in records:
                print(row)
        connection.commit()

        # return
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def queryTwo():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        showTotalResearchers = '''
                      select COUNT(*) from researcher;
                      '''

        cursor.execute(showTotalResearchers)

        record = cursor.fetchone()

        print("There are totally : " + str(record[0]) + " researchers")

        isTrue = True
        selectedPrincipleInvestigator = 0
        while isTrue:
            try:
                selectedPrincipleInvestigator = int(input(
                    "Please select the id number that is less or equal to " + str(record[0]) + ", Prompt ==> "))
                if selectedPrincipleInvestigator > record[0]:
                    print("The selected number is greater than " +
                          str(record[0]) + " please select again!")
                else:
                    isTrue = False
            except ValueError:
                print("This is not a whole number.")

        showAreas = '''
                    select DISTINCT area from call;
                    '''
        cursor.execute(showAreas)

        records = cursor.fetchall()

        print("The current areas we have are: ")
        for row in records:
            print(row[0])

        isTrue = True
        selectedArea = ""
        while isTrue:
            selectedArea = input(
                "Please enter the full name of the field that you would like to specify (case sensitive), Prompt ==> ")
            for row in records:
                if (selectedArea == row[0]):
                    isTrue = False

        print("One more data item to enter! ")
        selectedMonth = input("Please enter a month in NUMERIC form (esp: 1, 2...): Prompt ==> ")
        while (not (selectedMonth == '1' or selectedMonth == '2' or selectedMonth == '3' or selectedMonth == '4' or selectedMonth == '5' or selectedMonth == '6' or selectedMonth == '7' or selectedMonth == '8'or selectedMonth == '9' or selectedMonth == '10' or selectedMonth == '11' or selectedMonth == '12')):
            selectedMonth = input(
                "Invalid command! enter a month in NUMERIC form (esp: 1, 2...) Trying again: Prompt ==> ")

        # now the variable is selectedArea / selectedPrincipleInvestigator / selectedMonth

        selectAll = '''
                    with month as (
                    select * from (select id, extract(month from deadline) from call) as month where month.date_part >= %s)
                    select DISTINCT call.id, call.title
                    from call,month, proposal,collaborator
                    where call.id = proposal.callid AND month.id = call.id
                    AND call.area = %s AND proposal.pi = %s
                    AND (proposal.requestamount > 20000.00 OR (select COUNT(collaborator.proposalid) from collaborator) >= 10)
                    ;
                    '''

        cursor.execute(selectAll, (selectedMonth, selectedArea, selectedPrincipleInvestigator))
        records = cursor.fetchall()
        print("Printing the result:")
        if len(records) == 0:
            print("There are no records matching your criteria!")
            print("Try choosing engineering as the area and id as 3 if you want the check again!")
        else:
            for row in records:
                print(row)
        connection.commit()
        return

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def queryThree():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        showAreas = '''
                    select DISTINCT area from call;
                    '''
        cursor.execute(showAreas)

        records = cursor.fetchall()

        print("The current areas we have are: ")
        for row in records:
            print(row[0])

        isTrue = True
        selectedArea = ""
        while isTrue:
            selectedArea = input(
                "Please enter the full name of the field that you would like to specify (case sensitive), Prompt ==> ")
            for row in records:
                if (selectedArea == row[0]):
                    isTrue = False

        selectAll = '''
                    alter table proposal rename column id to proposalid ;
                    alter table proposal rename column status to proposalstatus ;
                    with newproposal as (select *
                    from proposal,call where proposal.callid = call.id AND call.area = %s)
                    select newproposal.proposalid, newproposal.callid, newproposal.pi, newproposal.proposalstatus, newproposal.amount, newproposal.requestamount
                    from newproposal
                    where newproposal.requestamount = (select MAX(requestamount) from newproposal);
                    '''

        # if i am not commiting i don't need to alter back
        alterColumnBack = '''
                        alter table proposal rename column proposalid to id ;
                        alter table proposal rename column proposalstatus to status;
                          '''
        cursor.execute(selectAll, (selectedArea,))

        records = cursor.fetchall()
        if len(records) == 0:
            print("There are no records matching your criteria!")
        else:
            print("Printing the matching proposal info:")
            # print("ID | callid | pi | status | amount | requestamount")
            for row in records:
                print("id: " + str(row[0]))
                print("callid: " + str(row[1]))
                print("pi: " + str(row[2]))
                print("status: " + str(row[3]))
                print("awarded amount: " + str(row[4]))
                print("requestamount: " + str(row[5]))

        # cursor.execute(alterColumnBack)
        # connection.commit()
        return

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def queryFour():
    isTrue = True
    selectedYear = 0
    while isTrue:
        try:
            selectedYear = int(input(
                "Please enter a year in NUMERIC form (esp: 2019,2018...): Prompt ==> "))
            if selectedYear > 2020 or selectedYear < 1:
                print("The year you have entered does not exist!")
            else:
                isTrue = False
        except ValueError:
            print("This is not a whole number.")

    selectedMonth = input("Please enter a month in NUMERIC form (esp: 1, 2...): Prompt ==> ")
    while (not (selectedMonth == '1' or selectedMonth == '2' or selectedMonth == '3' or selectedMonth == '4' or selectedMonth == '5' or selectedMonth == '6' or selectedMonth == '7' or selectedMonth == '8'or selectedMonth == '9' or selectedMonth == '10' or selectedMonth == '11' or selectedMonth == '12')):
        selectedMonth = input(
            "Invalid command! enter a month in NUMERIC form (esp: 1, 2...) Trying again: Prompt ==> ")

    selectedMonth = int(selectedMonth)

    isTrue = True
    selectedDay = 0
    while isTrue:
        try:
            selectedDay = int(input(
                "Please enter a date in NUMERIC form (esp: 31,30...): Prompt ==> "))
            if selectedDay > 31 or selectedDay < 1:
                print("The day you have entered does not exist!")
            else:
                isTrue = False
        except ValueError:
            print("This is not a whole number.")

    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        selectAll = '''
                    alter table proposal rename column id to proposalid ;
                    alter table proposal rename column status to proposalstatus;
                    with sub as
                    (select * from
                    call join proposal on proposal.callid = call.id),
                    subsub as
                    (select * from sub
                    where sub.deadline < '%s-%s-%s')
                    select subsub.proposalid, subsub.callid, subsub.pi, subsub.proposalstatus, subsub.amount, subsub.requestamount
                    from subsub
                    where subsub.amount = (select MAX(amount) from subsub)
                    ;
                    '''

        cursor.execute(selectAll, (selectedYear, selectedMonth, selectedDay))

        records = cursor.fetchall()

        print("Printing the result:")

        if len(records) == 0:
            print("There are no records matching your criteria!")
        else:
            for row in records:
                print("id: " + str(row[0]))
                print("callid: " + str(row[1]))
                print("pi: " + str(row[2]))
                print("status: " + str(row[3]))
                print("awarded amount: " + str(row[4]))
                print("requestamount: " + str(row[5]))
                print()
        # connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def queryFive():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        showAreas = '''
                    select DISTINCT area from call;
                    '''
        cursor.execute(showAreas)

        records = cursor.fetchall()

        print("The current areas we have are: ")
        for row in records:
            print(row[0])

        isTrue = True
        selectedArea = ""
        while isTrue:
            selectedArea = input(
                "Please enter the full name of the field that you would like to specify (case sensitive), Prompt ==> ")
            for row in records:
                if (selectedArea == row[0]):
                    isTrue = False

        selectAll = '''
                    with sub as
                    (select *
                    from proposal join call on proposal.callid = call.id
                    where call.area = %s and proposal.status = 'awarded'),
                    subsub as
                    (select ABS(amount - requestamount) AS discrepancy
                    from sub),
                    subsubsub as
                    (select count(discrepancy) as totalpeople, sum(discrepancy) as totaldiscrepancy
                    from subsub)
                    select ROUND((totaldiscrepancy/totalpeople),2) AS averagediscrepancy
                    from subsubsub
                    ;
                    '''

        cursor.execute(selectAll, (selectedArea,))

        record = cursor.fetchone()
        record = record[0]

        print("The average discrepancy amount for " + selectedArea + ":")

        if record == None:
            print("There are no records matching your criteria!")
        else:
            print(record)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def querySix():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        showResearchers = '''
                        select id, firstname, lastname from researcher;
                        '''

        showProposals = '''
                        alter table proposal rename column id to proposalid ;
                        alter table proposal rename column status to proposalstatus;
                        with newproposal as
                        (select * from
                        call join proposal on proposal.callid = call.id)
                        select newproposal.proposalid,newproposal.title,newproposal.proposalstatus, newproposal.amount, newproposal.requestamount
                        from newproposal
                        where newproposal.status = 'open'
                        '''

        alterColumnBack = '''
                        alter table proposal rename column proposalid to id ;
                        alter table proposal rename column proposalstatus to status;
                          '''

        showProposalid = '''
                        alter table proposal rename column id to proposalid ;
                        alter table proposal rename column status to proposalstatus;
                        with newproposal as
                        (select * from
                        call join proposal on proposal.callid = call.id)
                        select newproposal.proposalid
                        from newproposal
                        where newproposal.status = 'open'
                        '''
        cursor.execute(showResearchers)

        records = cursor.fetchall()

        print("All the researchers are: ")
        print("ID|first name|last name")
        for row in records:
            print(row)

        print()

        cursor.execute(showProposals)
        records = cursor.fetchall()
        totalProposals = []
        print("All the proposals that are still open for reviews: ")
        for row in records:
            totalProposals.append(row[0])  # store all the total proposals
            print("proposal id: " + str(row[0]))
            print("title: " + str(row[1]))
            print("status: " + str(row[2]))
            print("awarded amount: " + str(row[3]))
            print("requestamount: " + str(row[4]))
            print()

        cursor.execute(alterColumnBack)
        cursor.execute(showProposalid)
        availabeProposalIds = cursor.fetchall()

        list1 = []
        for row in availabeProposalIds:
            list1.append(row[0])

        # for i in range(len(list1)):  for testing whats inside the list
        #     print(list1[i])
        isTrue = True
        selectedProposalId = 0
        while isTrue:
            try:
                selectedProposalId = int(input(
                    "Please enter the proposal id that you want to pick from the availabe proposals above: Prompt ==> "))
                if selectedProposalId not in list1:
                    print("The proposal id you have entered does not exist!")
                else:
                    isTrue = False
                    totalProposals.remove(selectedProposalId)
            except ValueError:
                print("This is not a whole number.")

        print("The proposal id you have picked is: " + str(selectedProposalId))

        cursor.execute(alterColumnBack)

        getResearcherId = '''
                         select proposal.pi
                         from proposal
                         where proposal.id = %s
                         '''

        cursor.execute(getResearcherId, (selectedProposalId,))
        researchers = cursor.fetchall()

        list2 = []
        for row in researchers:
            list2.append(row[0])

        createTempTable = '''
                          CREATE TABLE temp(
                          id INT PRIMARY KEY,
                          researcherid INT NOT NULL
                          )
                          '''
        insertData = '''
                    INSERT INTO temp VALUES (%s,%s)
                     '''

        droptable = '''
                    DROP TABLE IF EXISTS temp
                    '''

        cursor.execute(createTempTable)
        for i in range(len(list2)):
            cursor.execute(insertData, (list2[i], list2[i]))

        getConflict = '''
                      select DISTINCT researcher2
                      from temp join conflict on temp.researcherid = conflict.researcher1
                      '''

        cursor.execute(getConflict)
        list3 = []
        conflicts = cursor.fetchall()
        for row in conflicts:
            list3.append(row[0])

        # cursor.execute(droptable)

        createTempTable2 = '''
                          CREATE TABLE temp2(
                          id INT PRIMARY KEY
                          )
                          '''

        insertData2 = '''
                    INSERT INTO temp2 VALUES (%s)
                     '''

        droptable2 = '''
                    DROP TABLE IF EXISTS temp2
                    '''

        cursor.execute(createTempTable2)
        for i in range(len(list3)):
            cursor.execute(insertData2, (list3[i],))

        selectNoneConflictResearchers = '''
                                        select * from researcher
                                        where researcher.id NOT IN (select id from temp2);
                                        '''

        getMaxConflict = '''
                        with sub as
                        (select reviewerid, COUNT(reviewerid) as totalReview
                        from review
                        where reviewerid  IN (select researcherid from temp) GROUP BY reviewerid)
                        select * from
                        sub where totalReview >=3;
                        '''

        cursor.execute(getMaxConflict)
        maxConflicts = cursor.fetchall()

        createTempTable3 = '''
                            CREATE TABLE temp3(
                            id INT PRIMARY KEY
                            );
                           '''
        insertData3 = '''
                    INSERT INTO temp3 VALUES (%s)
                     '''
        droptable3 = '''
                    DROP TABLE IF EXISTS temp3
                    '''

        if len(maxConflicts) == 0:
            cursor.execute(selectNoneConflictResearchers)

        else:
            list4 = []
            for row in maxConflicts:
                list4.append(row[0])

            cursor.execute(createTempTable3)
            for i in range(len(list4)):
                cursor.execute(insertData3, (list4[i],))

            selectNoneConflictResearchers = '''
                                            select * from researcher
                                            where researcher.id NOT IN (select id from temp2) AND researcher.id NOT IN (select id from temp3);
                                            '''
            cursor.execute(selectNoneConflictResearchers)

        records = cursor.fetchall()
        print("All the researchers info that are not in conflict with the targeted proposals:")
        noneConflictResearchers = []
        for row in records:
            noneConflictResearchers.append(row[0])
            print(row)

        # cursor.execute(droptable3)
        # cursor.execute(droptable)
        # cursor.execute(droptable2)

        inputList = []
        continueToAssign = True
        while len(totalProposals) > 0 and continueToAssign:
            isTrue = True
            selectedResearcher = 0
            while isTrue:
                try:
                    selectedResearcher = int(input(
                        "Please enter the (researcher id) from the availabe researchers above: Prompt ==> "))
                    if selectedResearcher not in noneConflictResearchers:
                        print("The researcher id you have entered does not exist!")
                    elif selectedResearcher in inputList:
                        print("This researcher id has been entered, please enter a different one!")
                    else:
                        inputList.append(selectedResearcher)
                        keepGoing = input(
                            "continue assgining more researchers for the current proposal?(y/n)?: Prompt==> ").lower()
                        if keepGoing == 'y':
                            continue
                        elif keepGoing == 'n':
                            print(str(len(inputList)) + " researchers assigned for the current proposal!")
                            inputList = []
                            isTrue = False
                        else:
                            print("Wrong answer, please try again!")

                except ValueError:
                    print("This is not a whole number.")

            print("The remaining (proposal id) are: ")
            for i in range(len(totalProposals)):
                print(totalProposals[i])
                print()

            nextAssignment = input(
                "continue to assgin for the next proposal(y/n)?: Prompt==> ").lower()
            if nextAssignment == 'y':
                cursor.execute(selectNoneConflictResearchers)
                records = cursor.fetchall()
                noneConflictResearchers = []

                print(
                    "All the researchers info:")
                for row in records:
                    noneConflictResearchers.append(int(row[0]))
                    print(row)

                isSecondTrue = True
                while isSecondTrue:
                    try:
                        selectedProposalId = int(input(
                            "Please enter the remaining (proposal id): Prompt ==> "))
                        if selectedProposalId not in totalProposals:
                            print("The researcher id you have entered does not exist!")
                        else:

                            isContinue = True
                            while isContinue:
                                try:
                                    selectedResearcher = int(input(
                                        "Please enter the (researcher id) from above: Prompt ==> "))
                                    if selectedResearcher not in noneConflictResearchers:
                                        print("The researcher id you have entered does not exist!")
                                    elif selectedResearcher in inputList:
                                        print(
                                            "This researcher id has been entered, please enter a different one!")
                                    else:
                                        inputList.append(selectedResearcher)
                                        keepGoing = input(
                                            "continue assgining more researchers for the current proposal?(y/n)?: Prompt==> ").lower()
                                        if keepGoing == 'y':
                                            continue
                                        elif keepGoing == 'n':
                                            print(str(len(inputList)) +
                                                  " researchers assigned for the current proposal!")
                                            inputList = []
                                            isContinue = False
                                            isSecondTrue = False
                                            # continueToAssign = False
                                            totalProposals.remove(selectedProposalId)
                                            if (len(totalProposals) == 0):
                                                print("All the proposals have been assgined to review!")
                                        else:
                                            print("Wrong answer, please try again!")

                                except ValueError:
                                    print("This is not a whole number.")

                    except ValueError:
                        print("This is not a whole number.")
                continue
            elif nextAssignment == 'n':
                continueToAssign = False
            else:
                print("Wrong answer, please try again!")

        cursor.execute(droptable3)
        cursor.execute(droptable)
        cursor.execute(droptable2)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def querySeven():
    isTrue = True
    selectedYear = 0
    while isTrue:
        try:
            selectedYear = int(input(
                "Please enter a year in NUMERIC form (esp: 2019,2018...): Prompt ==> "))
            if selectedYear > 2020 or selectedYear < 1:
                print("The year you have entered does not exist!")
            else:
                isTrue = False
        except ValueError:
            print("This is not a whole number.")

    selectedMonth = input("Please enter a month in NUMERIC form (esp: 1, 2...): Prompt ==> ")
    while (not (selectedMonth == '1' or selectedMonth == '2' or selectedMonth == '3' or selectedMonth == '4' or selectedMonth == '5' or selectedMonth == '6' or selectedMonth == '7' or selectedMonth == '8'or selectedMonth == '9' or selectedMonth == '10' or selectedMonth == '11' or selectedMonth == '12')):
        selectedMonth = input(
            "Invalid command! enter a month in NUMERIC form (esp: 1, 2...) Trying again: Prompt ==> ")

    selectedMonth = int(selectedMonth)

    isTrue = True
    selectedDay = 0
    while isTrue:
        try:
            selectedDay = int(input(
                "Please enter a date in NUMERIC form (esp: 31,30...): Prompt ==> "))
            if selectedDay > 31 or selectedDay < 1:
                print("The day you have entered does not exist!")
            else:
                isTrue = False
        except ValueError:
            print("This is not a whole number.")

    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      database="cmpt354_jundic")

        cursor = connection.cursor()

        selectAll = '''
                    select id, vacantdeadline from meeting
                    where meeting.vacantdeadline > '%s-%s-%s'
                    '''
        cursor.execute(selectAll, (selectedYear, selectedMonth, selectedDay))
        records = cursor.fetchall()

        availabeRooms = []
        if (len(records) == 0):
            print("There are no records matching your criteria!")
        else:
            print("The matching rooms info: ")
            print("id| availabe deadline")
            for row in records:
                availabeRooms.append(row[0])  # now we have all the availabeRooms
                print(row)
            print()

        isTrue = True
        selectedRoomId = 0
        while isTrue:
            try:
                selectedRoomId = int(input(
                    "Please enter a room id from above info: Prompt ==> "))
                if selectedRoomId not in availabeRooms:
                    print("The room id you have picked does not exist!")
                else:
                    isTrue = False
            except ValueError:
                print("This is not a whole number.")

        print("You have selected room #" + str(selectedRoomId))

        getConflictUserId = '''
                            select userid from meeting
                            where id = %s
                            '''

        cursor.execute(getConflictUserId, (selectedRoomId,))

        record = cursor.fetchone()
        conflictingId = record[0]

        # get the conflict id of the researcher whos using this room
        print("the conflict researcher id is: " + str(record[0]))

        getOpenCalls = '''
                        alter table proposal rename column id to proposalid ;
                        alter table proposal rename column status to proposalstatus;
                        with sub as
                        (select * from
                        call join proposal on proposal.callid = call.id)
                        select proposalid, callid, title,area from sub
                        where status = 'open'
                       '''

        alterColumnBack = '''
                        alter table proposal rename column proposalid to id ;
                        alter table proposal rename column proposalstatus to status;
                          '''

        cursor.execute(getOpenCalls)
        records = cursor.fetchall()
        list1 = []
        if (len(records) == 0):
            print("There are no records matching your criteria!")
        else:
            print("The matching calls info (calls are open for review): ")
            print()
            for row in records:
                # add in the researcher id  so that later i can check if it is present in the chosen id
                list1.append(row[1])
                print("id: " + str(row[0]))
                print("researcher id: " + str(row[1]))
                print("title: " + str(row[2]))
                print("area: " + str(row[3]))
                print()

        cursor.execute(alterColumnBack)

        inputList = []
        isTrue = True
        selectedId = 0
        while isTrue:
            try:
                selectedId = int(input(
                    "Please enter an id that is listed above(3 in total): Prompt ==> "))
                if selectedId not in list1:
                    print("The id you have entered does not exist(or have been entered already)!")
                else:
                    inputList.append(selectedId)
                    list1.remove(selectedId)
                    if (len(inputList) >= 3):
                        isTrue = False
            except ValueError:
                print("This is not a whole number.")

        if conflictingId in inputList:
            print("Impossible! researcher " + str(conflictingId) + " is occupied on that day!")
        else:
            print("You have successfully scheduled these three calls on this day!")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()


def main():
    # createALLTables();
    # i might need to get user name and password and pass them as params in each query
    # i can also prompt the TA to enter his/her database
    printMenu()
    while True:
        response = input("Main menu Prompt ==> ")
        while (not (response == '0' or response == '1' or response == '2' or response == '3' or response == '4' or response == '5' or response == '6' or response == '7' or response == '8' or response == '9')):
            response = input("Invalid command! Trying again: Main menu Prompt ==> ")
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
        elif response == '9':  # i need final fix on here and the menu
            createALLTables()


main()
