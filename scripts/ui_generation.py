import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox
import cubie_generation
from maya import cmds

class RubiksCubeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rubik\'s Cube Generator')
        self.setFixedSize(300, 250)

        main_layout = QVBoxLayout()
        size_layout = QHBoxLayout()
        self.size_label = QLabel('Rubik\'s Cube Size:')
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setMinimum(1)
        self.size_spinbox.setValue(3)
        
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_spinbox)

        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate_cube)

        self.delete_button = QPushButton('Delete Cube')
        self.delete_button.clicked.connect(self.delete_cube)
        self.delete_button.hide()

        main_layout.addLayout(size_layout)
        main_layout.addWidget(self.generate_button)
        main_layout.addWidget(self.delete_button)

        self.rotation_buttons = QVBoxLayout()
        self.rotation_buttons.setSpacing(10)

        self.rotate_x_button = QPushButton('Rotate X')
        self.rotate_y_button = QPushButton('Rotate Y')
        self.rotate_z_button = QPushButton('Rotate Z')

        self.rotate_x_button.clicked.connect(lambda: self.rotate_face('X'))
        self.rotate_y_button.clicked.connect(lambda: self.rotate_face('Y'))
        self.rotate_z_button.clicked.connect(lambda: self.rotate_face('Z'))

        self.rotation_buttons.addWidget(self.rotate_x_button)
        self.rotation_buttons.addWidget(self.rotate_y_button)
        self.rotation_buttons.addWidget(self.rotate_z_button)

        self.rotate_x_button.hide()
        self.rotate_y_button.hide()
        self.rotate_z_button.hide()

        main_layout.addLayout(self.rotation_buttons)
        self.setLayout(main_layout)

    def generate_cube(self):
        cube_size = self.size_spinbox.value()
        print(f'Generating Rubik\'s cube of size {cube_size}')
        self.main(cube_size)
        self.generate_button.hide()
        self.size_spinbox.hide()
        self.size_label.hide()
        self.delete_button.show()
        self.rotate_x_button.show()
        self.rotate_y_button.show()
        self.rotate_z_button.show()

    def delete_cube(self):
        print('Deleting Rubik\'s cube')
        # Logic to delete the cube in Maya
        cmds.select(all=True)
        cmds.delete()
        self.generate_button.show()
        self.delete_button.hide()
        self.rotate_x_button.hide()
        self.rotate_y_button.hide()
        self.rotate_z_button.hide()
        self.size_spinbox.show()
        self.size_label.show()

    def rotate_face(self, axis):
        print(f'Rotating {axis} face')

    def main(self, cube_size):
        print(f'Main function called with cube size: {cube_size}')
        cubie_generation.main(cube_size)

def show_ui():
    app = QApplication.instance()  
    if app is None:
        app = QApplication(sys.argv)
    window = RubiksCubeUI()
    window.show()
    sys.exit(app.exec_())
