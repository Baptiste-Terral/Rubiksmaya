from maya import cmds
from maya.api import OpenMaya as om


# CUBE GENERATION

def generate_custom_matrices(cube_size):
    matrices = []
    offset = (cube_size - 1) / 2.0

    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                pos = om.MVector(x - offset, y - offset, z - offset)
                rotation = om.MEulerRotation(0, 0, 0)  # No rotation initially
                scale = om.MVector(1, 1, 1)  # No scaling initially

                # Create MTransformationMatrix
                transformation_matrix = om.MTransformationMatrix()
                transformation_matrix.setTranslation(pos, om.MSpace.kWorld)
                transformation_matrix.setRotation(rotation)
                transformation_matrix.setScale(scale, om.MSpace.kWorld)

                # Get MMatrix representation of the transformation matrix
                matrix = transformation_matrix.asMatrix()

                matrices.append(matrix)

    return matrices

def create_cubie(size, matrix, index):
    cubie_name = f'cubie{index}'
    cubie = cmds.polyCube(width=size, height=size, depth=size, name=cubie_name)[0]
    cmds.xform(cubie, matrix=matrix)
    return cubie_name


# COLOR

colors = {
    'white': [255, 255, 255],
    'yellow': [255, 255, 0],
    'blue': [0, 0, 255],
    'green': [0, 255, 0],
    'red': [255, 0, 0],
    'orange': [255, 160, 0]
}

def create_material(name, color):
    if not cmds.objExists(name):
        material = cmds.shadingNode('lambert', asShader=True, name=name)
        cmds.setAttr(f'{material}.color', color[0], color[1], color[2], type='double3')
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{name}SG')
        cmds.connectAttr(f'{material}.outColor', f'{shading_group}.surfaceShader', force=True)
    return name

def apply_material(cubie, face_indices, material):
    for face_index in face_indices:
        face_str = f'{cubie}.f[{face_index}]'
        cmds.select(face_str)
        cmds.hyperShade(assign=material)

def color_cubies(cube_names, cube_size, colors):
    # Create materials
    materials = {color_name: create_material(color_name, color) for color_name, color in colors.items()}
    
    offset = (cube_size - 1) / 2.0
    face_indices = {
        'left': [3],
        'right': [1],
        'bottom': [5],
        'top': [4],
        'front': [2],
        'back': [0]
    }

    for cubie in cube_names:
        pos = cmds.xform(cubie, query=True, translation=True, worldSpace=True)
        
        # X-axis faces
        if round(pos[0]) == -offset:
            apply_material(cubie, face_indices['left'], materials['red'])    # Left face
        if round(pos[0]) == offset:
            apply_material(cubie, face_indices['right'], materials['orange']) # Right face
        # Y-axis faces
        if round(pos[1]) == -offset:
            apply_material(cubie, face_indices['bottom'], materials['white'])  # Bottom face
        if round(pos[1]) == offset:
            apply_material(cubie, face_indices['top'], materials['yellow']) # Top face
        # Z-axis faces
        if round(pos[2]) == -offset:
            apply_material(cubie, face_indices['front'], materials['blue'])   # Front face
        if round(pos[2]) == offset:
            apply_material(cubie, face_indices['back'], materials['green'])  # Back face
        

# MAIN

def main(cube_size):
    custom_matrices = generate_custom_matrices(cube_size)
    cube_names = []
    for i, matrix in enumerate(custom_matrices):
        cubie_name = create_cubie(1, matrix, i + 1)
        cube_names.append(cubie_name)
    color_cubies(cube_names, cube_size, colors)
    return cube_names