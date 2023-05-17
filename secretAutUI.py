from secretAutDB import Database
import sys

db = Database()

accountPrompt = """\n--- Secret_Authorization_System ---

Please choose one of these options:
1) Login.
2) Register.
3) Exit.
Your selection: """

menuPrompt = """\n--- Secret_Authorization_System ---

Please choose one of these options:
1) Vote for authorization.
2) Vote for the decision.
3) Add a decision.
4) See all employees.
5) See all decisions.
6) Exit.
Your selection: """

def menu():
    while True:
        userInput = input(accountPrompt)
        if userInput == "1":
            if login():
                break
        elif userInput == "2":
            register()
        elif userInput == "3":
            exit()
        else:
            print("\nInvalid input, please try again!")

    while True:
        userInput = input(menuPrompt)
        if userInput == "1":
            vote_authorization()
        elif userInput == "2":
            vote_decision()
        elif userInput == "3":
            add_decision()
        elif userInput == "4":
            show_employees()
        elif userInput == "5":
            show_decisions()
        elif userInput == "6":
            exit()
        else:
            print("\nInvalid input, please try again!")

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
    db.insert_emp(name, password)

def vote_authorization():
    coolDown = db.check_cooldown(namel, "perm")
    if coolDown:
        employees = [employee[0] for employee in db.get_all_emps() if employee[0] != namel]
        empDict = {str(count): name for count, name in enumerate(employees, start=1)}
        while empDict:
            print(empDict)
            empChoice = input("Your choice: ")
            if empChoice in empDict:
                name = empDict[empChoice]
                db.update_emp_tpoint(name, len(empDict), False)
                del empDict[empChoice]
        db.update_emp_tpoint(namel, None, True)
    else:
        print("You already voted for authorization!")

def vote_decision():
    coolDown = db.check_cooldown(namel, "dec")
    if coolDown is True:
        currentDec = db.check_current_dec(namel)
        if currentDec:
            print(f"Current decision is: {currentDec}")
            while True:
                vote = input("1 => Accept\n2 => Refuse\nYour selection: ").strip()
                if vote in ("1", "2"):
                    db.update_dec_assentState(namel, currentDec, vote)
                    break
                else:
                    print("\nInvalid input, please try again!")
        else:
            print("There is no current decision!")
    elif coolDown:
        print("You should first finish voting for authorization!")
    else:
        print("You already voted for the decision!")

def add_decision():
    name = input("Decision's name: ")
    db.insert_dec(name, namel)

def show_employees():
    print("-------------------------")
    employees = db.get_all_emps()
    for employee in employees:
        print(f"Name: {employee[0]}, Password: {employee[1]}")
    print("-------------------------")

def show_decisions():
    print("-------------------------")
    decisions = db.get_all_decs()
    for decision in decisions:
        print(f"Decision: {decision[1]}, Creator: {decision[2]}, Assent: {decision[3]}")
    print("-------------------------")

def exit():
    print("Exiting the application...")
    sys.exit()

if __name__ == "__main__":
    menu()