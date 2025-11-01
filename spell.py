import pyray as rl

class Spell:
    def __init__(self, caster, body = None, subbody = None, element = None, hand_position = None):
        self.caster = caster
        self.body = body
        self.subbody = subbody
        self.element = element
        self.hand_position = hand_position
        self.properties = dict()
        self.add_native_atributes()
        self.ceil_values = 1024

    def add_native_atributes(self):
        if self.hand_position:
            self.properties = self.caster.game.assets_loader.hand_positions_properties[self.hand_position].copy()
        elif self.element:
            self.properties = self.caster.game.assets_loader.elements_properities[self.element].copy()
            

    def merge(self, other_spell):
        # if self.hand_position and other_spell.hand_position
        pass

    def double_all_properties(self):
        number_violation = False
        for key in self.properties:
            self.properties[key] *= 2
            if self.properties[key] > self.ceil_values:
                self.properties[key] = self.ceil_values
                number_violation = True
        if number_violation:
            self.caster.messages.append(("Some spell properties reached maximum value of {}".format(self.ceil_values), 120))

        print("Doubled spell properties:", self.properties)

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
