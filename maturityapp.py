import requests
uri = "http://127.0.0.1:8080"

email = "amari.sql@gmail.com" #input("What is your email?")
password = "kya63amari" # input("What is your password?")
login_option = "signup"
interact_option = "store"

maturity_assessment_data = [{"maturityassessment":"Nist Company Name Assessment","function":"ID","category":"ID.AM","subcategory":"ID.AM-1","grade":3, 
                                                        "questionrating":"Credible","questions":"Is there asset management support?",
                                                        "evidence":"The technical engineer said this."},
                            {"maturityassessment":"Nist Company Name Assessment","function":"GV","category":"GV.CE","subcategory":"GV.CV-1","grade":2, 
                                                                "questionrating":"Basic","questions":"Is there a backup policy?",
                                                                "evidence":"The CTO said this"}]

if login_option == "login":
    responselogin = requests.post(f"{uri}/loginapi",json={"email":email,"password":password})
    access_token = responselogin.json()["access_token"]
elif login_option == "signup":
    responselogin = requests.post(f"{uri}/signupapi",json={"email":email,"password":password})
    access_token = responselogin.json().get("access_token")
    if not access_token:
        responselogin = requests.post(f"{uri}/loginapi",json={"email":email,"password":password})
        access_token = responselogin.json()["access_token"]

headers = {"Authorization": f"Bearer {access_token}"}
if interact_option == "store":
    for maturity_assessment in maturity_assessment_data:
        response = requests.post(f"{uri}/storequestion",json=maturity_assessment ,headers=headers)
        if response.json().get("message"):
            print(response.json().get("message"))
        else:
            print(response.json().get("error"))

elif interact_option == "get":
    response = requests.get(f"{uri}/getquestions",params={"maturityassessment":"Nist Company Name Assessment","maturityassessment":"Nist Company Name Assessment"},headers=headers)
    if response.json().get("error"):
        print(response.json().get("error"))
    else:
        print(response.json())


elif interact_option == "update":
    response = requests.put(f"{uri}/updatequestion",json={"maturityassessment":"Nist Company Name Assessment","category":"GV.CE","oldcategory":"PR.IR"},headers=headers)
    if response.json().get("message"):
        print(response.json().get("message"))
    else:
        print(response.json())

