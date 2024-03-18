import re
from MaturityAppOps.maturityappops import MaturityAppOps


class MaturityOptions:
    def __init__(self) -> None:
        self.questionratings = ["Foundation","Basic","Marginal","Credible","Optimal"]
        self.cat_pattern = r'[A-Z][A-Z]\.[A-Z][A-Z]'
        self.sub_pattern = r'[A-Z][A-Z]\.[A-Z][A-Z]\-[0-9]'
        self.maturityops = MaturityAppOps("http://127.0.0.1:8080")
        self.maturity_assessment_data = {"maturityassessment":"Nist Company Name Assessment","function":"ID","category":"ID.FF","subcategory":"ID.FF-1","grade":2, 
                                                                "questionrating":"Basic","questions":"Is there a backup policy?",
                                                               "evidence":"The CTO said this"}
    def pick_action(self):
        action_picked = False
        while not action_picked:
            print("Sample Data:",{
                "maturityassessment": "Nist Company Name Assessment",
                "function": "ID",
                "category": "ID.AM",
                "subcategory": "ID.AM-1",
                "grade": 3,
                "questionrating": "Credible",
                "questions": "Is there asset management support?",
                "evidence": "The technical engineer said this."
            })
            print()
            action_option = input("Pick action option:\n(1) store new maturity assessment\n(2) get maturity assessment data\n(3) update existing maturity assessment.\n(4) get all existing from field.\n(5) Delete question.\n(6) try sample.\n(q) quit\n")
            if action_option == "q":
                exit()
            if action_option == "1" or action_option == "2" or action_option == "3" or action_option == "4" or action_option == "5" or action_option == "6":
                action_picked = True
        return action_option
    def store_data(self):
        maturity_assessment_picked = False
        return_to_main_menu = False
        print("POST - Storing Maturity Assessments")
        while not maturity_assessment_picked:
            maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment ")
            # Validation of correct data format
            function = input("What NIST control framework function to input? (max 2 chars): e.g ID: or return to menu (q)")
            if function == "q":
                return True

            if len(function) > 2: # Has to be in form ID
                continue
            category = input("What NIST control framework category to input? (max 5 chars) e.g ID.AM: or return to menu (q)")
            if category == "q":
                return True
            if len(category) > 5 or not re.search(self.cat_pattern, category): # Has to be in form ID.AM
                continue
            subcategory = input("What NIST control framework subcategory to input? (max 7 chars) e.g ID.AM-1: or return to menu (q)")
            if subcategory == "q":
                return True
            if len(category) > 7 or not re.search(self.sub_pattern, subcategory): # Has to be in form ID.AM-1
                continue
            grade = input("What NIST control framework grade to input? (0-5) or return to menu (q)") # Has to be between 0-5
            if grade == "q":
                return True
            if not grade.isdigit():
                continue
            else:
                grade = int(grade)
                if grade < 0 or grade> 5:
                    continue
            questionrating = input(f"What NIST control framework question rating to input? {str(self.questionratings)} or return to menu (q)")
            if questionrating == "q":
                return True
            if questionrating.lower() not in [x.lower() for x in self.questionratings]: # Has to be one of these values ["Foundation","Basic","Marginal","Credible","Optimal"]
                continue
            question = input(f"What NIST control framework question to input? or return to menu (q)")
            if question == "q":
                return True
            evidence = input(f"What NIST control framework evidence to input? or return to menu (q)")
            if evidence == "q":
                return True
            maturity_assessment_picked = True

        self.maturityops.store_question({"maturityassessment":maturity_assessment,"function":function,"category":category,"subcategory":subcategory,"grade":grade, 
                                                                    "questionrating":questionrating,"questions":question,
                                                                "evidence":evidence})
        return return_to_main_menu
    def get_data(self):
        return_to_main_menu = False
        print("GET- Querying Maturity Assessments")
        maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment or return to menu (q)")
        if maturity_assessment == "q":
            return True
        field = input(f"What field do you want to retrieve or return to menu (q) ?\ne.g {list(self.maturity_assessment_data.keys())}")
        if field == "q":
            return True
        if field == "maturityassessment":
            value = maturity_assessment
        else:
            value = input(f"What is the maturity assesment data you want to query?\ne.g {list(self.maturity_assessment_data.values())}\n")
        self.maturityops.get_question(maturity_assessment,{field:value})
        return return_to_main_menu
    
    def update_data(self):
        return_to_main_menu = False
        print("UPDATE - Querying Maturity Assessments")

        maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment or return to menu (q)")
        if maturity_assessment == "q":
            return True
        field = input(f"What field do you want to change? or return to menu (q) \ne.g {list(self.maturity_assessment_data.keys())}")
        if field == "q":
            return True
        oldvalue = input(f"What is the old value you want to change? or return to menu (q)\ne.g {list(self.maturity_assessment_data.values())}\n") # getting old value to change
        if oldvalue == "q":
            return True
        newvalue = input(f"What is the new value you want to change? or return to menu (q) \n")
        if newvalue == "q":
            return True
        self.maturityops.update_question(maturity_assessment,field,oldvalue,newvalue)
        return return_to_main_menu
    def delete_question(self):
        return_to_main_menu = False
        print("DELETE - Querying Maturity Assessment Question.")
        maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment or return to menu (q)")
        if maturity_assessment == "q":
            return True
        maturity_assessment_question = input("What is the question you would like to delete?e.g Nist Company Name Assessment or return to menu (q)")
        if maturity_assessment_question == "q":
            return True
        self.maturityops.delete_question(maturity_assessment,maturity_assessment_question)
        return return_to_main_menu

    def get_all(self):
        return_to_main_menu = False
        maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment or return to menu (q)")
        if maturity_assessment == "q":
            return True
        maturity_assessment_data= list(self.maturity_assessment_data.keys())
        maturity_assessment_data[-2] = maturity_assessment_data[-2][:-1]
        field = input(f"What is the maturity assesment field you want to query? or return to menu (q) \ne.g {maturity_assessment_data}\n")
        if field == "q":
            return True
        self.maturityops.getallexisting(maturity_assessment,field)
        return return_to_main_menu
    def try_sample(self):
        print("POST - Storing Maturity Assessments")
        maturityassessment = "Nist Company Name Assessment"
        self.maturityops.store_question(self.maturity_assessment_data)
        print("GET- Querying Maturity Assessments")
        self.maturityops.get_question(maturityassessment,{"subcategory":"ID.FF-1"})
        print("UPDATE - Querying Maturity Assessments")
        self.maturityops.update_question(maturityassessment,"subcategory","ID.FF-1","GV.FF-1")
        print("GET- Querying Maturity Assessments")
        self.maturityops.get_question(maturityassessment,{"subcategory":"GV.FF-1"})