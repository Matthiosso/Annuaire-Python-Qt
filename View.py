#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TP INGE 2 FOR PYTHON ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ (Phone Book Project) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ due on March, 25, 2016 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Louise RAPILLY, Aurélien LABAUTE & Matthieu CLEMENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ class 2C1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ || VIEW FILE || ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Libraries imported
from PyQt5 import QtWidgets, QtCore, QtGui


class View(QtWidgets.QMainWindow):
    """Represent the data shown in the main window"""

    def __init__(self, control, nom, app):
        """Constructor of View"""
        super(View, self).__init__()

        #  Initialization of important variables:
        self.control = control
        self.app = app
        self.tableOfContact = QtWidgets.QTreeWidget()
        self.editBox = EditBox(self)
        self.contactBox = ContactBox(self)
        self.toolBar = QtWidgets.QToolBar()
        self.searchBar = QtWidgets.QLineEdit()
        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.isModified = False

        # Function calls to create all the interface:
        self.createAction()
        self.createMenu()
        self.createToolBar()
        self.createTable()

        # To set the design of the View:
        self.setWindowTitle(nom)
        self.setFixedSize(1000, 600)
        self.mainLayout.addWidget(self.tableOfContact)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.searchBar.setStyleSheet("color: #1ED760;"
                                     "background-color: #545454;"
                                     "border: 1px solid #1ED760;"
                                     "border-radius: 2px")
        self.mainWidget.setStyleSheet("color: solid black;"
                           "background-color: #282828;"
                           "font-family: Comic sans MS, Arial, sans-serif")
        self.tableOfContact.setAlternatingRowColors(True)
        self.tableOfContact.setStyleSheet("color: #1ED760;"
                                          "alternate-background-color: #545454;"
                                          "font-family: Comic sans MS, Arial, sans-serif")
        self.searchBar.setToolTip("Search Contact")
        self.setCursor(QtGui.QCursor(QtGui.QPixmap(r"Images/mouse.png"),0.85,1.66))
        self.setWindowIcon(QtGui.QIcon(r"Images/logopyqt.png"))

    def beforeClose(self):
        """Function to ask the user to save before closing the program"""
        if self.isModified:
            ret = QtWidgets.QMessageBox.warning(self, "Warning !","The table has not been saved !\n"
                                                "Do you want to save your changes before closing?",
                                                QtWidgets.QMessageBox.Save |
                                                QtWidgets.QMessageBox.Discard |
                                                QtWidgets.QMessageBox.Cancel)
            if ret == QtWidgets.QMessageBox.Save:
                self.exportContacts()
                return True
            elif ret == QtWidgets.QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, event):
        """Function called when we close a window"""
        if self.beforeClose():
            event.accept()
            QtWidgets.QMainWindow.close(self)
            self.app.quit()
        else:
            event.ignore()

    def handleItemDoubleClicked(self):
        """Function called when we double click on an item"""
        self.displayContact()

    def handleItemSelected(self):
        """Function to change the color of selected items to see them better"""
        for index in range(self.tableOfContact.topLevelItemCount()):
            for column in range(7):
                self.tableOfContact.topLevelItem(index).setForeground(column, QtGui.QBrush(QtGui.QColor(30, 215, 96)))
        if self.tableOfContact.currentItem() is not None:
            for column in range(7):
                self.tableOfContact.currentItem().setForeground(column, QtGui.QBrush(QtGui.QColor(255,0,0)))

    def indexOfCurrentElement(self):
        """Returns the the index of the current element"""
        return self.tableOfContact.indexOfTopLevelItem(self.tableOfContact.currentItem())

    def createAction(self):
        """Creates the actions"""
        self.actionQuit = QtWidgets.QAction("&Quit", self)              # Name
        self.actionQuit.setShortcut(QtGui.QKeySequence.Close)           # Shortcut
        self.actionQuit.setIcon(QtGui.QIcon(r"Images/exit.png"))        # Icon

        self.actionNewContact = QtWidgets.QAction("&New Contact", self)
        self.actionNewContact.setShortcut(QtGui.QKeySequence.New)
        self.actionNewContact.setIcon(QtGui.QIcon(r"Images/newcontact.png"))

        self.actionModContact = QtWidgets.QAction("&Modify Contact", self)
        self.actionModContact.setShortcut(QtGui.QKeySequence.Replace)
        self.actionModContact.setIcon(QtGui.QIcon(r"Images/modifycontact.png"))

        self.actionDelContact = QtWidgets.QAction("&Delete Contact", self)
        self.actionDelContact.setShortcut(QtGui.QKeySequence.Delete)
        self.actionDelContact.setIcon(QtGui.QIcon(r"Images/deletecontact.png"))

        self.actionImportFile = QtWidgets.QAction("&Open File", self)
        self.actionImportFile.setShortcut(QtGui.QKeySequence.Open)
        self.actionImportFile.setIcon(QtGui.QIcon(r"Images/open.png"))

        self.actionExportFile = QtWidgets.QAction("&Save File", self)
        self.actionExportFile.setShortcut(QtGui.QKeySequence.Save)
        self.actionExportFile.setIcon(QtGui.QIcon(r"Images/save.png"))

        self.actionDisplay = QtWidgets.QAction("Display &Contact", self)
        self.actionDisplay.setIcon(QtGui.QIcon(r"Images/displaycontact.png"))

        self.actionSearch = QtWidgets.QAction("Searc&h", self)
        self.actionSearch.setShortcut(QtCore.Qt.Key_Return)

        self.actionAbout = QtWidgets.QAction("&About", self)
        self.actionAbout.setShortcut(QtGui.QKeySequence.HelpContents)

        #  Connections of the buttons:
        self.actionQuit.triggered.connect(self.close)
        self.actionNewContact.triggered.connect(self.newContact)
        self.actionModContact.triggered.connect(self.modContact)
        self.actionDelContact.triggered.connect(self.delContact)
        self.actionExportFile.triggered.connect(self.exportContacts)
        self.actionImportFile.triggered.connect(self.importContacts)
        self.actionDisplay.triggered.connect(self.displayContact)
        self.actionAbout.triggered.connect(self.app.aboutQt)
        self.actionSearch.triggered.connect(self.searchContact)
        self.searchBar.textChanged.connect(self.searchContact)
        self.tableOfContact.itemSelectionChanged.connect(self.handleItemSelected)
        self.tableOfContact.itemDoubleClicked.connect(self.handleItemDoubleClicked)

    def createMenu(self):
        """Creates the menu and add the actions"""
        self.menuFile = self.menuBar().addMenu("&File")
        self.menuFile.addAction(self.actionQuit)
        self.menuFile.addAction(self.actionImportFile)
        self.menuFile.addAction(self.actionExportFile)

        self.menuContacts = self.menuBar().addMenu("&Contact")
        self.menuContacts.addAction(self.actionNewContact)
        self.menuContacts.addAction(self.actionModContact)
        self.menuContacts.addAction(self.actionDelContact)
        self.menuContacts.addAction(self.actionDisplay)

        self.menuHelp = self.menuBar().addMenu("&?")
        self.menuHelp.addAction(self.actionAbout)

    def createToolBar(self):
        """Creates the toolbar"""
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)         # Add it on top of the main window

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.toolBar.addAction(self.actionNewContact)
        self.toolBar.addAction(self.actionModContact)
        self.toolBar.addAction(self.actionDelContact)
        self.toolBar.addAction(self.actionDisplay)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExportFile)
        self.toolBar.addAction(self.actionImportFile)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.searchBar)
        self.toolBar.addWidget(spacer)
        self.toolBar.addAction(self.actionQuit)

        self.toolBar.setStyleSheet("color: black;"
                           "background-color: #545454")

    def createTable(self):
        """Creates the the table containing the contacts"""
        self.tableOfContact.setColumnCount(7)
        self.listHeaderLabels = ["Family name", "First name",
                                 "Telephone number", "Address",
                                 "Postal code",
                                 "City", "Mail"]
        self.tableOfContact.setHeaderLabels(self.listHeaderLabels)
        for i in range(7):
            self.tableOfContact.setColumnWidth(i, 130)

    def searchContact(self):
        """Function to search a contact in the list of contact"""
        self.control.searchContact(self.searchBar.text())

    def newContact(self):
        """Function to add a new contact to the list of contact"""
        self.editBox.modification = False
        self.editBox.show()

    def modContact(self):
        """Function to modify a contact already registered"""
        if self.tableOfContact.currentItem() is not None:
            self.editBox.modification = True
            self.editBox.show()
        else:
            QtWidgets.QMessageBox.information(self,"Information", "There isn't any selected contact to modify.")

    def delContact(self):
        """Function to delete a contact"""
        if self.tableOfContact.currentItem() is not None:
            answer = QtWidgets.QMessageBox.question(self, "Warning !","Are you sure you want to delete this contact ?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                if self.control.eraseContact(self.tableOfContact.currentItem()):
                    self.tableOfContact.takeTopLevelItem(self.indexOfCurrentElement())
                    QtWidgets.QMessageBox.information(self,"Information","The contact has been successfully deleted.")
                    self.isModified = True
                else:
                    QtWidgets.QMessageBox.warning(self,"Warning ! ","There isn't any contact to delete!")
            else:
                QtWidgets.QMessageBox.information(self,"Information","The contact has not been deleted.")
        else:
            QtWidgets.QMessageBox.warning(self,"Warning !", "There isn't any selected contact to delete!")

    def registerContact(self, modification):
        """Function to send the contact to control"""
        if not modification:
            self.control.registerContact(self.editBox.contact.clone())
        else:
            self.control.registerContact(self.editBox.contact.clone(), self.tableOfContact.currentItem())
        self.sortContacts()
        self.isModified = True

    def exportContacts(self):
        """Function to save the contact list, send it to control"""
        self.control.exportCSV()


    def importContacts(self):
        """Function to add a list of contact from control"""
        self.control.importCSV()
        self.sortContacts()


    def sortContacts(self):
        """Function to sort the list of contact by alphabetic order"""
        self.tableOfContact.sortByColumn(0, QtCore.Qt.AscendingOrder)

    def displayContact(self):
        """Function to call the Contact Box to display contact information"""
        if (self.tableOfContact.currentItem() != None):
            self.contactBox.show()
        else:
            QtWidgets.QMessageBox.information(self,"Information", "There isn't any selected contact to display.")

    def clearAll(self):
        """Delete every contact"""
        self.control.clearAll()


class EditBox(QtWidgets.QDialog):
    """ Edit Interface for editing Class"""

    def __init__(self, parent=None):
        """Contructor of EditBox"""

        super(EditBox, self).__init__(None, QtCore.Qt.WindowTitleHint |
                                      QtCore.Qt.WindowCloseButtonHint |
                                      QtCore.Qt.WindowSystemMenuHint)
        #  Initialization of important variables:
        self.view = parent
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                                    QtWidgets.QDialogButtonBox.Cancel |
                                                    QtWidgets.QDialogButtonBox.Reset)
        self.contact = QtWidgets.QTreeWidgetItem()
        self.modification = False
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.frameWidget = QtWidgets.QGroupBox("New Contact")
        self.formLayout = QtWidgets.QFormLayout()

        #  To set each field to fill:
        self.familyNameField = QtWidgets.QLineEdit()
        familyNameFont = QtGui.QFont()
        familyNameFont.setCapitalization(QtGui.QFont.AllUppercase)
        self.familyNameField.setFont(familyNameFont)
        self.familyNameField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z\- ]*")))

        self.firstNameField = QtWidgets.QLineEdit()
        firstNameFont = QtGui.QFont()
        firstNameFont.setCapitalization(QtGui.QFont.Capitalize)
        self.firstNameField.setFont(firstNameFont)
        self.firstNameField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Zà-ü\- ]*")))

        self.numberField = QtWidgets.QLineEdit()
        self.numberField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("(00|\+)33[1-9][0-9]{8}|0[0-9]{9}")))

        self.addressField = QtWidgets.QLineEdit()
        self.addressField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9à-ü\- ]*")))

        self.postalCodeField = QtWidgets.QLineEdit()
        self.postalCodeField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{5}")))

        self.cityField = QtWidgets.QLineEdit()
        self.cityField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Zà-ü\- ]*")))

        self.mailField = QtWidgets.QLineEdit()
        self.mailField.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9\-_\.]*"
                                                                          "@[a-zA-Z0-9\-_]*"
                                                                          "\.[a-zA-Z]*")))

        #  To add each row to the form:
        self.formLayout.addRow("Family &Name", self.familyNameField)
        self.formLayout.addRow("&First Name", self.firstNameField)
        self.formLayout.addRow("&Telephone Number", self.numberField)
        self.formLayout.addRow("&Address", self.addressField)
        self.formLayout.addRow("&Postal Code", self.postalCodeField)
        self.formLayout.addRow("&City", self.cityField)
        self.formLayout.addRow("&Mail", self.mailField)

        self.frameWidget.setLayout(self.formLayout)
        self.mainLayout.addWidget(self.frameWidget)
        self.mainLayout.addWidget(self.buttonBox)

        # For the design:
        self.setLayout(self.mainLayout)
        self.frameWidget.setStyleSheet( "border: 1px solid #1ED760;"
                                        "border-radius: 2px;"
                                        "margin-top: 5px;"
                                        "padding: 2 3px")
        self.setWindowTitle("Edit")
        self.setStyleSheet("color: #ADAFB2;"
                           "background-color: #282828;"
                           "font-family: Verdana, Arial, sans-serif")
        self.setFixedSize(500, 300)
        self.setModal(True)
        self.setCursor(QtGui.QCursor(QtGui.QPixmap(r"Images/mouse.png"),0.85,1.66))

        #  Connections for each buttons:
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.OKPressed)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.clearForm)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.hide)

    def OKPressed(self):
        """Pick each elements of the form and send them to the View for registering"""
        self.contact.setText(0, self.familyNameField.text().upper())
        self.contact.setText(1, self.firstNameField.text().title())
        self.contact.setText(2, self.numberField.text())
        self.contact.setText(3, self.addressField.text())
        self.contact.setText(4, self.postalCodeField.text())
        self.contact.setText(5, self.cityField.text())
        self.contact.setText(6, self.mailField.text().lower())
        if not self.isEmpty():
            self.view.registerContact(self.modification)
            self.hide()
        else:
            QtWidgets.QMessageBox.warning(self,"Warning !","You can't register an empty contact!")
        self.view.contactBox.updateContact()

    def showEvent(self, QShowEvent):
        """Function called when the window is shown"""
        self.clearForm()
        if self.modification is True:
            self.frameWidget.setTitle("Modifying Contact")
            self.setWindowIcon(QtGui.QIcon(r"modifycontact.png"))
            self.fillForm(self.view.tableOfContact.currentItem())
        else:
            self.frameWidget.setTitle("New Contact")
            self.setWindowIcon(QtGui.QIcon(r"Images/newcontact.png"))

    def clearForm(self):
        """To clear all the fields of the form"""
        self.familyNameField.setText("")
        self.firstNameField.setText("")
        self.numberField.setText("")
        self.addressField.setText("")
        self.postalCodeField.setText("")
        self.cityField.setText("")
        self.mailField.setText("")
        self.familyNameField.setFocus()

    def fillForm(self, element):
        """To fill the form with a specified element (to modify an already existing element)"""
        self.contact = element.clone()
        if not self.isEmpty():
            self.familyNameField.setText(element.text(0))
            self.firstNameField.setText(element.text(1))
            self.numberField.setText(element.text(2))
            self.addressField.setText(element.text(3))
            self.postalCodeField.setText(element.text(4))
            self.cityField.setText(element.text(5))
            self.mailField.setText(element.text(6))

    def isEmpty(self):
        """To check if the fields of the form are all empty"""
        for i in range(self.contact.columnCount()):
            if self.contact.text(i) != "":
                return False
        return True


class ContactBox(QtWidgets.QDialog):
    """ Contact Interface to look at information about the contact Class"""
    def __init__(self, parent = None):
        """Constructor of ContactBox"""
        super(ContactBox, self).__init__()
        self.view = parent
        self.contact = QtWidgets.QTreeWidgetItem()
        self.contactLayout = QtWidgets.QHBoxLayout()
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.modifyButton = QtWidgets.QPushButton("Modify contact")
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.addButton(self.modifyButton, QtWidgets.QDialogButtonBox.ActionRole)
        self.infoBox = QtWidgets.QLabel()
        self.imageBox = QtWidgets.QLabel()
        self.image = QtGui.QPixmap()
        self.image.load(r"Images/social.png")
        self.imageBox.setPixmap(self.image.scaled(100, 100))
        self.text = ""

        self.contactLayout.addWidget(self.infoBox)
        self.contactLayout.addWidget(self.imageBox)
        self.mainLayout.addLayout(self.contactLayout)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

        #  For design:
        self.setFixedSize(400, 200)
        self.setStyleSheet("color: #ADAFB2;"
                           "background-color: #282828")
        self.setWindowIcon(QtGui.QIcon(r"Images/social.png"))
        self.setCursor(QtGui.QCursor(QtGui.QPixmap(r"Images/mouse.png"),0.85,1.66))
        self.setModal(True)

        #  Connections of the buttons:
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.hide)
        self.modifyButton.clicked.connect(self.modContact)

    def updateContact(self):
        """To update the contact's display in the Contact Box"""
        self.contact = self.view.tableOfContact.currentItem()
        self.setWindowTitle("Contact : %s %s" % (self.contact.text(0), self.contact.text(1)))
        for column in range(7):
            self.text += str(self.view.listHeaderLabels[column] + "  :  " + self.contact.text(column) + "\n")
        self.infoBox.setText(self.text)
        self.text = ""

    def modContact(self):
        """To modify the contact in view"""
        self.view.modContact()

    def showEvent(self, QShowEvent):
        """Function called when the window is shown"""
        self.updateContact()