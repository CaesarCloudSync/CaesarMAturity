import requests
import unittest
import base64
from dotenv import load_dotenv
load_dotenv(".env")
from MaturitySQLDB.Maturitycrud import MaturityCRUD
from MaturitySQLDB.Maturityhash import MaturityHash
from SQLOps.sqlops import SQLOps
from MaturitySQLDB.Maturity_create_tables import MaturityCreateTables
Maturitycrud = MaturityCRUD()
Maturitycreatetables = MaturityCreateTables()
revsqlops = SQLOps(Maturitycrud,Maturitycreatetables)
uri = "http://192.168.0.11:8080"

class MaturityAssessmentCase(unittest.TestCase):
    def AssertSignup(self,response_json):
        if response_json.get("access_token"):
            return True
        if response_json.get("message"):
            return True
    def signup(self):
        response = requests.post(f"{uri}/signupapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        return self.AssertSignup(response.json())
    def test_signup(self):

        self.assertEqual(True,self.signup())
  
        #self.assertNotEqual(None,response.json().get("access_token"))
    def test_store_maturity_assesment(self):
        self.assertEqual(True,self.signup())

        response = requests.post(f"{uri}/loginapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        self.assertNotEqual(None,response.json().get("access_token"))
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{uri}/storequestions",json= {"maturityassessment":"Nist Company Name Assessment","function":"GV","category":"GV.CE","subcategory":"GV.CV-1","grade":2, 
                                                                "questionrating":"Basic","questions":["Is there a backup policy?","Is there constant monitoring"],
                                                                "evidence":["The CTO said this","There is endpoint detection"]},headers=headers)
        response = requests.post(f"{uri}/storequestions",json= {"maturityassessment":"Nist Company Name Assessment","function":"ID","category":"ID.AM","subcategory":"ID.AM-1","grade":3, 
                                                        "questionrating":"Credible","questions":["Is there asset management support?","Is there a list of assets?"],
                                                        "evidence":["The technical engineer said this.","They have a large scale database"]},headers=headers)
        self.assertEqual("question was stored",response.json().get("message"))
    def test_get_maturity_assesment(self):
        response = requests.post(f"{uri}/loginapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        self.assertNotEqual(None,response.json().get("access_token"))
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{uri}/getquestions",params={"maturityassessment":"Nist Company Name Assessment","grade":2},headers=headers)
        print(response.json())
        #
    def test_update_maturity_assesment(self):
        response = requests.post(f"{uri}/loginapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        self.assertNotEqual(None,response.json().get("access_token"))
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.put(f"{uri}/updatequestion",json={"maturityassessment":"Nist Company Name Assessment","category":"GV.CE","oldcategory":"PR.IR"},headers=headers)
        self.assertEquals("maturity data updated.",response.json().get("message"))
    def test_delete_maturity_assesment(self):
        response = requests.post(f"{uri}/loginapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        self.assertNotEqual(None,response.json().get("access_token"))
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(f"{uri}/deletematurityinfo",params={"maturityassessment":"Nist Company Name Assessment","category":"GV.CE"},headers=headers)
        self.assertEqual("maturity data deleted.",response.json().get("message"))
    def test_grant_access(self):
        response = requests.post(f"{uri}/loginapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        self.assertNotEqual(None,response.json().get("access_token"))
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        email = "amari.fbl@gmail.com"
        response = requests.post(f"{uri}/grantaccess",json={"email":email,"maturityassessment":"Nist Company Name Assessment"},headers=headers)
        self.assertEqual(f"access has been granted to {email} for this maturity assesement.",response.json().get("message"))
    def test_grant_access(self):
        response = requests.post(f"{uri}/loginapi",json={"email":"amari.sql@gmail.com","password":"kya63amari"})
        self.assertNotEqual(None,response.json().get("access_token"))
        access_token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        email = "amari.fbl@gmail.com"
        response = requests.delete(f"{uri}/removeaccess",params={"email":email,"maturityassessment":"Nist Company Name Assessment"},headers=headers)
        self.assertEqual(f"access has been remove from {email} for this maturity assesement.",response.json().get("message"))

        


if __name__ == "__main__":
    unittest.main()
