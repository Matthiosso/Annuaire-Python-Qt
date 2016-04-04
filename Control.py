#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TP INGE 2 FOR PYTHON ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ (Phone Book Project) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ due on March, 25, 2016 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Louise RAPILLY, Aurélien LABAUTE & Matthieu CLEMENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ class 2C1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ || CONTROL FILE || ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#  Librairies imported
from PyQt5 import QtWidgets
from View import View
from Model import Model
import csv


class Control:
    """Control Class: Commands the View and the Model, and deals with interactions between them."""

    def __init__(self, app):
        """Constructor of Control"""
        self.view = View(self, "Phone Book", app)
        self.view.show()
        self.model = Model()

    def exportCSV(self):
        """Export contacts into a CSV file"""
        fileDialog = QtWidgets.QFileDialog.getSaveFileName(self.view,
                                                           "Save File",
                                                           "untitled",
                                                           "CSV files (*.csv);;All Files (*)")
        fileName = str(fileDialog).partition('\'')[2].split('\'')[0]
        if not (fileName is ""):
            with open(fileName, "wb") as file:
                file.write(str(self.model.exportCSV()).encode('Latin-1'))
            QtWidgets.QMessageBox.information(self.view,
                                              "Save succeeded",
                                              "The file has been successfully saved in the folder : " + fileName,
                                              QtWidgets.QMessageBox.Close)
            self.view.isModified = False
        else:
            QtWidgets.QMessageBox.information(self.view, "Save failed", "The file has not been saved.")

    def importCSV(self):
        """Import contacts from a CSV file"""
        fileDialog = QtWidgets.QFileDialog.getOpenFileName(self.view, "Open File", None, "CSV Files (*.csv)")
        fileName = str(fileDialog).partition('\'')[2].split('\'')[0]
        if not (fileName is ""):
            if not self.model.listContact:
                answer = QtWidgets.QMessageBox.No
            else:
                answer = QtWidgets.QMessageBox.question(self.view, "Death or life choice !?",
                                                        "Would you like to append the contacts to your actual list?",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.No:
                self.clearAll()
            with open(fileName, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for nbLine, row in enumerate(reader):
                    tempElement = QtWidgets.QTreeWidgetItem()
                    if nbLine != 0:
                        for index, word in enumerate(row):
                            tempElement.setText(index, word)
                        self.registerContact(tempElement.clone())
            QtWidgets.QMessageBox.information(self.view,
                                              "Open succeeded",
                                              "The file has been successfully opened in the folder : " + fileName,
                                              QtWidgets.QMessageBox.Close)
        else:
            QtWidgets.QMessageBox.information(self.view, "Open failed", "The file has not been opened.")

    def registerContact(self, newElement, oldElement = None):
        """Register contacts in Model before adding them to the View"""
        if self.model.registerContact(newElement.clone(), oldElement):
            if oldElement is not None:
                self.view.tableOfContact.takeTopLevelItem(self.view.indexOfCurrentElement())
            self.view.tableOfContact.addTopLevelItem(self.model.buffer)
            self.view.tableOfContact.setCurrentItem(self.model.buffer)

    def eraseContact(self, item):
        """Erase contacts in model and by doing so, authorized the View to delete it too"""
        if self.model.listContact:
            if not self.model.eraseContact(item):
                return False
            else:
                return True
        else:
            return False

    def searchContact(self, strContact):
        """Search the text entered by the user among the list of contacts in model"""
        if self.model.listContact:
            newListContact = self.model.searchContact(strContact)
            if newListContact:
                #  Erase contacts in the view before inserting the ones among
                # the new list containing the searched contacts:
                size = int(self.view.tableOfContact.topLevelItemCount())
                if size != 0:
                    for index in reversed(range(size)):
                        self.view.tableOfContact.takeTopLevelItem(index)
                for contact in newListContact:
                    self.view.tableOfContact.addTopLevelItem(contact)

    def clearAll(self):
        """Erase all contacts from the Model and the View"""
        size = int(self.view.tableOfContact.topLevelItemCount())
        if size != 0:
            for index in reversed(range(size)):
                self.model.eraseContact(index)
                self.view.tableOfContact.takeTopLevelItem(index)
