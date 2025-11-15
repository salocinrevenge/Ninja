from pyray import Vector3

def check_collision(a, b):
    # Calcula os limites min/max dos dois objetos
    a_min = Vector3(a.pos.x - a.dims.x/2, a.pos.y - a.dims.y/2, a.pos.z - a.dims.z/2)
    a_max = Vector3(a.pos.x + a.dims.x/2, a.pos.y + a.dims.y/2, a.pos.z + a.dims.z/2)
    b_min = Vector3(b.pos.x - b.dims.x/2, b.pos.y - b.dims.y/2, b.pos.z - b.dims.z/2)
    b_max = Vector3(b.pos.x + b.dims.x/2, b.pos.y + b.dims.y/2, b.pos.z + b.dims.z/2)

    return (
        a_min.x <= b_max.x and a_max.x >= b_min.x and
        a_min.y <= b_max.y and a_max.y >= b_min.y and
        a_min.z <= b_max.z and a_max.z >= b_min.z
    )

def check_colision_point(pos, dims, block_pos, block_dims):
    # Calcula os limites min/max do objeto
    obj_min = Vector3(pos.x - dims.x/2, pos.y, pos.z - dims.z/2)
    obj_max = Vector3(pos.x + dims.x/2, pos.y + dims.y, pos.z + dims.z/2)
    # Calcula os limites min/max do bloco
    block_min = Vector3(block_pos.x, block_pos.y, block_pos.z)
    block_max = Vector3(block_pos.x + block_dims.x, block_pos.y + block_dims.y, block_pos.z + block_dims.z)

    return (
        obj_min.x <= block_max.x and obj_max.x >= block_min.x and
        obj_min.y <= block_max.y and obj_max.y >= block_min.y and
        obj_min.z <= block_max.z and obj_max.z >= block_min.z
    )