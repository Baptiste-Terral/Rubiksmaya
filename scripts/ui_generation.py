import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox
import cubie_generation, rotations
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
        self.size_spinbox.setMaximum(3) # Limiting to 3 for now
        
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
        self.rotate_r_button = QPushButton('Rotate R')
        self.rotate_l_button = QPushButton('Rotate L')
        self.rotate_u_button = QPushButton('Rotate U')
        self.rotate_d_button = QPushButton('Rotate D')
        self.rotate_f_button = QPushButton('Rotate F')
        self.rotate_b_button = QPushButton('Rotate B')

        self.rotate_x_button.clicked.connect(lambda: self.rotate_face('X'))
        self.rotate_y_button.clicked.connect(lambda: self.rotate_face('Y'))
        self.rotate_z_button.clicked.connect(lambda: self.rotate_face('Z'))
        self.rotate_r_button.clicked.connect(lambda: self.rotate_face('R'))
        self.rotate_l_button.clicked.connect(lambda: self.rotate_face('L'))
        self.rotate_u_button.clicked.connect(lambda: self.rotate_face('U'))
        self.rotate_d_button.clicked.connect(lambda: self.rotate_face('D'))
        self.rotate_f_button.clicked.connect(lambda: self.rotate_face('F'))
        self.rotate_b_button.clicked.connect(lambda: self.rotate_face('B'))

        self.rotation_buttons.addWidget(self.rotate_x_button)
        self.rotation_buttons.addWidget(self.rotate_y_button)
        self.rotation_buttons.addWidget(self.rotate_z_button)
        self.rotation_buttons.addWidget(self.rotate_r_button)
        self.rotation_buttons.addWidget(self.rotate_l_button)
        self.rotation_buttons.addWidget(self.rotate_u_button)
        self.rotation_buttons.addWidget(self.rotate_d_button)
        self.rotation_buttons.addWidget(self.rotate_f_button)
        self.rotation_buttons.addWidget(self.rotate_b_button)

        self.toggle_rotation_buttons(False)

        main_layout.addLayout(self.rotation_buttons)
        self.setLayout(main_layout)

    def toggle_rotation_buttons(self, state):
        if state:
            self.rotate_x_button.show()
            self.rotate_y_button.show()
            self.rotate_z_button.show()
            self.rotate_r_button.show()
            self.rotate_l_button.show()
            self.rotate_u_button.show()
            self.rotate_d_button.show()
            self.rotate_f_button.show()
            self.rotate_b_button.show()
        else:
            self.rotate_x_button.hide()
            self.rotate_y_button.hide()
            self.rotate_z_button.hide()
            self.rotate_r_button.hide()
            self.rotate_l_button.hide()
            self.rotate_u_button.hide()
            self.rotate_d_button.hide()
            self.rotate_f_button.hide()
            self.rotate_b_button.hide()

    def generate_cube(self):
        cube_size = self.size_spinbox.value()
        print(f'Generating Rubik\'s cube of size {cube_size}')
        self.main(cube_size)
        self.generate_button.hide()
        self.size_spinbox.hide()
        self.size_label.hide()
        self.delete_button.show()
        self.toggle_rotation_buttons(True)

    def delete_cube(self):
        print('Deleting Rubik\'s cube')
        # Logic to delete the cube in Maya
        cmds.select(all=True)
        cmds.delete()
        self.generate_button.show()
        self.delete_button.hide()
        self.toggle_rotation_buttons(False)
        self.size_spinbox.show()
        self.size_label.show()

    def rotate_face(self, axis): 
        if axis == 'X':
            rotations.rotate_x_axis()
        elif axis == 'Y':
            rotations.rotate_y_axis()
        elif axis == 'Z':
            rotations.rotate_z_axis()
        elif axis == 'R':
            rotations.rotate_right_face()
        elif axis == 'L':
            rotations.rotate_left_face()
        elif axis == 'U':
            rotations.rotate_up_face()
        elif axis == 'D':
            rotations.rotate_down_face()
        elif axis == 'F':
            rotations.rotate_front_face()
        elif axis == 'B':
            rotations.rotate_back_face()

    def main(self, cube_size):
        print(f'Main function called with cube size: {cube_size}')
        cubie_generation.main(cube_size)

def show_ui():
    app = QApplication.instance()  
    if app is None:
        app = QApplication(sys.argv)
    window = RubiksCubeUI()
    window.show()
