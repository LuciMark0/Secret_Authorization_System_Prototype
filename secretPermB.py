import sqlite3

createEmployeesTable = """CREATE TABLE IF NOT EXISTS employees 
(name TEXT PRIMARY KEY, password INTEGER, reputation INTEGER, dcheck INTEGER);"""

createDecisionsTable = """CREATE TABLE IF NOT EXISTS decisions 
(id INTEGER PRIMARY KEY, decisionSum TEXT UNIQUE, whoAdvised TEXT, assentState INTEGER, voteCheck INTEGER);"""

insertEmployees = "INSERT OR IGNORE INTO employees (name, password, reputation, dcheck) VALUES (?, ?, 0, 0);"

insertDecisions = "INSERT OR IGNORE INTO decisions (decisionSum, whoAdvised, assentState, voteCheck) VALUES (?, ?, 0, 0);"

AllEmployees = "SELECT * FROM employees;"

AllDecisions = "SELECT * FROM decisions WHERE voteCheck = 1;"

checkForLogin = "SELECT * FROM employees WHERE name = ?;"

updateTPoint = "UPDATE employees SET reputation = reputation + ? WHERE name = ?;"

# ----------------------- decision vote part
currentDec = "SELECT decisionSum FROM decisions WHERE voteCheck = 0 ORDER BY id ASC LIMIT 1;"

checkDecCooldown = "SELECT dcheck FROM employees WHERE name = ?;"

updateDcheckCooldown = "UPDATE employees SET dcheck = ? WHERE name = ?;"

updateDecVoteF = """
UPDATE decisions 
SET assentState = assentState"""
updateDecVoteL ="""
(SELECT reputation FROM employees WHERE name = ?)
WHERE decisionSum = ?;"""

checkVoteEnd = "Select name From employees WHERE dcheck = 1 OR dcheck = 0"

updateDecVoteCheck = "UPDATE decisions SET voteCheck = 1 WHERE decisionSum = ?"

setDecAsState = """UPDATE decisions 
SET assentState = (CASE WHEN assentState > 0 THEN 'Accepted' ELSE 'Refused' END) 
WHERE decisionSum = ? """

updateEmpsDchecks = "UPDATE employees SET dcheck = dcheck - 1"
#-------------------- End

deleteEmp = "DELETE FROM employees WHERE name = ?;"

deleteDec = "DELETE FROM decisions WHERE decisionSum = ?;"
class Database:
    def __init__(self) -> None:
        self.con = sqlite3.connect("secretPerm.db")
        self.cur = self.con.cursor()
        self.create_tables()


    def create_tables(self):
        self.cur.execute(createEmployeesTable)
        self.cur.execute(createDecisionsTable)
    

    def insert_emp(self, namel, password):
        self.cur.execute(insertEmployees, (namel, password))
        self.con.commit()

    
    def insert_dec(self,decSum,namel):
        self.cur.execute(insertDecisions, (decSum,namel))
        self.con.commit()


    def get_all_emps(self):
        return self.cur.execute(AllEmployees).fetchall()

    
    def get_all_decs(self):
        return self.cur.execute(AllDecisions).fetchall()
    

    def check_login(self,namel):
        return self.cur.execute(checkForLogin, (namel,)).fetchone()
    

    def check_cooldown(self,namel,checkfor):
        dcheck = self.cur.execute(checkDecCooldown, (namel,)).fetchone()[0]
        if checkfor == "perm":
            return True if dcheck == 0 else False
        elif checkfor == "dec":
            return True if dcheck == 1 else False if dcheck == 2 else "exception"


    def update_emp_tpoint(self,name,order,finished):
        if not finished:
            self.cur.execute(updateTPoint, (order,name))
        else:
            self.cur.execute(updateDcheckCooldown, (1,name))
            self.con.commit()
    

    def update_emp_dcheks(self):
        self.cur.execute(updateEmpsDchecks)
        self.con.commit()
            
    
    #----------------------  decision vote part
    def check_current_dec(self,namel):
        curndec = self.cur.execute(currentDec).fetchone()
        if not curndec is None:
            self.cur.execute(updateDcheckCooldown, (2,namel))
            self.con.commit()
            return curndec[0]
        else:
            return False
    

    def update_dec_assentState(self,empName,decName,vote):
        if vote == "1":
            vote = " + "
            updateDecVote = updateDecVoteF + vote + updateDecVoteL
        else:
            vote = " - "
            updateDecVote = updateDecVoteF + vote + updateDecVoteL
        self.cur.execute(updateDecVote, (empName,decName))
        self.con.commit()
        
        voteEnd = self.cur.execute(checkVoteEnd).fetchall()
        if not voteEnd:
            self.cur.execute(updateDecVoteCheck, (decName,))
            self.cur.execute(setDecAsState, (decName,))
            self.con.commit()
            self.update_emp_dcheks()
    #-------------------- End
    
    
    def delete_emp(self,name):
        self.cur.execute(deleteEmp, (name,))
        self.con.commit()
    

    def delete_dec(self,name):
        self.cur.execute(deleteDec, (name,))
        self.con.commit()
