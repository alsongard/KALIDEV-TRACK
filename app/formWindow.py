from PySide6.QtWidgets import QWidget, QTabWidget,QMessageBox, QApplication,  QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
import json
# from homeTaskView import TaskAppView
import sys, os, bcrypt, secrets
from threading import Timer

from homeTaskView import TaskAppView

# this window will have 2 views: using QTabWidget 1 for creatign account and the other for signing in
class MainFormWindow(QWidget):
    def __init__(self, app):
        self.app = app # app will be given as an argument to MainFormWindow on start which will be assigned to variable app
        super().__init__()
        self.filepath = './data/userDetails.json'
        # window title
        self.setWindowTitle("KaliDevTrack")

        tab_widget = QTabWidget() # this tabWidget takes in widgets 


        # first widget: createAccout
        createAccount = QWidget()
        

        # creating variable to be used for allocating window: why: enable toggling
        self.taskView = None

        # set layout
        vLayout = QVBoxLayout()


        user_label = QLabel('Email:', parent=None)
        self.username_input = QLineEdit()

        passwd_label = QLabel("Password:", parent=None)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # add widgets to vLayout
        vLayout.addWidget(user_label)
        vLayout.addWidget(self.username_input)
        vLayout.addWidget(passwd_label)
        vLayout.addWidget(self.password_input)

        self.successMsg =QLabel("")


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
        self.login_username_line_input = QLineEdit()
        login_passwd = QLabel('Password')
        self.login_passwd_line_input = QLineEdit()
        self.login_passwd_line_input.setEchoMode(QLineEdit.EchoMode.Password)


        # buttons
        LoginBtn = QPushButton("Login")
        loginCancelBtn  = QPushButton("Cancel")

        # add functionality to loginButtons
        loginCancelBtn.clicked.connect(self.quit_app)
        LoginBtn.clicked.connect(self.checkLogin)


        # set layouts
        loginFormLayout = QVBoxLayout()
        loginFormLayout.addWidget(login_username)
        loginFormLayout.addWidget(self.login_username_line_input)
        loginFormLayout.addWidget(login_passwd)
        loginFormLayout.addWidget(self.login_passwd_line_input)

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

        
    def success_msg_set(self):
        self.successMsg.setText("")

    def WriteUserDetails(self):
        username = self.username_input.text()
        password = self.password_input.text()
        filepath=self.filepath

        # generate random string
        gen_user_id = secrets.token_hex(16)

        passwd_encoded = password.encode()
        hashed_password = bcrypt.hashpw(passwd_encoded, bcrypt.gensalt())
        decoded_hash_passwd = hashed_password.decode() # decoding rom bytes to string for storage
        # print(decoded_hash_passwd) testing=working correctly

        user_detail_dictionary = {"user_name":username, "password":decoded_hash_passwd, 'user_id':gen_user_id}
        # print(user_detail_dictionary) testing=working correctly
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'r') as file:
                data = json.load(file)
        else:
            # print(f'File is empty')
            data = []

        data.append(user_detail_dictionary)
        responseMsgBox = QMessageBox.information(
            self,
            "Information",
            "Proceed to Login to continue", 
            QMessageBox.StandardButton.Ok
        )
        with open(filepath, 'w') as file:
            json.dump(data, file)
            print('Data has been successfully added to file')
            self.successMsg.setText("User Account created Successfully")
            timer = Timer(3.0, self.success_msg_set)
            timer.start()
    
    def checkLogin(self):
        # get username &  get password
        username = self.login_username_line_input.text()
        userpassword = self.login_passwd_line_input.text()
        # get data from file:
        filepath=self.filepath

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file) # return an array of dictionaries
            for item in data: 
                if item['user_name'] == username:
                    # print('user found') # testing:working
                    # print(f'found user: {item}') # testing:working
                    getHashedPassword = item['password']
                    getUserId = item['user_id']
                    encoded_passwd = userpassword.encode()
                    getPasswdByte = getHashedPassword.encode()
                    # print(f"Type of getPsswdByte: {type(getPasswdByte)} and data : {getPasswdByte}") testing:working correctly
                    # try and compare the password
                    # when working with the bcrypt module it is required to encode this data: hence encoding both passwords:userpassword,getHashPassword
                    
                    print(f" result of checkpw is {bcrypt.checkpw(encoded_passwd, getPasswdByte)}")
                    if bcrypt.checkpw(encoded_passwd,getPasswdByte): # returns boolean
                        print(f'User {username}  found and password True')
                        userLoginFound=True
                        self.successMessage()
                        new_window = TaskAppView.get_instance(username,getUserId)
                        new_window.show()
                        new_window.activateWindow()
                        new_window.raise_()
                        self.close()
                        timer = Timer(3.0, self.success_msg_set)
                        timer.start()
                        # self.w = TaskAppView(username, getUserId)
                        # self.w.show()
                        # break
                    else:
                        print("Wrong password")
                        self.alertMessage()
                        # break
        else:
            print('Wrong file path : {filepath}')

    def successMessage(self):
        messageObject = QMessageBox()
        messageObject.setMinimumSize(700, 200)
        messageObject.setWindowTitle("Login Successfull")
        messageObject.setText("Continue to Applicaton")
        messageObject.setIcon(QMessageBox.Icon.Information)

        messageObject.setStandardButtons(
            QMessageBox.StandardButton.Ok 
        )
        messageObject.exec()


    def alertMessage(self):
        messageObject = QMessageBox()
        messageObject.setMinimumSize(700, 200)
        messageObject.setWindowTitle("Login failed")
        messageObject.setText("Invalid Credentials")
        messageObject.setIcon(QMessageBox.Icon.Critical)

        messageObject.setStandardButtons(
            QMessageBox.StandardButton.Ok 
        )
        messageObject.exec()







"""
to set mask characters for password we use:
``QLineEdit.EchoMode.Password``  
as the use enters the password they're masked by the platform dependent mask: it can be circles in kali linux
while stars in windows

``line_editVarName.setEchoMode(QLineEdit.EchoMode.Password)``
learn more from : [link](https://www.pythonguis.com/docs/qlineedit/)
"""



# app = QApplication()
# window = MainFormWindow(app)
# window.show()
# exit_code = app.exec()
# sys.exit(exit_code)