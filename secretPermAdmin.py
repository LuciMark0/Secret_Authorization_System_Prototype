from secretPermB import Database

db = Database()

def menu():
    while (adminInput:=input(adminPanel)) != "4":
            if adminInput == "1":
                reset_perm_cooldown()
            elif adminInput == "2":
                fire_emp()
            elif adminInput == "3":
                remove_dec()
            else:
                print("\nInvalid input, please try again!")

adminPanel = """\n--- Secret Permission App ---

Please choose one of these options:

1) Reset perm cooldown.
2) Delete a employee.
3) Delete a decision.
4) Exit.
Your selection: """

def reset_perm_cooldown():
    currentDec = db.check_current_dec(None)
    if not currentDec:
        db.update_emp_dcheks()
    else:
        print("There is a current decision!")


def fire_emp():
    print("-------------------------")
    employees = db.get_all_emps()
    for employee in employees:
        print(employee[0], end=", ")
    print("\n-------------------------")
    name = input("name: ").strip()
    db.delete_emp(name)


def remove_dec():
    print("-------------------------")
    decisions = db.get_all_decs()
    for decision in decisions:
        print(f"{decision[1]} by {decision[2]}: {decision[3]}")
    print("-------------------------")
    name = input("name: ").strip()
    db.delete_dec(name)

menu()