import pyray as rl

class Spell:
    def __init__(self, caster, body = None, subbody = None, element = None, hand_position = None):
        self.caster = caster
        self.body = body
        self.subbody = subbody
        self.element = element
        self.hand_position = hand_position
        self.properties = dict()

    def merge(self, other_spell):
        pass

    def double_all_properties(self):
        for i in range(len(self.properties)):
            self.properties[i] *= 2

    def add_property(self, property, value):
        if property not in self.properties:
            self.properties[property] = value
        self.properties[property] += value

    def render_rune(self, x,y,SPELL_SIZE):
        if self.hand_position:
            hand_texture = self.caster.game.assets_loader.get_texture(self.caster.game.assets_loader.hand_positions_path + self.hand_position+".png")
            rl.draw_texture_pro(
                hand_texture,
                rl.Rectangle(0, 0, hand_texture.width, hand_texture.height),
                rl.Rectangle(x, y, SPELL_SIZE, SPELL_SIZE),
                rl.Vector2(0, 0),
                0,
                rl.WHITE
            )
            return
        if self.element:
            body_texture = self.caster.game.assets_loader.get_texture(self.caster.game.assets_loader.body_positions_path + self.caster.game.assets_loader.bodies[self.body][self.subbody]+".png")
            ok, cor = self.caster.game.assets_loader.color_element(self.element)
            rl.draw_texture_pro(
                body_texture,
                rl.Rectangle(0, 0, body_texture.width, body_texture.height),
                rl.Rectangle(x, y, SPELL_SIZE, SPELL_SIZE),
                rl.Vector2(0, 0),
                0,
                rl.Color(*cor)
            )
            return
        if self.body and self.subbody == None:
            body_texture = self.caster.game.assets_loader.get_texture(self.caster.game.assets_loader.body_positions_path + self.caster.game.assets_loader.bodies[self.body]["None"]+".png")
            ok, cor = self.caster.game.assets_loader.color_element(self.element)
            rl.draw_texture_pro(
                body_texture,
                rl.Rectangle(0, 0, body_texture.width, body_texture.height),
                rl.Rectangle(x, y, SPELL_SIZE, SPELL_SIZE),
                rl.Vector2(0, 0),
                0,
                rl.Color(*cor)
            )
            return

        rl.draw_rectangle(x, y, SPELL_SIZE, SPELL_SIZE, rl.GRAY)        
