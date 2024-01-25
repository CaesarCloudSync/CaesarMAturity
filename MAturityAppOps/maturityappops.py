import requests
class MaturityAppOps:
    def __init__(self,uri) -> None:
        email = "maturity.unittest@gmail.com" #input("What is your email?")
        password = "maturity" # input("What is your password?")
        self.uri = uri
        self.headers = self.login(email,password)
        
    def store_question(self,maturity_assessment):
        response = requests.post(f"{self.uri}/storequestion",json=maturity_assessment ,headers=self.headers)
        if response.json().get("message"):
            print(response.json().get("message"))
        else:
            print(response.json().get("error"))
    def get_question(self,maturityassessment,maturity_data):
        # get data
        param_data = {"maturityassessment":maturityassessment}
        param_data.update(maturity_data)
        response = requests.get(f"{self.uri}/getquestions",params=param_data,headers=self.headers)
        if response.json().get("error"):
            print(response.json().get("error") + "or maturity assessment doesn't exist.")
        else:
            print(response.json())
    def getallexisting(self,maturityassessment,field):
        # get all existing data on the specified field
        param_data = {"maturityassessment":maturityassessment}
        param_data.update({"field":field})
        response = requests.get(f"{self.uri}/getallexisting",params=param_data,headers=self.headers)
        if response.json().get("error"):
            print(response.json().get("error") + "or maturity assessment doesn't exist.")
        else:
            print(response.json())
    def update_question(self,maturityassessment,field,oldvalue,newvalue):
        response = requests.put(f"{self.uri}/updatequestion",json={"maturityassessment":maturityassessment,field:newvalue,f"old{field}":oldvalue},headers=self.headers)
        if response.json().get("message"):
            print(response.json().get("message"))
        else:
            print(response.json())
    def login(self,email,password):
        responselogin = requests.post(f"{self.uri}/signupapi",json={"email":email,"password":password})
        access_token = responselogin.json().get("access_token")
        if not access_token:
            responselogin = requests.post(f"{self.uri}/loginapi",json={"email":email,"password":password})
            access_token = responselogin.json()["access_token"]
        if not access_token:
            raise Exception("Login Unsuccessful")
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers