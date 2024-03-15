import os
import base64
import requests
from MaturitySQLDB.maturitycrud import MaturityCRUD
from MaturitySQLDB.maturity_create_tables import MaturityCreateTables
class SQLOps:
    def __init__(self,Maturitycrud : MaturityCRUD,Maturitycreatetables : MaturityCreateTables) -> None:
        self.Maturitycrud = Maturitycrud
        self.Maturitycreatetables = Maturitycreatetables
    def validate_store_request(self,data):
        maturityassessment = data["maturityassessment"]
        function = data["function"]
        category = data["category"]
        subcategory = data["subcategory"]
        questionrating = data["questionrating"]
        question = data["questions"]
        evidence = data["evidence"]
        grade = data["grade"]
        return maturityassessment,function,category,subcategory,questionrating,question,evidence,grade
    def check_question_exists(self, maturityassessment,function,category ,subcategory,questionrating,question):
        mat_exists = self.Maturitycrud.check_exists(("*"),"maturityassessments",f"maturityassessment = '{maturityassessment}'")
        func_exists = self.Maturitycrud.check_exists(("*"),"functions",f"function = '{function}'")
        cat_exists = self.Maturitycrud.check_exists(("*"),"categorys",f"category = '{category}'")
        subcat_exists = self.Maturitycrud.check_exists(("*"),"subcategorys",f"subcategory = '{subcategory}'")    
        qr_exists = self.Maturitycrud.check_exists(("*"),"questionratings",f"questionrating = '{questionrating}'")
        q_exists = self.Maturitycrud.check_exists(("*"),"questions",f"question = '{question}'")
        if mat_exists and func_exists and cat_exists and subcat_exists and qr_exists and q_exists:
            return True
        else:
            return False
    def check_access(self,email,maturityassessment):
        has_access = self.Maturitycrud.check_exists(("*"),"maturityassessmentaccess",f"email = '{email}' AND maturityassessment = '{maturityassessment}'")
        if has_access:
            return True
        else:
            return False
    def store_question(self,email,maturityassessment,function,category,grade,subcategory,questionrating,question,evidence):
        maturity_assessment_exists = self.Maturitycrud.check_exists(("*"),f"maturityassessments",f"maturityassessment = '{maturityassessment}'")
        if not maturity_assessment_exists:
            mat_res = self.Maturitycrud.post_data(("author_email","maturityassessment"),(email,maturityassessment),"maturityassessments")
            acc_res = self.Maturitycrud.post_data(("email","maturityassessment"),(email,maturityassessment),"maturityassessmentaccess")
        func_res = self.Maturitycrud.post_data(("maturityassessment","function"),(maturityassessment,function),"functions")
        cat_res = self.Maturitycrud.post_data(("function","category"),(function,category),"categorys")
        subcat_res = self.Maturitycrud.post_data(("category","subcategory","grade"),(category,subcategory,grade),"subcategorys")
        qr_res = self.Maturitycrud.post_data(("subcategory","questionrating"),(subcategory,questionrating),"questionratings")

        q_res = self.Maturitycrud.post_data(("questionrating","question","evidenceforservice"),(questionrating,question,evidence),"questions")
        #acc_res = self.Maturitycrud.post_data(("email","maturityassessment"),(email,maturityassessment),"maturityassessmentaccess")
        if func_res and cat_res and subcat_res and qr_res and q_res:
            return True
        else:
            return False

        