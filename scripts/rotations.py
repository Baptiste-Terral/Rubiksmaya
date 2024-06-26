from maya import cmds

def rotate_right_face():
    # Select faces of the right face
    cmds.select('cubie1.f[1]', 'cubie4.f[1]', 'cubie7.f[1]', 'cubie16.f[3]', 'cubie19.f[3]', 'cubie22.f[3]', r=True)
    cmds.rotate(90, 0, 0, r=True)

def rotate_left_face():
    # Select faces of the left face
    cmds.select('cubie3.f[3]', 'cubie6.f[3]', 'cubie9.f[3]', 'cubie18.f[1]', 'cubie21.f[1]', 'cubie24.f[1]', r=True)
    cmds.rotate(-90, 0, 0, r=True)

def rotate_up_face():
    # Select faces of the top face
    cmds.select('cubie7.f[4]', 'cubie8.f[4]', 'cubie9.f[4]', 'cubie19.f[0]', 'cubie20.f[0]', 'cubie21.f[0]', r=True)
    cmds.rotate(0, 0, 90, r=True)

def rotate_down_face():
    # Select faces of the bottom face
    cmds.select('cubie1.f[0]', 'cubie2.f[0]', 'cubie3.f[0]', 'cubie16.f[4]', 'cubie17.f[4]', 'cubie18.f[4]', r=True)
    cmds.rotate(0, 0, -90, r=True)

def rotate_front_face():
    # Select faces of the front face
    cmds.select('cubie7.f[2]', 'cubie8.f[2]', 'cubie9.f[2]', 'cubie16.f[2]', 'cubie17.f[2]', 'cubie18.f[2]', r=True)
    cmds.rotate(0, 90, 0, r=True)

def rotate_back_face():
    # Select faces of the back face
    cmds.select('cubie1.f[5]', 'cubie2.f[5]', 'cubie3.f[5]', 'cubie19.f[5]', 'cubie20.f[5]', 'cubie21.f[5]', r=True)
    cmds.rotate(0, -90, 0, r=True)

def rotate_x_axis():
    # Rotate the entire cube around the X-axis
    print('Rotating around X-axis')
    cmds.select('cubie*', r=True)
    cmds.rotate(90, 0, 0, r=True)

def rotate_y_axis():
    # Rotate the entire cube around the Y-axis
    cmds.select('cubie*', r=True)
    cmds.rotate(0, 90, 0, r=True)

def rotate_z_axis():
    # Rotate the entire cube around the Z-axis
    cmds.select('cubie*', r=True)
    cmds.rotate(0, 0, 90, r=True)

def rotate_middle_slice():
    # Rotate the middle slice (M move)
    # Example: Select middle cubies and rotate
    cmds.select('cubie10', 'cubie13', 'cubie16', 'cubie19', 'cubie22', r=True)
    cmds.rotate(0, 90, 0, r=True)

