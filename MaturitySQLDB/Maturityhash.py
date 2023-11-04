import hashlib
import uuid

class MaturityHash:
    @staticmethod
    def hash_text_auth(text):
        """
            Basic hashing function for a text using random unique salt.  
        """
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt
    @staticmethod
    def hash_text(text):
        """
            Basic hashing function for a text.
        """
        return hashlib.sha256(text.encode()).hexdigest() 
    @staticmethod
    def match_hashed_text(hashedText, providedText):
        """
            Check for the text in the hashed text
        """
        _hashedText, salt = hashedText.split(':')
        return _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()
    @staticmethod
    def hash_quota(data:dict):
        hashinput = data["quotatitle"].lower().replace(" ","",100) + data["quotatype"].lower().replace(" ","",100)
        quotahash = MaturityHash.hash_text(hashinput)
        return quotahash
if __name__ == "__main__":
    # qpsignup - 82d7dc19d97ef3e5ffb6917ae5586d5090a489f16b9cca34250223cf6bef6583
    # GoogleAI:amari.lawal05@gmail.com
    #print(MaturityHash.hash_text("GoogleAI" + ":" + "amari.lawal05@gmail.com"))
    #fields = ("quoter","quotatitle","quotatype","thumbnail","description","visibility","quoterkey","thumbnailfiletype","quotahash")
    #value = ('GoogleAI', 'MaturityAI', 'A.I Assistant', b'image here', 'data:image/jpeg;base64,', 'd6bc8ca9302d5cb923f267833a666c20920672b5728ff162cf7d2de282999721')
    text = ""
    
    for i in ["86c8a9f00ff799e13202b79bed230368707369107729b344903632073c22ad40","a4fc8fd49a8c84a40d91c7a0f3927291556ab6fe717e5754dbb017181e6943d7"]:
        
        text += f"emailhash = '{i}'"
        text += " OR "
    finaltext = text[:text.rfind("OR")].strip()
    from Maturitycrud import MaturityCRUD
    Maturitycrud = MaturityCRUD()
    res = Maturitycrud.get_data(("email",),"contributors",finaltext)
    print(res)
    print(finaltext)

    #print(MaturityHash.hash_text("amari.lawal@gmail.com"))