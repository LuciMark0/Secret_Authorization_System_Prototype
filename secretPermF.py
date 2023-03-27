from secretPermB import Database

db = Database()


def menu():

    while (userInput:=input(accountPrompt)) != "3":
        if userInput == "1":
            if login():
                break
        elif userInput == "2":
            register()
        else:
            print("\nInvalid input, please try again!")
    else:
        exit()

    while (userInput:=input(menuPrompt)) != "6":
        if userInput == "1":
            vote_permissions()
        elif userInput == "2":
            vote_decision()
        elif userInput == "3":
            add_decision()
        elif userInput == "4":
            show_employees()
        elif userInput == "5":
            show_decisions()
        else:
            print("\nInvalid input, please try again!")

accountPrompt = """\n--- Secret Permission App ---

Please choose one of these options:

1) Login.
2) Register.
3) Exit.
Your selection: """

menuPrompt = """\n--- Secret Permission App ---

Please choose one of these options:

1) Vote for Permissions.
2) Vote for the decision.
3) add a decision.
4) See all employees.
5) See all decisions.
6) Exit.
Your selection: """

def login():
    global namel 

    name = input("Name: ").strip()
    password = input("Password: ").strip()
    login = db.check_login(name)

    if login is None or str(login[1]) != password:
        print("\nInvalid input, please try again!")
        return False
    else:    
        namel = name
        return True


def register():
    name = input("Name: ").strip()
    password = input("Password: ").strip()
    db.insert_emp(name,password)


def vote_permissions():
    coolDown = db.check_cooldown(namel,"perm")
    if coolDown:
        employees = [employee[0] for employee in db.get_all_emps() if employee[0] != namel]
        empDict = {str(count):name for count,name in enumerate(employees,start=1)}
        while empCount:=len(empDict):
            print(empDict)
            # can do some upgrades here
            empChoice = input("Your choice: ")
            if empChoice in empDict.keys():
                name = empDict[empChoice]
                db.update_emp_tpoint(name,empCount,False)
                del empDict[empChoice]
            
        db.update_emp_tpoint(namel,None,True)
        #  print("ı am done")
    else:
        print("You already vote for permissions!")


def vote_decision():
    coolDown = db.check_cooldown(namel,"dec")
    if coolDown is True:
        currentDec = db.check_current_dec(namel)
        if currentDec:
            print(f"Current decision is: {currentDec}")
            while vote:=input("1 => Accept \n2 => Refuse \nYour selection: ").strip():
                if vote in ("1","2"):
                    db.update_dec_assentState(namel,currentDec,vote)
                    break
                else:
                    print("\nInvalid input, please try again!")
        else:
            print("There is no current decision!")
    elif coolDown:
        print("You should firstly finish the voting for permissions section!")
    else:
        print("You already vote for the decision!")
                
       

def add_decision():
    name = input("Decision's name: ")
    db.insert_dec(name,namel)


def show_employees():
    print("-------------------------")
    employees = db.get_all_emps()
    for employee in employees:
        print(employee[0], employee[2])
    print("-------------------------")
    input("Press enter to continue: ")


def show_decisions():
    print("-------------------------")
    decisions = db.get_all_decs()
    for decision in decisions:
        print(f"{decision[1]} by {decision[2]}: {decision[3]}")
    print("-------------------------")
    input("Press enter to continue: ")
menu()