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
