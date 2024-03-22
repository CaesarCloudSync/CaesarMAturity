class MaturityCreateTables:
    def __init__(self) -> None:
        self.usersfields = ("email","password")
        self.maturityassessmentsfields = ("author_email","maturityassessment")
        self.functionfields = ("maturityassessment","function")
        self.categoryfields = ("function","category")
        self.subcategoryfields = ("category","subcategory","grade")
        self.questionratingfields = ("subcategory","questionrating")
        self.questionfields = ("questionrating","question","evidenceforservice")
        self.maturityassessmentaccessfields = ("email","maturityassessment")

        
    # Creates the SQL Tables.
    def create(self,Maturitycrud):
        Maturitycrud.create_table("userid",self.usersfields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL"),
        "users")
        Maturitycrud.create_table("maturityassessmentid",self.maturityassessmentsfields,
        ("varchar(255)  NOT NULL","varchar(255) NOT NULL"),
        "maturityassessments")

        Maturitycrud.create_table("functionid",self.functionfields,
        ("TEXT NOT NULL","TEXT NOT NULL"),
        "functions")

        Maturitycrud.create_table("categoryid",self.categoryfields,
        ("TEXT NOT NULL","TEXT NOT NULL"),
        "categorys")

        Maturitycrud.create_table("subcategoryid",self.subcategoryfields,
        ("TEXT NOT NULL","TEXT NOT NULL","INT NOT NULL"),
        "subcategorys")

        Maturitycrud.create_table("questionratingid",self.questionratingfields,
        ("TEXT NOT NULL","TEXT NOT NULL"),
        "questionratings")

        Maturitycrud.create_table("questionid",self.questionfields,
        ("TEXT NOT NULL","TEXT NOT NULL","TEXT NOT NULL"),
        "questions")
        Maturitycrud.create_table("maturityassessmentaccessid",self.maturityassessmentaccessfields ,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL"),
        "maturityassessmentaccess")
        


