import pymel.core as pm
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def mayaWindow():

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)


def every_other(every_other_variable, selection):
    
    selection_length = len(selection)
    pm.select(clear=True)
    if every_other_variable == 1:
        pm.select(selection)
    elif every_other_variable == 0:
        pm.select(clear = True)
    else:
        for i in range(selection_length):
            if i%every_other_variable == True:
                pm.select(selection[i], add = True)


def custom_pattern (selected_var, deselected_var, selection ):

    selection_length = len(selection)
    pm.select(clear=True)

    for i in range(selected_var): #number of faces that should be skipped
        step_custom_pattern = 0
        result = 0
    
        while result < selection_length:
            temp = i + ((selected_var + deselected_var)*step_custom_pattern)
            if (temp >= selection_length):
                break
            else:
                result = temp
            print(f' Ergebnis: {result}')
            pm.select(selection[result], add = True)
            step_custom_pattern +=1
            print(f'w: {step_custom_pattern}')



class pattern_selection(QtWidgets.QDialog):

	
    def __init__(self,parent=mayaWindow()):
            
        self.winName = "Pattern Selection"
        self.geo_name = ""
        self.selection = 0
        self.every_other_variable = 0
        self.selected_variable = 0
        self.not_selected_variable = 0

        super(pattern_selection,self).__init__(parent)
              
        self.setWindowTitle(self.winName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, 1)
        self.resize(400, 250)
        self.layout()

	
    def layout(self):
	
        self.save_selection_group = QtWidgets.QGroupBox("Save Selection")
        self.every_other_group = QtWidgets.QGroupBox("Every Other")
        self.custom_pattern_group = QtWidgets.QGroupBox("Custom Pattern")
        

        self.save_selection_layout = QtWidgets.QHBoxLayout()
        self.save_selection_button = QtWidgets.QPushButton("Save Selection", self)
        self.save_selection_layout.addWidget(self.save_selection_button)
        self.save_selection_group.setLayout(self.save_selection_layout)
	
	
        self.every_other_text_layout = QtWidgets.QHBoxLayout()
        self.every_other_text_layout.setSpacing(2)
        self.every_other_text = QtWidgets.QLabel("Select every: ")
        self.every_other_input = QtWidgets.QSpinBox()
        self.every_other_input.setSingleStep(1)
        self.every_other_input.setValue(0) 
        self.every_other_text.setAlignment(QtCore.Qt.AlignCenter)
        self.every_other_input.setAlignment(QtCore.Qt.AlignCenter)
        self.every_other_text_layout.addWidget(self.every_other_text)
        self.every_other_text_layout.addWidget(self.every_other_input)

        self.every_other_button_layout = QtWidgets.QHBoxLayout()
        #self.every_other_button_layout.setContentsMargins(1,1,1,1)
        self.every_other_button = QtWidgets.QPushButton("Select",self)
        self.every_other_button_layout.addWidget(self.every_other_button)

        self.every_other_layout = QtWidgets.QVBoxLayout()
        self.every_other_layout.setContentsMargins(6, 1, 6, 2)
        self.every_other_layout.addLayout(self.every_other_text_layout)
        self.every_other_layout.addLayout(self.every_other_button_layout)
        self.every_other_group.setLayout(self.every_other_layout)


        self.custom_pattern_select_input_layout = QtWidgets.QHBoxLayout()
        self.custom_pattern_select_input_layout.setContentsMargins(1, 1, 1, 1)
        self.custom_pattern_select_text = QtWidgets.QLabel("Select: ")
        self.custom_pattern_select_input = QtWidgets.QSpinBox()
        self.custom_pattern_select_input.setSingleStep(1) 
        self.custom_pattern_select_input.setValue(0)
        self.custom_pattern_select_input_layout.addWidget(self.custom_pattern_select_text)
        self.custom_pattern_select_input_layout.addWidget(self.custom_pattern_select_input)


        self.custom_pattern_deselect_input_layout = QtWidgets.QHBoxLayout()
        self.custom_pattern_deselect_input_layout.setSpacing(2)
        self.custom_pattern_deselect_input_layout.setContentsMargins(1, 1, 1, 1)
        self.custom_pattern_deselect_text = QtWidgets.QLabel("Deselect: ")
        self.custom_pattern_deselect_input = QtWidgets.QSpinBox()
        self.custom_pattern_deselect_input.setSingleStep(1) 
        self.custom_pattern_deselect_input.setValue(0)
        self.custom_pattern_deselect_input_layout.addWidget(self.custom_pattern_deselect_text)
        self.custom_pattern_deselect_input_layout.addWidget(self.custom_pattern_deselect_input)

        self.custom_pattern_button_layout = QtWidgets.QHBoxLayout()
        self.custom_pattern_button_layout.setContentsMargins(1,1,1,1)
        self.custom_pattern_button = QtWidgets.QPushButton("Select",self)
        self.custom_pattern_button_layout.addWidget(self.custom_pattern_button)

        self.custom_pattern_layout = QtWidgets.QVBoxLayout()
        self.custom_pattern_layout.setContentsMargins(6, 1, 6, 2)
        self.custom_pattern_layout.addLayout(self.custom_pattern_select_input_layout)
        self.custom_pattern_layout.addLayout(self.custom_pattern_deselect_input_layout)
        self.custom_pattern_layout.addLayout(self.custom_pattern_button_layout)
        self.custom_pattern_group.setLayout(self.custom_pattern_layout)


        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.addWidget(self.save_selection_group)
        main_layout.addWidget(self.every_other_group)
        main_layout.addWidget(self.custom_pattern_group)
        self.setLayout(main_layout)

        self.save_selection_button.clicked.connect(self.save_selection)
        self.every_other_button.clicked.connect(self.every_other_selection)
        self.custom_pattern_button.clicked.connect(self.custom_pattern_selection)

    def save_selection(self):

        self.selection = pm.ls(selection=True, fl=True)
        print(self.selection)

    def every_other_selection(self):

        self.every_other_variable = self.every_other_input.value()
        print(self.every_other_variable)
        every_other(self.every_other_variable, self.selection)

    def custom_pattern_selection(self):

        self.selected_variable = self.custom_pattern_select_input.value()
        self.deselected_variable = self.custom_pattern_deselect_input.value()
        print(self.selected_variable)
        print(self.deselected_variable)
        custom_pattern(self.selected_variable, self.deselected_variable, self.selection)

                                       
if __name__=="__main__":
    myWin = pattern_selection()
    myWin.show()
