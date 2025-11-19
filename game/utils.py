from pyray import Vector3
import pyray

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

def draw_quad(texture: pyray.Texture, pos: pyray.Vector3, width, height, orientation="xy", src_rect: pyray.Rectangle=None):
    pyray.rl_push_matrix()
    pyray.rl_translatef(pos.x, pos.y, pos.z)

    pyray.rl_begin(pyray.RL_QUADS)
    pyray.rl_set_texture(texture.id)
    pyray.rl_color4ub(255, 255, 255, 255)

    if src_rect is None:
        u0,v0,u1,v1 = 0,0,1,1
    else:
        u0 = src_rect.x / texture.width
        v0 = src_rect.y / texture.height
        u1 = (src_rect.x + src_rect.width) / texture.width
        v1 = (src_rect.y + src_rect.height) / texture.height
    
    uvs = (u0,v1), (u0,v0), (u1,v0), (u1,v1)
    if orientation=="xy":
        positions = (0,0,0), (0,height,0), (width,height,0), (width,0,0)
    elif orientation=="zy":
        positions = (0,0,0), (0,height,0), (0,height,width), (0,0,width)
    elif orientation=="xz":
        positions = (0,0,0), (0,0,height), (width,0,height), (width,0,0)
    
    for i in range(4):
        create_uv_vertex(uvs[i],positions[i])

    pyray.rl_end()
    pyray.rl_set_texture(0)
    pyray.rl_pop_matrix()

def create_uv_vertex(uv, pos):
    pyray.rl_tex_coord2f(*uv); pyray.rl_vertex3f(*pos)

def draw_skybox(camera_pos, tex, src_sky, size=1000):

    half = size / 2

    # Centered at camera_pos
    x, y, z = camera_pos.x, camera_pos.y, camera_pos.z

    draw_quad(tex, pyray.Vector3(x+half, y-half, z-half), size, size, orientation="zy", src_rect=src_sky["+X"])
    draw_quad(tex, pyray.Vector3(x-half, y-half, z+half), -size, size, orientation="zy", src_rect=src_sky["-X"])
    draw_quad(tex, pyray.Vector3(x+half, y-half, z+half), -size, size, orientation="xy", src_rect=src_sky["-Z"])
    draw_quad(tex, pyray.Vector3(x-half, y-half, z-half), size, size, orientation="xy", src_rect=src_sky["+Z"])
    draw_quad(tex, pyray.Vector3(x-half, y+half, z-half), size, size, orientation="xz", src_rect=src_sky["+Y"])
    draw_quad(tex, pyray.Vector3(x-half, y-half, z-half), size, size, orientation="xz", src_rect=src_sky["-Y"])

def load_sky():
    sky_tex = pyray.load_texture("assets/skybox.jpg")
    face_w = sky_tex.width // 4
    face_h = sky_tex.height // 3

    sky_src = {
        "+Y": pyray.Rectangle(face_w, 0, face_w, face_h),
        "-Y": pyray.Rectangle(face_w, 2*face_h, face_w, face_h),
        "-X": pyray.Rectangle(0, face_h, face_w, face_h),
        "+Z": pyray.Rectangle(face_w, face_h, face_w, face_h),
        "+X": pyray.Rectangle(2*face_w, face_h, face_w, face_h),
        "-Z": pyray.Rectangle(3*face_w, face_h, face_w, face_h),
    }

    return sky_tex, sky_src