from Maturitysql import MaturitySQL
import pandas as pd
import os
import shutil

def insert_data():
# Insert Data into Table resume
    for ind,candidate in enumerate(names):
        data_exists = Maturitysql.run_command(f"SELECT name FROM {table} WHERE name LIKE '{candidate}'",Maturitysql.check_exists)
        if not data_exists:
            amarilogo = Maturitysql.convert_to_blob(f"Logos/{logos[ind]}")
            amaricv = Maturitysql.convert_to_blob(f"Humans/{humans[ind]}")
            resumetuple = (candidate,amarilogo,amaricv)
            Maturitysql.run_command(f"INSERT INTO {table} (name,photo,resume) VALUES (%s,%s,%s)",datatuple=resumetuple)
            print("resume inserted.")
if __name__ == "__main__":
   #allnames = pd.read_csv("brazilian-names.csv")
   names = ['Issa', 'Midas', 'Adalvina', 'Euquenor', 'Celimena', 'Poguira', 'Munir', 'Corina', 'Vismara', 'Tristão', 'Baraúna', 'Pandora', 'Náiade', 'Salatiel', 'Jênie', 'Pasini', 'Acalântis', 'Platâo', 'Xanthe', 'Bretãs', 'Branka', 'Marina', 'Moke', 'Natacha', 'Saladino', 'Silvana', 'Libânia', 'Fedro', 'Tito', 'Bosco', 'Barac', 'Abdera', 'Daltivo', 'Elvira', 'Iodâmia', 'Jacina', 'Carmem', 'Osni', 'Metanira', 'Afrodísio', 'Lindoia', 'Abner', 'Samir', 'Ramão', 'Agabo', 'Norina', 'Inandê', 'Zebilon', 'Solveig', 'Telêmaco', 'Fauno', 'Aranha', 'Holda', 'Alan', 'Marisa', 'Apolínio', 'Alexandre', 'Keike', 'Haskel', 'Cinara', 'Sátiro', 'Vincent', 'Epicasta', 'Odélio', 'Karolina', 'Alex', 'Wolf', 'Arthur', 'Dona', 'Faros', 'Santoro', 'Nery', 'Fernandes', 'Partênope', 'Faetonte', 'Caron', 'Angerona', 'Fenaio', 'Mandi', 'Amapola', 'Kauê', 'Seth', 'Dimitre', 'Astêmio', 'Ira', 'Kanela', 'Onã', 'Almirante', 'Carol', 'Cezar', 'Adina', 'Beoto', 'Ida', 'Tecobiara', 'Urbano', 'Aritana', 'Solange', 'Górki', 'Apolline', 'Oberon']
   logos = os.listdir("Logos")
   humans = os.listdir("Humans")[:100]
   db = "resumebase"
   table = "resumes"
   Maturitysql = MaturitySQL()
   # Create Database
   db_exists = Maturitysql.run_command(f"SHOW DATABASES LIKE '{db}';",Maturitysql.check_exists)
   if not db_exists:
    Maturitysql.run_command(f"CREATE DATABASE {db};")
   Maturitysql.run_command(f"USE {db};")
# Create Table resume
   table_exists = Maturitysql.run_command(f"SHOW TABLES LIKE '{table}';",Maturitysql.check_exists)
   if not table_exists:
    Maturitysql.run_command(f"CREATE TABLE {table} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), photo BLOB,resume MEDIUMBLOB)")

      

   candidate = "Amari Lawal Again"
   newcandidate = "Amari Lawal"
   data_exists = Maturitysql.run_command(f"SELECT name FROM {table} WHERE name LIKE '{newcandidate}'",Maturitysql.check_exists)
   if data_exists:
      result = Maturitysql.run_command(f"SELECT name from {table} WHERE name LIKE '{newcandidate}'",Maturitysql.fetch)
      print(result)
      #Maturitysql.run_command(f"UPDATE {table} SET name='{newcandidate}' WHERE name LIKE '{candidate}'")
      #print("table update.")
