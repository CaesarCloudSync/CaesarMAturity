import json
from MAturityAppOps.maturityappops import MaturityAppOps
maturity_assessment_data = {"maturityassessment":"Nist Company Name Assessment","function":"GV","category":"GV.CE","subcategory":"GV.CV-1","grade":2, 
                                                                "questionrating":"Basic","question":"Is there a backup policy?",
                                                               "evidence":"The CTO said this"}
                        

maturityops = MaturityAppOps("http://127.0.0.1:8080")

import re
questionratings = ["Foundation","Basic","Marginal","Credible","Optimal"]
cat_pattern = r'[A-Z][A-Z]\.[A-Z][A-Z]'
sub_pattern = r'[A-Z][A-Z]\.[A-Z][A-Z]\-[0-9]'
finished = False
while not finished:
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
        action_option = input("Pick action option:\n(1) store new maturity assessment\n(2) get maturity assessment data\n(3) update existing maturity assessment.\n(4) get all existing from field.\n(q) quit\n")
        if action_option == "q":
            exit()
        if action_option == "1" or action_option == "2" or action_option == "3" or action_option == "4":
            action_picked = True
    if action_option == "1":
        print("POST - Storing Maturity Assessments")
        maturity_assessment_picked = False
        while not maturity_assessment_picked:
            maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment ")
            # Validation of correct data format
            function = input("What NIST control framework function to input? (max 2 chars): e.g ID: ")
            if len(function) > 2: # Has to be in form ID
                continue
            category = input("What NIST control framework category to input? (max 5 chars) e.g ID.AM: ")
            if len(category) > 5 or not re.search(cat_pattern, category): # Has to be in form ID.AM
                continue
            subcategory = input("What NIST control framework subcategory to input? (max 7 chars) e.g ID.AM-1: ")
            if len(category) > 7 or not re.search(sub_pattern, subcategory): # Has to be in form ID.AM-1
                continue
            grade = input("What NIST control framework grade to input? (0-5) ") # Has to be between 0-5
            if not grade.isdigit():
                continue
            else:
                grade = int(grade)
                if grade < 0 or grade> 5:
                    continue
            questionrating = input(f"What NIST control framework question rating to input? {str(questionratings)} ")
            if questionrating.lower() not in [x.lower() for x in questionratings]: # Has to be one of these values ["Foundation","Basic","Marginal","Credible","Optimal"]
                continue
            question = input(f"What NIST control framework question to input? ")
            evidence = input(f"What NIST control framework evidence to input? ")
            maturity_assessment_picked = True

        maturityops.store_question({"maturityassessment":maturity_assessment,"function":function,"category":category,"subcategory":subcategory,"grade":grade, 
                                                                    "questionrating":questionrating,"questions":question,
                                                                "evidence":evidence})
        exit()
    if action_option == "2":
        print("GET- Querying Maturity Assessments")
        maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment ")
        field = input(f"What field do you want to retrieve?\ne.g {list(maturity_assessment_data.keys())}")
        if field == "maturityassessment":
            value = maturity_assessment
        else:
            value = input(f"What is the maturity assesment data you want to query?\ne.g {list(maturity_assessment_data.values())}\n")
        maturityops.get_question(maturity_assessment,{field:value})


    if action_option == "3":
        print("UPDATE - Querying Maturity Assessments")

        maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment ")
        field = input(f"What field do you want to change?\ne.g {list(maturity_assessment_data.keys())}")
        oldvalue = input(f"What is the old value you want to change?\ne.g {list(maturity_assessment_data.values())}\n") # getting old value to change
        newvalue = input(f"What is the new value you want to change?\n")
        maturityops.update_question(maturity_assessment,field,oldvalue,value)


    if action_option == "4":
            maturity_assessment = input("What is the maturity assesments name?e.g Nist Company Name Assessment ")
            field = input(f"What is the maturity assesment field you want to query?\ne.g {list(maturity_assessment_data.keys())}\n")
            maturityops.getallexisting(maturity_assessment,field)

