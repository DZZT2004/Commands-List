import sys
import json
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction, QFont
from PySide6.QtCore import Qt

class App(QApplication):

    languages = {}
    commands = {}
    currentCommand = None

    def __init__(self):
        super().__init__(sys.argv)
        self.setStyleSheet(Path(Path(__file__).parent.resolve().joinpath('style.qss')).read_text()) # we use pathlib to get the path to our stylesheet file
        self.setApplicationName('Hello World')
        self.createWindow()
        self.createMainLayout()
        self.createToolbar()
        self.createAllBoxes()
        
    def createWindow(self):
        self.mainWindow = QMainWindow()
        self.load()
        self.loadCommands()

    def createMainLayout(self):
        self.centralBox = QWidget(self.mainWindow)
        self.centralBox.setObjectName('centralBox')
        self.centralBox.setStyleSheet("#centralBox{border: 2px solid black; margin-bottom: 0px}")
        #Create a scroll area 
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.centralBox)
        layout = QVBoxLayout(self.centralBox)
        layout.setAlignment(Qt.AlignTop)
        self.mainWindow.setCentralWidget(self.scroll)

    def createToolbar(self):
        self.toolbar = QToolBar()
        self.centralBox.layout().addWidget(self.toolbar)
        addLangAction = QAction('Add Language', self.centralBox)
        addLangAction.triggered.connect(self.addLanguage)
        self.toolbar.addAction(addLangAction)
        removeLangAction = QAction('Remove Language', self.centralBox)
        removeLangAction.triggered.connect(self.removeLanguage)
        self.toolbar.addAction(removeLangAction)
        addType = QAction('Add Type', self.centralBox)
        addType.triggered.connect(self.addType)
        self.toolbar.addAction(addType)
        removeType = QAction('Remove Type', self.centralBox)
        removeType.triggered.connect(self.removeType)
        self.toolbar.addAction(removeType)
        self.toolbar.show()
        
    
    def createAllBoxes(self):
        self.load()
        temp = 0
        tempListValues = []
        key_values = list(self.languages.keys())
        for lang in self.languages:
            tempListValues = self.languages.get(key_values[temp])
            if tempListValues is not None:
                self.createLanguageBox(key_values[temp], tempListValues)
            elif tempListValues is None:
                self.createBlankBox(key_values[temp])
            temp += 1
            
    
    def createLanguageBox(self, key, values):
        box = QWidget()
        box.setObjectName("boxLanguage")
        layout = QHBoxLayout(box)
        layout.setAlignment(Qt.AlignLeft) 
        box.setMinimumHeight(100)
        label  = QLabel(text=key)
        label.setFont(QFont("Arial", 24))
        label.setMinimumWidth(200)
        layout.addWidget(label)
        for value in values:
            button = QPushButton(text = value)
            button.setFont(QFont("Arial", 14))
            #self.dumpCommands()
            self.commands.update({value: {}})
            button.clicked.connect(lambda: self.createSubInfoWindow(value))
            layout.addWidget(button)
        self.centralBox.layout().addWidget(box)
          
    def createBlankBox(self, key):
        box = QWidget()
        box.setObjectName("boxLanguage")
        layout = QHBoxLayout(box)
        layout.setAlignment(Qt.AlignLeft) 
        box.setMinimumHeight(100)
        label  = QLabel(text=key)
        label.setFont(QFont("Arial", 24))
        label.setMinimumWidth(200)
        layout.addWidget(label)
        self.centralBox.layout().addWidget(box)

    def addLanguage(self):
        result, ok = QInputDialog.getText(self.centralBox, 'Add Language', 'Enter a new language')
        if ok and result:
            self.languages.update({result: None})
            self.dump()
            self.clearLayout(self.centralBox.layout())
            self.createToolbar()
            self.createAllBoxes()
    
    def removeLanguage(self):
        result, ok = QInputDialog.getItem(self.centralBox, "Remove language",
                                "Languages:", self.languages.keys(), 0, False)
        if ok:
            self.languages.pop(result)
            self.dump()
            self.clearLayout(self.centralBox.layout())
            self.createToolbar()
            self.createAllBoxes()
        
    def addType(self):
        result, ok = QInputDialog.getItem(self.centralBox, "Select Language",
                                "languages:", self.languages.keys(), 0, False)
        if ok and result in self.languages:
            type, ok = QInputDialog.getText(self.centralBox, 'Add Type', 'Enter the type you want to add')
            if ok and type:
                if self.languages.get(result) is None:
                    temp1 = [type]
                else:
                    temp1 = self.languages.get(result)
                    temp1.append(type)
                temp = {result:temp1}
                self.languages.update(temp)
                self.dump()
                self.clearLayout(self.centralBox.layout())
                self.createToolbar()
                self.createAllBoxes()

    def removeType(self):
        result, ok = QInputDialog.getItem(self.centralBox, "Select Language",
                                "languages:", self.languages.keys(), 0, False)
        if ok:
            result2, ok2 = QInputDialog.getItem(self.centralBox, "Remove Type",
                                "Types:", self.languages.get(result), 0, False)
            if ok2:
                if self.languages.get(result) is None:
                    temp1 = [result2]
                else:
                    temp1 = self.languages.get(result)
                    temp1.remove(result2)
                temp = {result:temp1}
                self.languages.update(temp)
                self.dump()
                self.clearLayout(self.centralBox.layout())
                self.createToolbar()
                self.createAllBoxes()
                

    def dump(self):
        with open("data_file", "w") as write_file:
            json.dump(self.languages, write_file, indent=4)

    def dumpCommands(self):
        with open("commands_file", "w") as write_file:
            json.dump(self.commands, write_file, indent=4)
            print('dumped')


    def load(self):
        try:
            with open("data_file", "r") as read_file:
                self.languages = json.load(read_file)    
        except FileNotFoundError:
            self.dump()            
        

    def loadCommands(self):
        try:
            with open("commands_file", "r") as read_file:
                self.commands = json.load(read_file)
                print('loaded')
        except FileNotFoundError:
            self.dumpCommands()


    def createSubInfoWindow(self, command):
        self.currentCommand = command
        self.clearLayout(self.centralBox.layout())
        self.createSubInfoWindowToolbar()
        self.createAllSubInfoBoxes()

    def createSubInfoWindowToolbar(self):
        self.subtoolbar = QToolBar()
        self.centralBox.layout().addWidget(self.subtoolbar)

        addCommand = QAction('Add Command', self.centralBox)
        addCommand.triggered.connect(self.addCommand)
        self.subtoolbar.addAction(addCommand)

        removeCommand = QAction('Remove Command', self.centralBox)
        removeCommand.triggered.connect(self.removeCommand)
        self.subtoolbar.addAction(removeCommand)

        editCommand = QAction('Edit Command', self.centralBox)
        editCommand.triggered.connect(self.editCommand)
        self.subtoolbar.addAction(editCommand)

        backCommand = QAction('Go back', self.centralBox)
        backCommand.triggered.connect(self.backToLanguageMenu)
        self.subtoolbar.addAction(backCommand)

        self.subtoolbar.show()


    def createAllSubInfoBoxes(self):
        self.loadCommands()
        if self.commands.get(self.currentCommand) is not None:
            for command in self.commands.get(self.currentCommand):
                self.createSubInfoBox(command, self.commands.get(self.currentCommand).get(command))
        
        

    def createSubInfoBox(self, name, description):
        box = QWidget()
        box.setObjectName("boxCommandInfo")
        layout = QHBoxLayout(box)
        layout.setAlignment(Qt.AlignLeft) 
        box.setMinimumHeight(100)
        labelName = QLabel(text=name)
        labelName.setFont(QFont("Arial", 24))
        labelName.setMinimumWidth(200)
        layout.addWidget(labelName)
        labelDescription = QLabel(text=description)
        labelDescription.setFont(QFont("Arial", 14))
        labelDescription.setMinimumWidth(300)
        layout.addWidget(labelDescription)
        self.centralBox.layout().addWidget(box)

    def addCommand(self):
        resultName, ok = QInputDialog.getText(self.centralBox, 'Add Command', 'Enter a new command')
        if ok and resultName:
            resultDescription, ok2 = QInputDialog.getText(self.centralBox, 'Add Description', 'Enter the description')
            if ok2 and resultDescription:
                if self.commands.get(self.currentCommand) is not None:
                    self.commands.get(self.currentCommand).update({resultName: resultDescription})
                else:
                    self.commands.update({self.currentCommand: {resultName: resultDescription}})

            self.dumpCommands()
            self.clearLayout(self.centralBox.layout())
            self.createSubInfoWindowToolbar()
            self.createAllSubInfoBoxes()

    def removeCommand(self):
        resultName, ok = QInputDialog.getItem(self.centralBox, "Remove Command",
                                          "Commands:", self.commands.get(self.currentCommand).keys(), 0, False)
        if resultName and ok:
            self.commands.get(self.currentCommand).pop(resultName)
            self.dumpCommands()
            self.clearLayout(self.centralBox.layout())
            self.createSubInfoWindowToolbar()
            self.createAllSubInfoBoxes()

    def editCommand(self):
        resultName, ok = QInputDialog.getItem(self.centralBox, "Edit Command",
                                          "Commands:", self.commands.get(self.currentCommand).keys(), 0, False)
        if resultName and ok:
            resultDescription, ok2 = QInputDialog.getText(self.centralBox, 'Edit Description', 'Enter the description')
            if ok2 and resultDescription:
                self.commands.get(self.currentCommand).update({resultName: resultDescription})
            self.dumpCommands()
            self.clearLayout(self.centralBox.layout())
            self.createSubInfoWindowToolbar()
            self.createAllSubInfoBoxes()

    # Clears ALL widgets in the layout
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                layout.removeWidget(child.widget())
                # remove it from the gui
                child.widget().setParent(None)
    # Goes back to the language menu
    def backToLanguageMenu(self):
        self.clearLayout(self.centralBox.layout())
        self.createToolbar()
        self.createAllBoxes()


if __name__ == '__main__':
    app = App()
    app.mainWindow.show()
    app.exec()
