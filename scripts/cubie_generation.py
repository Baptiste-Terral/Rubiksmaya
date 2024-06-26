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
    'white': [1.0, 1.0, 1.0],
    'yellow': [1.0, 1.0, 0.0],
    'blue': [0.0, 0.0, 1.0],
    'green': [0.0, 1.0, 0.0],
    'red': [1.0, 0.0, 0.0],
    'orange': [1.0, 0.647, 0.0],
    'black': [0.0, 0.0, 0.0],
    'purple': [0.502, 0.0, 0.502] # for debugging purposes
}

def create_material(name, color):
    if not cmds.objExists(name):
        material = cmds.shadingNode('lambert', asShader=True, name=name)
        cmds.setAttr(f'{material}.color', color[0], color[1], color[2], type='double3')
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{name}SG')
        cmds.connectAttr(f'{material}.outColor', f'{shading_group}.surfaceShader', force=True)
    return name

def apply_black_border(cubie, face_index):
    face_str = f'{cubie}.f[{face_index}]'
    cmds.select(face_str)
    
    # First extrude out slightly to create the border
    extrude_node = cmds.polyExtrudeFacet(localTranslateZ=0.01, keepFacesTogether=True)[0]
    
    # Select the new faces created by the extrusion
    cmds.select(f'{cubie}.f[{face_index}]', add=True)
    cmds.select(f'{cubie}.e[*]', deselect=True)
    
    # Assign the black material to the border faces
    cmds.hyperShade(assign=[0.0, 0.0, 0.0])
    
    # Deselect the border faces and reselect the original face
    cmds.select(f'{cubie}.f[{face_index}]', toggle=True)
    
    # Extrude the original face back to its original position
    cmds.polyExtrudeFacet(extrude_node, edit=True, localTranslateZ=-0.01)

def apply_black_to_uncolored_faces(cubie):
    # Get the number of faces of the cubie
    face_count = cmds.polyEvaluate(cubie, face=True)
    black_color = [0.0, 0.0, 0.0]
    
    for i in range(face_count):
        face_str = f'{cubie}.f[{i}]'
        
        # Check if the face already has a material applied
        shaders = cmds.listConnections(face_str, type='shadingEngine')
        
        if not shaders:
            # Assign the material to the face
            cmds.select(face_str)  # Select the face
            cmds.hyperShade(assign=[0.0, 0.0, 0.0])  # Assign the material to the selected face


# apply material on a single face of a cubie
def apply_material(cubie, face_index, material):
    face_str = f'{cubie}.f[{face_index}]'
    cmds.select(face_str)
    cmds.hyperShade(assign=material)
    print(f'Applied material {material} to {face_str}')
    # Apply black border around the face
    apply_black_border(cubie, face_index)

def main(cube_size):
    custom_matrices = generate_custom_matrices(cube_size)
    cube_names = []

    materials = {color_name: create_material(color_name, color) for color_name, color in colors.items()}

    # 1x1x1 cube
    if cube_size == 1:
        matrix = custom_matrices[0]
        cubie_name = create_cubie(1, matrix, 0)
        cube_names.append(cubie_name)

        # apply materials for each face
        face_indices = {
            'front': 2,
            'back': 0,
            'left': 3,
            'right': 1,
            'bottom': 5,
            'top': 4
        }

        apply_material(cube_names[0], face_indices['right'], materials['orange'])
        apply_material(cube_names[0], face_indices['left'], materials['red'])
        apply_material(cube_names[0], face_indices['top'], materials['yellow'])
        apply_material(cube_names[0], face_indices['bottom'], materials['white'])
        apply_material(cube_names[0], face_indices['front'], materials['green'])
        apply_material(cube_names[0], face_indices['back'], materials['blue'])
    
    # 2x2x2 cube
    if cube_size == 2:
        for i, matrix in enumerate(custom_matrices):
            cubie_name = create_cubie(1, matrix, i)
            cube_names.append(cubie_name)

        # Apply materials for each cubie based on its position
        for cubie in cube_names:
            pos = cmds.xform(cubie, query=True, translation=True, worldSpace=True)
            print(f'Position of {cubie}: {pos}')

            # Determine which faces need which colors based on the position
            if round(pos[0], 1) == -0.5 and round(pos[1], 1) == -0.5 and round(pos[2], 1) == -0.5:
                # Bottom-left-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == -0.5 and round(pos[1], 1) == -0.5 and round(pos[2], 1) == 0.5:
                # Bottom-left-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == -0.5 and round(pos[1], 1) == 0.5 and round(pos[2], 1) == -0.5:
                # Top-left-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == -0.5 and round(pos[1], 1) == 0.5 and round(pos[2], 1) == 0.5:
                # Top-left-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == 0.5 and round(pos[1], 1) == -0.5 and round(pos[2], 1) == -0.5:
                # Bottom-right-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 4, materials['yellow'])
            elif round(pos[0], 1) == 0.5 and round(pos[1], 1) == -0.5 and round(pos[2], 1) == 0.5:
                # Bottom-right-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 4, materials['yellow'])
            elif round(pos[0], 1) == 0.5 and round(pos[1], 1) == 0.5 and round(pos[2], 1) == -0.5:
                # Top-right-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 4, materials['yellow'])
            elif round(pos[0], 1) == 0.5 and round(pos[1], 1) == 0.5 and round(pos[2], 1) == 0.5:
                # Top-right-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 4, materials['yellow'])
    
    # 3x3x3 cube
    if cube_size == 3:
        for i, matrix in enumerate(custom_matrices):
            cubie_name = create_cubie(1, matrix, i)
            cube_names.append(cubie_name)
        
        # color centers of each face of the cube
        # white center
        apply_material(cube_names[4], 5, materials['white'])
        # yellow center
        apply_material(cube_names[22], 4, materials['yellow'])
        # blue center
        apply_material(cube_names[12], 2, materials['blue'])
        # green center
        apply_material(cube_names[14], 0, materials['green'])
        # red center
        apply_material(cube_names[10], 3, materials['red'])
        # orange center
        apply_material(cube_names[16], 1, materials['purple'])

        # Corners
        for cubie in cube_names:
            pos = cmds.xform(cubie, query=True, translation=True, worldSpace=True)
            print(f'Position of {cubie}: {pos}')

            # Determine which faces need which colors based on the position
            if round(pos[0], 1) == -1.0 and round(pos[1], 1) == -1.0 and round(pos[2], 1) == -1.0:
                # Bottom-left-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == -1.0 and round(pos[1], 1) == -1.0 and round(pos[2], 1) == 1.0:
                # Bottom-left-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == -1.0 and round(pos[1], 1) == 1.0 and round(pos[2], 1) == -1.0:
                # Top-left-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == -1.0 and round(pos[1], 1) == 1.0 and round(pos[2], 1) == 1.0:
                # Top-left-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 5, materials['white'])
            elif round(pos[0], 1) == 1.0 and round(pos[1], 1) == -1.0 and round(pos[2], 1) == -1.0:
                # Bottom-right-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 4, materials['yellow'])
            elif round(pos[0], 1) == 1.0 and round(pos[1], 1) == -1.0 and round(pos[2], 1) == 1.0:
                # Bottom-right-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 3, materials['red'])
                apply_material(cubie, 4, materials['yellow'])
            elif round(pos[0], 1) == 1.0 and round(pos[1], 1) == 1.0 and round(pos[2], 1) == -1.0:
                # Top-right-back
                apply_material(cubie, 2, materials['blue'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 4, materials['yellow'])
            elif round(pos[0], 1) == 1.0 and round(pos[1], 1) == 1.0 and round(pos[2], 1) == 1.0:
                # Top-right-front
                apply_material(cubie, 0, materials['green'])
                apply_material(cubie, 1, materials['purple'])
                apply_material(cubie, 4, materials['yellow'])

        # Edges
        # White blue edge
        apply_material(cube_names[3], 2, materials['blue'])
        apply_material(cube_names[3], 5, materials['white'])
        # White green edge
        apply_material(cube_names[5], 0, materials['green'])
        apply_material(cube_names[5], 5, materials['white'])
        # White red edge
        apply_material(cube_names[1], 3, materials['red'])
        apply_material(cube_names[1], 5, materials['white'])
        # White orange edge
        apply_material(cube_names[7], 1, materials['purple'])
        apply_material(cube_names[7], 5, materials['white'])
        # Yellow blue edge
        apply_material(cube_names[21], 2, materials['blue'])
        apply_material(cube_names[21], 4, materials['yellow'])
        # Yellow green edge
        apply_material(cube_names[23], 0, materials['green'])
        apply_material(cube_names[23], 4, materials['yellow'])
        # Yellow red edge
        apply_material(cube_names[19], 3, materials['red'])
        apply_material(cube_names[19], 4, materials['yellow'])
        # Yellow orange edge
        apply_material(cube_names[25], 1, materials['purple'])
        apply_material(cube_names[25], 4, materials['yellow'])
        # Blue red edge
        apply_material(cube_names[9], 2, materials['blue'])
        apply_material(cube_names[9], 3, materials['red'])
        # Blue orange edge
        apply_material(cube_names[15], 2, materials['blue'])
        apply_material(cube_names[15], 1, materials['purple'])
        # Green red edge
        apply_material(cube_names[11], 0, materials['green'])
        apply_material(cube_names[11], 3, materials['red'])
        # Green orange edge
        apply_material(cube_names[17], 0, materials['green'])
        apply_material(cube_names[17], 1, materials['purple'])

    # n x n x n cube
    # later

    return cube_names
