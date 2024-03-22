import base64
from typing import Union
from MaturitySQLDB.Maturitysql import MaturitySQL
class MaturityCRUD:
    def __init__(self) -> None:
        self.Maturitysql = MaturitySQL()
    def remove_last_occurrence(self,original_string, word_to_remove):
        # This is a problem when creating the SQL string a final AND would still be there causing a syntax error. This removes the last AND
        split_string = original_string.rsplit(word_to_remove, 1)
        if len(split_string) > 1:
            new_string = ''.join(split_string)
            return new_string
        else:
            return original_string
    # Creates tables
    def create_table(self,primary_key:str,fields:tuple,types :tuple,table: str):
        if type(fields) == tuple: # If several fields were provided put it into SQL format 
            fieldlist = [f"{field} {typestr}"for field,typestr in zip(fields,types)]
            fieldstr = ', '.join(fieldlist)
            result = self.Maturitysql.run_command(f"CREATE TABLE IF NOT EXISTS {table} ({primary_key} int NOT NULL AUTO_INCREMENT,{fieldstr}, PRIMARY KEY ({primary_key}) );",self.Maturitysql.fetch)
            if result == ():
                return {"message":f"{table} table was created."}
            else:
                return {"error":f"error table was not created.","error":result}
        else:
            fieldstr = f"{fields} {types}"
            result = self.Maturitysql.run_command(f"CREATE TABLE IF NOT EXISTS {table} ({primary_key} int NOT NULL AUTO_INCREMENT,{fieldstr}, PRIMARY KEY ({primary_key}) );",self.Maturitysql.fetch)
            if result == ():
                return {"message":f"{table} table was created."}
    def base64_to_hex(self,value):
        value = value.encode()
        value = base64.decodebytes(value).hex()
        return value
    

    def post_data(self,fields:tuple,values:tuple,table:str):
            

            valuestr= str(tuple("%s" for i in values)).replace("'","",100) # Turns field tuple into SQL string command format
            fieldstr = str(tuple(i for i in fields)).replace("'","",100) # Turns value tuple into SQL string command format
            
            if len(fields) == 1:
                fieldstr = fieldstr.replace(",","",100)
                valuestr = valuestr.replace(",","",100)
            #print(f"INSERT INTO {table} {fieldstr} VALUES {valuestr};")

            #values = tuple(map(convert_to_hex,values))

            result = self.Maturitysql.run_command(f"INSERT INTO {table} {fieldstr} VALUES {valuestr};",self.Maturitysql.fetch,datatuple=values)
            if result == ():
                return True
            else:
                return False


    def tuple_to_json(self,fields:tuple,result:tuple):
        # Turns the tuples returned into json.
        if type(result[0]) == tuple:
            final_result = []
            for entry in result:
                entrydict = dict(zip(fields,entry))
                final_result.append(entrydict)
            return final_result
        elif type(result[0]) == str:
            final_result = dict(zip(fields,result))
            return final_result 
        
    def json_to_tuple(self,json:dict):
        keys = tuple(json.keys())
        values = tuple(json.values())
        return keys,values


    
    def get_data(self,fields:tuple,table:str,condition=None,getamount:int=1000):
    
        if len(fields) != 1:
            fieldlist = [f"{field}" for field in fields] 
            fieldstr = ', '.join(fieldlist) # Turns tuple into SQL command format.
        else:
            fieldstr = fields[0]
        
            #fieldstr = fieldstr.replace(", ","",100)
        if condition:
            #print(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            result = self.Maturitysql.run_command(f"""SELECT {fieldstr} FROM {table} WHERE {condition} LIMIT {str(getamount)};""",self.Maturitysql.fetch)
            if result == ():
                return False
            elif result != () and type(result) == tuple:
                result = self.tuple_to_json(fields,result)
                return result
            else:
                return {"error":"error syntax error.","error":result}
        else:
            result = self.Maturitysql.run_command(f"""SELECT {fieldstr} FROM {table} LIMIT {str(getamount)};""",self.Maturitysql.fetch)
            if result == ():
                return False
            elif result != () and type(result) == tuple:
                result = self.tuple_to_json(fields,result)
                return result
            else:
                return {"error":"error syntax error.","error":result}
    def hex_to_base64(self,hex_file:bytes): # x0 unicode-like hex
        return  base64.b64encode(bytes.fromhex(hex_file.hex())).decode()
    def get_large_data(self,fields:tuple,table:str,condition=None):
        # Gets data as a generator to be memory efficienct for fetching of large amounts of data.
        if len(fields) != 1:
            fieldlist = [f"{field}" for field in fields]
            fieldstr = ', '.join(fieldlist) 
        else:
            fieldstr = fields[0]
        
            #fieldstr = fieldstr.replace(", ","",100)
        if condition:
            #print(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            result = self.Maturitysql.run_command_generator(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            return result
        else:
            result = self.Maturitysql.run_command_generator(f"""SELECT {fieldstr} FROM {table};""")
            return result
    def get_join_question_data(self,fields:tuple,condition=Union[dict,None]):
        # Gets data by joining SQL tables.
        # The main tables follow a pattern of having an 's' as the last letter. So when a field is selected the table and field can be matched easily for the table join.
            if len(fields) != 1:
                fieldlist = [f"{field}" for field in fields]
                fieldstr = ', '.join(fieldlist) 
            else:
                fieldstr = fields[0]

            
            if condition:
                condfields = tuple(condition.keys())
                fieldvalues = tuple(condition.values())
                conditionres = ""
                for ind in range(len(condfields)):
                    if condfields[ind] == "author_email": # Deals with anomaly fields that don't end with 's'
                        condstr = f"maturityassessments.{condfields[ind]} = '{fieldvalues[ind]}' AND "
                    elif condfields[ind] == "grade": # Deals with anomaly fields that don't end with 's'
                        condstr = f"subcategorys.{condfields[ind]} = '{fieldvalues[ind]}' AND "
                    elif condfields[ind] == "question" or condfields[ind] == "evidenceforservice": # Deals with anomaly fields that don't end with 's'
                        condstr = f"questions.{condfields[ind]} = '{fieldvalues[ind]}' AND "
                        
                    else:
                        if type(condfields[ind]) == int:
                            condstr = f"{condfields[ind]}s.{condfields[ind]} = {fieldvalues[ind]} AND " # Deals with integer values
                        else:
                            condstr = f"{condfields[ind]}s.{condfields[ind]} = '{fieldvalues[ind]}' AND " # Deals with string values.
                    conditionres += condstr
                condition_result = self.remove_last_occurrence(conditionres,"AND") + ";"
                result = self.Maturitysql.run_command(
                        f"""
                        SELECT {fieldstr} FROM questions
                        INNER JOIN questionratings ON questions.questionrating = questionratings.questionrating
                        INNER JOIN subcategorys ON questionratings.subcategory = subcategorys.subcategory
                        INNER JOIN categorys ON subcategorys.category = categorys.category
                        INNER JOIN functions ON categorys.function = functions.function
                        INNER JOIN maturityassessments ON functions.maturityassessment = maturityassessments.maturityassessment
                        WHERE {condition_result};
                        
                        """,self.Maturitysql.fetch)
            else:
               result = self.Maturitysql.run_command(
                        f"""
                        SELECT {fieldstr} FROM questions
                        JOIN questionratings ON questions.questionrating = questionratings.questionrating
                        JOIN subcategorys ON questionratings.subcategory = subcategorys.subcategory
                        JOIN categorys ON subcategorys.category = categorys.category
                        JOIN functions ON categorys.function = functions.function
                        JOIN maturityassessments ON functions.maturityassessment = maturityassessments.maturityassessment;
                        
                        """,self.Maturitysql.fetch)
            if result == ():
                return False
            elif result != () and type(result) == tuple:
                result = self.tuple_to_json(fields,result)
                return result
            else:
                return {"error":"error syntax error.","error":result}
    
    def update_maturityinfo(self,data:dict):
        if not data.get("oldmaturityassessment"):
            del data["maturityassessment"]
        hierarchy_order = ["maturityassessments","functions","categorys","subcategorys","questionratings","questions"]
        fieldname = list(filter(lambda x: "old" not in x, list(data.keys())))[0] # to differentiate the old data and new data to input dynamically. old is added to the front of the field. This checks if it exists and gets the name.
        column_name = fieldname + "s"
        old_value  = data["old" + fieldname]
        new_value = data[fieldname]
        is_removing_question = False
        try:
            next_column_name = hierarchy_order[hierarchy_order.index(column_name) +1] # When updated in one table, the other table also needs to be updated too.
        except IndexError as ex:
            is_removing_question = True
            pass
        if not is_removing_question:
            sql_command = f"""
                UPDATE questions
                INNER JOIN questionratings ON questions.questionrating = questionratings.questionrating
                INNER JOIN subcategorys ON questionratings.subcategory = subcategorys.subcategory
                INNER JOIN categorys ON subcategorys.category = categorys.category
                INNER JOIN functions ON categorys.function = functions.function
                INNER JOIN maturityassessments ON functions.maturityassessment = maturityassessments.maturityassessment
                SET {column_name}.{fieldname}  = '{new_value}',
                    {next_column_name}.{fieldname} = '{new_value}'
                WHERE {column_name}.{fieldname} = '{old_value}';"""
        else:
            sql_command = f"UPDATE {column_name} SET {fieldname} = '{data['question']}' WHERE {fieldname} = '{old_value}';"
        #print(sql_command)
        
        res = self.Maturitysql.run_command(sql_command,self.Maturitysql.fetch)
        return res
    def delete_maturityinfo(self,params :dict):
        if len(list(params.keys())) > 1:
            del params["maturityassessment"]
        fieldname = list(params.keys())[0]
        column_name =  fieldname  + "s"
        value = params[fieldname]
        res = self.Maturitysql.run_command(f"""DELETE {column_name} FROM questions
                INNER JOIN questionratings ON questions.questionrating = questionratings.questionrating
                INNER JOIN subcategorys ON questionratings.subcategory = subcategorys.subcategory
                INNER JOIN categorys ON subcategorys.category = categorys.category
                INNER JOIN functions ON categorys.function = functions.function
                INNER JOIN maturityassessments ON functions.maturityassessment = maturityassessments.maturityassessment
                WHERE {column_name}.{fieldname} = '{value}';""",self.Maturitysql.fetch)
        return res
    
    def update_data(self,fieldstoupdate:tuple,values:tuple,table=str,condition=str):
        if len(fieldstoupdate) > 1:
            updatelist = []
            for field,value in zip(fieldstoupdate,values):
                if type(value) != str:
                    fieldstr = f"{field} = {value}" # Creates the SQL Command for integer values
                    updatelist.append(fieldstr)

                else:
                    fieldstr = f"{field} = '{value}'" # Creates the SQL Command for string values
                    updatelist.append(fieldstr)
            updatestr = ', '.join(updatelist) # Turns into SQL command.
            result = self.Maturitysql.run_command(f"UPDATE {table} SET {updatestr} WHERE {condition};",self.Maturitysql.fetch)
            if result == ():
                return True
            else:
                return False
        else:          
            if type(values[0]) != str:
                updatestr = f"{fieldstoupdate[0]} = {values[0]}"
            else:
                updatestr = f"{fieldstoupdate[0]} = '{values[0]}'"
            result = self.Maturitysql.run_command(f"UPDATE {table} SET {updatestr} WHERE {condition};",self.Maturitysql.fetch)
            if result == ():
                return True
            else:
                return False

    def update_blob(self,fieldstoupdate:str,value:str,table=str,condition=str):
        updatestr = "UPDATE %s SET %s = x'%s' WHERE %s;" % (table,fieldstoupdate,self.base64_to_hex(value),condition) # update blob data.
        result = self.Maturitysql.run_command(updatestr,self.Maturitysql.fetch)
        if result == ():
            return True
        else:
            return False
    def delete_data(self,table:str,condition:str):
        result = self.Maturitysql.run_command(f"DELETE FROM {table} WHERE {condition};",self.Maturitysql.fetch) # Deletes data
        if result == ():
            return True
        else:
            return False
        
    def check_exists(self,fields:tuple,table:str,condition=None):
        # checks if data exists in tables.
        if len(fields) != 1:
            fieldlist = [f"{field}" for field in fields]
            fieldstr = ', '.join(fieldlist) 
        else:
            fieldstr = fields[0]
        
            #fieldstr = fieldstr.replace(", ","",100)
        if condition:
            #print(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""")
            result = self.Maturitysql.run_command(f"""SELECT {fieldstr} FROM {table} WHERE {condition};""",self.Maturitysql.check_exists)
            if result == True or result == False:
                return result
            else:
                return {"message":"syntax error or table doesn't exist.","error":result}
                
        else:
            result = self.Maturitysql.run_command(f"""SELECT {fieldstr} FROM {table};""",self.Maturitysql.check_exists)
            if result == True or result == False:
                return result
            else:
                return {"message":"syntax error or table doesn't exist.","error":result}

    
