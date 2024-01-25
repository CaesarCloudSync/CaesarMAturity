import requests
import unittest
import json
import pandas as pd

uri = "http://127.0.0.1:8080"
email = "maturity.unittest@gmail.com" #input("What is your email?")
password = "maturity" # input("What is your password?")
with open ("UnittestData/store_maturity_assessment.json") as f:
    store_mata_data  = json.load(f)
with open ("UnittestData/update_maturity_assessment.json") as f:
    update_mata_data  = json.load(f)["update_maturity_assessments"]
class MaturityAssessmentCase(unittest.TestCase):
    def login(self):
        responselogin = requests.post(f"{uri}/signupapi",json={"email":email,"password":password})
        access_token = responselogin.json().get("access_token")
        if not access_token:
            responselogin = requests.post(f"{uri}/loginapi",json={"email":email,"password":password})
            access_token = responselogin.json()["access_token"]
        print("Output:",{"access_token":access_token})
        self.assertNotEqual(access_token,None)
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers
    
    def grant_access_initial(self):
        # Normally this endpoint wouldn't exist in a production setting, this would be done manually for the first person, but for automated purposes the first ever person with access has to be automated.
        # This endpoint would normally be a security problem.
        maturity_assess_names= set(map(lambda x: x["maturityassessment"],store_mata_data["store_maturity_data"]))
        for maturity in maturity_assess_names:
            response = requests.post(f"{uri}/grantaccessinitial",json={"email":email,"maturityassessment":maturity})
            if response.json().get("message"):
                self.assertNotEqual(response.json().get("message"),None)
            else:
                self.assertEqual(response.json().get("error"),"already has access.")

    def loginfriend(self,emailfriend):
        responselogin = requests.post(f"{uri}/signupapi",json={"email":emailfriend,"password":password})
        access_token = responselogin.json().get("access_token")
        if not access_token:
            responselogin = requests.post(f"{uri}/loginapi",json={"email":emailfriend,"password":password})
            access_token = responselogin.json()["access_token"]
        print("Output:",{"access_token":access_token})
        self.assertNotEqual(access_token,None)
        headers = {"Authorization": f"Bearer {access_token}"}
        return headers

    def test_store_maturity_assessment(self):
        print("test_store_maturity_assessment")
        maturity_assessment_data = store_mata_data["store_maturity_data"]
        headers = self.login()
        self.grant_access_initial()
        for maturity_assessment in maturity_assessment_data:
            print("Input:",maturity_assessment)
            response = requests.post(f"{uri}/storequestion",json=maturity_assessment ,headers=headers)
            if response.json().get("message"):
                print("Output:",response.json().get("message"))
                self.assertNotEqual(response.json().get("message"),None)
            else:
                print("Output:",response.json().get("error"))
                self.assertEqual(response.json().get("error"),"question already exist")

    def test_get_maturity_assessment(self):
        print("test_get_maturity_assessment")
        headers = self.login()
        self.grant_access_initial()
        print("Input:","Nist Company Name Assessment")
        response = requests.get(f"{uri}/getquestions",params={"maturityassessment":"Nist Company Name Assessment"},headers=headers)
        if response.json().get("error"):
            print("Output:",response.json())
            self.assertEqual(response.json().get("error"),"maturity assessment data does not exist.")
        else:
            print("Output:",response.json())
            self.assertNotEqual(response.json().get("maturityassessments"),None)

    def test_update_maturity_assessment(self):
        print("test_update_maturity_assessment")
        headers = self.login()
        self.grant_access_initial()
        each_change = update_mata_data
        for fields in each_change:
            for fieldupdate in fields:
                print("Input:",fieldupdate)
                json_data = {"maturityassessment":"Nist Company Name Assessment"}
                json_data.update(fieldupdate)
                #print("Output:",json_data)
                response = requests.put(f"{uri}/updatequestion",json=json_data,headers=headers)
                if response.json().get("message"):
                    print("Output:",response.json().get("message"))
                    self.assertNotEqual(response.json().get("message"),None)

                else:
                    print("Output:",response.json().get("error"))
                    self.assertEqual(response.json().get("error"),None)

    def test_grant_access(self):
        print("test_grant_access")
        headers = self.login()
        self.grant_access_initial()
        emailfriend = "maturity.friend@gmail.com"
        self.loginfriend(emailfriend)
        print("Input:",{"email":emailfriend,"maturityassessment":"Nist Company Name Assessment"})
        response = requests.post(f"{uri}/grantaccess",json={"email":emailfriend,"maturityassessment":"Nist Company Name Assessment"},headers=headers)
        if response.json().get("message"):
            print("Output:",response.json().get("message"))
            self.assertNotEqual(response.json().get("message"),None)
        else:
            print("Output:",response.json().get("error"))
            self.assertEqual(response.json().get("error"),"already has access.")
    def test_remove_access(self):
        print("test_remove_access")
        headers = self.login()
        self.grant_access_initial()
        emailfriend = "maturity.friend@gmail.com"
        self.loginfriend(emailfriend)
        print("Input:",{"email":emailfriend,"maturityassessment":"Nist Company Name Assessment"})
        response = requests.delete(f"{uri}/removeaccess",params={"email":emailfriend,"maturityassessment":"Nist Company Name Assessment"},headers=headers)
        if response.json().get("message"):
            print("Output:",response.json().get("message"))
            self.assertNotEqual(response.json().get("message"),None)
        else:
            print("Output:",response.json().get("error"))
            self.assertEqual(response.json().get("error"),"never had access.")


if __name__ == "__main__":
    unittest.main()
