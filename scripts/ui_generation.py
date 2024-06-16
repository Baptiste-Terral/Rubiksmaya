from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class RubiksCubeUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RubiksCubeUI, self).__init__(parent)
        self.setWindowTitle("Rubik's Cube Generator")
        self.setFixedSize(300, 200)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.size_label = QtWidgets.QLabel("Rubik's Cube Size:")
        layout.addWidget(self.size_label)
        
        self.size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.size_slider.setMinimum(2)
        self.size_slider.setMaximum(10)
        self.size_slider.setValue(3)
        layout.addWidget(self.size_slider)
        
        self.generate_button = QtWidgets.QPushButton("Generate Rubik's Cube")
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_cube)

    def generate_cube(self):
        size = self.size_slider.value()
        cubies = generate_rubiks_cube(size)
        group_faces(size, cubies)

def show_ui():
    ui = RubiksCubeUI(parent=maya_main_window())
    ui.show()

show_ui()


