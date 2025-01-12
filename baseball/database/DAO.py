from database.DB_connect import DBConnect
from model.team import Team

class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT `year` 
                       FROM teams t 
                       WHERE `year` >= 1985
                       ORDER BY `year` DESC """

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                    FROM teams t 
                    WHERE t.`year` = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeams(year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.teamCode, t.ID, sum(s.salary) as totSalary
                    FROM salaries s, teams t, appearances a
                    WHERE s.`year`=t.`year` and t.`year`=a.`year` and a.`year`= %s 
                    and t.ID = a.teamID and a.playerID = s.playerID
                    GROUP BY t.teamCode"""

        cursor.execute(query, (year,))

        result ={}
        for row in cursor:
            #result.append((idMap[row["ID"]], [row["totSalary"]]))
            ##senza dizionario, ma ci conviene usarlo
            result[idMap[row["ID"]]] = row["totSalary"]
            #come chiave metto l'oggetto e come valore il salario

        cursor.close()
        conn.close()
        return result

