from PySide6.QtWidgets import QWidget, QTabWidget, QApplication,  QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
import json
# from homeTaskView import TaskAppView
import sys

# this window will have 2 views: using QTabWidget 1 for creatign account and the other for signing in
class MainFormWindow(QWidget):
    def __init__(self, app):
        self.app = app # app will be given as an argument to MainFormWindow on start which will be assigned to variable app
        super().__init__()

        # window title
        self.setWindowTitle("KaliDevTrack")

        tab_widget = QTabWidget() # this tabWidget takes in widgets 


        # first widget: createAccout
        createAccount = QWidget()
        

        # creating variable to be used for allocating window: why: enable toggling
        self.taskView = None;

        # set layout
        vLayout = QVBoxLayout()


        user_label = QLabel('Email:')
        self.username_input = QLineEdit()

        passwd_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # add widgets to vLayout
        vLayout.addWidget(user_label)
        vLayout.addWidget(self.username_input)
        vLayout.addWidget(passwd_label)
        vLayout.addWidget(self.password_input)


        # setting up buttons
        buttonLayout = QHBoxLayout()

        cancelBtn = QPushButton('Cancel')
        okBtn = QPushButton("Sign Up")

        # setting button functionality
        cancelBtn.clicked.connect(self.quit_app) # quit application
        # okBtn.clicked.connect(self.get_user_details) testing
        okBtn.clicked.connect(self.WriteUserDetails)
        # okBtn.clicked.connect(self.openTaskHome) # open taskView

        # add buttons to buttonLayout
        buttonLayout.addWidget(cancelBtn)
        buttonLayout.addWidget(okBtn)



        # add button layout
        vLayout.addLayout(buttonLayout)
        createAccount.setLayout(vLayout)



        """
        alreadyLabel = QLabel("already have an Account")
        signBtn = QPushButton("SignIn")

        horLayout = QHBoxLayout()
        horLayout.addWidget(alreadyLabel)
        horLayout.addWidget(signBtn)

        vLayout.addLayout(horLayout)
        """

        # second widget:login
        loginView = QWidget()

        login_username = QLabel('Email:')
        login_username_line_input = QLineEdit()
        login_passwd = QLabel('Password')
        login_passwd_line_input = QLineEdit()


        # buttons
        LoginBtn = QPushButton("Login")
        loginCancelBtn  = QPushButton("Cancel")

        # add functionality to loginButtons
        loginCancelBtn.clicked.connect(self.quit_app)


        # set layouts
        loginFormLayout = QVBoxLayout()
        loginFormLayout.addWidget(login_username)
        loginFormLayout.addWidget(login_username_line_input)
        loginFormLayout.addWidget(login_passwd)
        loginFormLayout.addWidget(login_passwd_line_input)

        # horizontal layout for buttons
        login_hor_layout = QHBoxLayout()
        login_hor_layout.addWidget(loginCancelBtn)
        login_hor_layout.addWidget(LoginBtn)

        loginFormLayout.addLayout(login_hor_layout)

        loginView.setLayout(loginFormLayout)

        tab_widget.addTab(createAccount, "Sign Up")
        tab_widget.addTab(loginView, "Login In")

        # add layout to window
        # self.setLayout(vLayout)

        formLayout = QVBoxLayout()
        formLayout.addWidget(tab_widget)
        
        self.setLayout(formLayout)
        # set size for window
        self.resize(500,100)




    # class methods
    def quit_app(self):
        self.app.quit()

    def get_user_details(self):
        print(f"username : {self.username_input.text()}")
        print(f"password : {self.password_input.text()}")
        

    def WriteUserDetails(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_detail_dictionary = {"user_name":username, "password":password}
        # print(f"user_detail_dictionary : ${user_detail_dictionary}") testing
        with open("./data/userDetails.json", "a") as file:
            # print('file has been opened writing data to file') testing
            file.write(",")
            json.dump(user_detail_dictionary, file)

    # def openTaskHome(self):
    #     if self.taskView == None:
    #         self.taskView = TaskAppView()
    #         self.taskView.show()
    #     else:
    #         self.taskView.close()
    #         self.taskView = None



"""
to set mask characters for password we use:
``QLineEdit.EchoMode.Password``  
as the use enters the password they're masked by the platform dependent mask: it can be circles in kali linux
while stars in windows

``line_editVarName.setEchoMode(QLineEdit.EchoMode.Password)``
learn more from : [link](https://www.pythonguis.com/docs/qlineedit/)
"""



app = QApplication()
window = MainFormWindow(app)
window.show()
exit_code = app.exec()
sys.exit(exit_code)