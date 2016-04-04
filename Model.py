#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TP INGE 2 FOR PYTHON ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ (Phone Book Project) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ due on March, 25, 2016 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ by Louise RAPILLY, Aurélien LABAUTE & Matthieu CLEMENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ class 2C1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ || MODEL FILE || ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#  Library imported
from PyQt5 import QtWidgets


class Model:
    """Model Class : stores the data that is retrieved according to commands from the controller and displayed in the view"""

    def __init__(self):
        """Constructor of Model"""
        self.buffer = QtWidgets.QTreeWidgetItem()
        self.listContact = []
        self.bufferString = "Family name, First name, Telephone number, Address, Postal code, City, Mail"

    def registerContact(self, newElement, oldElement):
        """Register contact by adding the contact in listContact"""
        self.buffer = newElement
        if oldElement is None:
            self.listContact.append(self.buffer)
        else:
            if oldElement in self.listContact:
                self.listContact.remove(oldElement)
                self.listContact.append(self.buffer)
        self.listContact.sort()
        return True

    def eraseContact(self, item):
        """Erase selected contact in listContact"""
        if len(self.listContact) > 0:
            if item in self.listContact:
                self.listContact.remove(item)
            return True
        else:
            return False

    def exportCSV(self):
        """Export a CSV file and add it to listContact"""
        for contact in self.listContact:
            self.bufferString += "\n"
            for indexColumn in range(7):
                self.bufferString += contact.text(indexColumn)
                if indexColumn < 6:
                    self.bufferString += ","
        return str(self.bufferString)

    def searchContact(self, strContact):
        """Search the contact into listContact and display the contact searched"""
        newListContact = []
        for item in self.listContact:
            for indexColumn in range(7):
                if (strContact.lower() in item.text(indexColumn).lower()) and not (item in newListContact):
                    newListContact.append(item)
        if not newListContact:
            noResult = QtWidgets.QTreeWidgetItem()
            noResult.setText(0, "Aucun résultat trouvé")
            newListContact.append(noResult)
        return newListContact
