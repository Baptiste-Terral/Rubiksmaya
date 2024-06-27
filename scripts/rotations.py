from maya import cmds

CUBIE_PREFIX = 'cubie'

def get_cube_size():
    cubie_count = len(cmds.ls(f'{CUBIE_PREFIX}*'))
    if cubie_count == 8:
        return 2
    elif cubie_count == 27:
        return 3
    else:
        if cubie_count % 27 == 0:
            return cubie_count // 27
        else:
            raise ValueError(f"Unsupported number of cubies: {cubie_count}. Cannot determine cube size.")

def get_face_cubies(face):
    size = get_cube_size()
    threshold = -size * 0.5  # Adjust this threshold based on your cubie positions

    face_cubies = []

    for i in range(size ** 3):
        cubie = f'{CUBIE_PREFIX}{i}'
        pos = cmds.xform(cubie, q=True, ws=True, t=True)
        print(f'{cubie} position: {pos}')

        if face == 'U' and pos[1] < threshold:
            face_cubies.append(cubie)
        elif face == 'D' and pos[1] > -threshold:
            face_cubies.append(cubie)
        elif face == 'L' and pos[0] < -threshold:
            face_cubies.append(cubie)
        elif face == 'R' and pos[0] > threshold:
            face_cubies.append(cubie)
        elif face == 'F' and pos[2] > threshold:
            face_cubies.append(cubie)
        elif face == 'B' and pos[2] < -threshold:
            face_cubies.append(cubie)

    print(f'Face {face} cubies: {face_cubies}')
    return face_cubies

def rotate_face(face, degrees, axis):
    cubies = get_face_cubies(face)
    if not cubies:
        raise ValueError(f"No cubies found for face: {face}")

    temp_group = cmds.group(cubies, n='temp_rotate_group')
    
    print(f'Rotating face {face} around axis {axis} by {degrees} degrees')
    
    if axis == 'x':
        cmds.rotate(degrees, 0, 0, temp_group, r=True)
    elif axis == 'y':
        cmds.rotate(0, degrees, 0, temp_group, r=True)
    elif axis == 'z':
        cmds.rotate(0, 0, degrees, temp_group, r=True)
    else:
        cmds.delete(temp_group)
        raise ValueError(f"Invalid axis: {axis}")

    cmds.parent(cubies, w=True)
    cmds.delete(temp_group)

def rotate_right_face():
    rotate_face('R', 90, 'x')

def rotate_left_face():
    rotate_face('L', -90, 'x')

def rotate_up_face():
    rotate_face('U', 90, 'y')

def rotate_down_face():
    rotate_face('D', -90, 'y')

def rotate_front_face():
    rotate_face('F', 90, 'z')

def rotate_back_face():
    rotate_face('B', -90, 'z')

def rotate_x_axis():
    cubies = cmds.ls(f'{CUBIE_PREFIX}*')
    temp_group = cmds.group(cubies, n='temp_rotate_group')
    cmds.rotate(90, 0, 0, temp_group, r=True)
    cmds.parent(cubies, w=True)
    cmds.delete(temp_group)

def rotate_y_axis():
    cubies = cmds.ls(f'{CUBIE_PREFIX}*')
    temp_group = cmds.group(cubies, n='temp_rotate_group')
    cmds.rotate(0, 90, 0, temp_group, r=True)
    cmds.parent(cubies, w=True)
    cmds.delete(temp_group)

def rotate_z_axis():
    cubies = cmds.ls(f'{CUBIE_PREFIX}*')
    temp_group = cmds.group(cubies, n='temp_rotate_group')
    cmds.rotate(0, 0, 90, temp_group, r=True)
    cmds.parent(cubies, w=True)
    cmds.delete(temp_group)
