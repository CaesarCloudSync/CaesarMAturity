from Maturitysql import MaturitySQL
import pymysql

if __name__ == "__main__":
    Maturitysql = MaturitySQL()
    Maturitysql.run_command(filename="mysqlsampledatabase.sql")