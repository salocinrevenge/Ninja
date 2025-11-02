import pyray as rl

class Spell:
    def __init__(self, caster, body = None, subbody = None, element = None, hand_position = None):
        self.caster = caster
        self.body = body
        self.subbody = subbody
        self.element = element
        self.hand_position = hand_position
        self.properties = dict()
        self.ceil_values = 1024
        self.add_native_atributes()

    def add_native_atributes(self):
        if self.hand_position:
            new_properties = self.caster.game.assets_loader.hand_positions_properties.get(self.hand_position, None)
            print("Hand position properties for '{}': {}".format(self.hand_position, new_properties))
            for key, value in new_properties.items():
                self.add_property(key, value)
        elif self.element:
            new_properties = self.caster.game.assets_loader.elements_properities.get(self.element, None)
            for key, value in new_properties.items():
                self.add_property(key, value)

    def merge(self, other_spell):
        if self.hand_position and other_spell.hand_position:
            if self.hand_position in self.caster.game.assets_loader.loaded_recipes:
                if other_spell.hand_position in self.caster.game.assets_loader.loaded_recipes[self.hand_position]:
                    self.hand_position = self.caster.game.assets_loader.loaded_recipes[self.hand_position][other_spell.hand_position]
                    self.add_native_atributes()
            for key, value in other_spell.properties.items():
                self.add_property(key, value)
            return
        if self.element and other_spell.element:
            if self.body == other_spell.body and self.subbody == other_spell.subbody:
                if self.element in self.caster.game.assets_loader.loaded_recipes:
                    if other_spell.element in self.caster.game.assets_loader.loaded_recipes[self.element]:
                        self.element = self.caster.game.assets_loader.loaded_recipes[self.element][other_spell.element]
                        self.add_native_atributes()
                for key, value in other_spell.properties.items():
                    self.add_property(key, value)
            return
        if self.element and other_spell.hand_position:
            if self.element in self.caster.game.assets_loader.loaded_recipes:
                if other_spell.hand_position in self.caster.game.assets_loader.loaded_recipes[self.element]:
                    self.element = self.caster.game.assets_loader.loaded_recipes[self.element][other_spell.hand_position]
                    self.add_native_atributes()
            for key, value in other_spell.properties.items():
                self.add_property(key, value)
            return

    def multiply_all_properties(self, factor):
        number_violation = False
        for key in self.properties:
            self.properties[key] *= factor
            if self.properties[key] > self.ceil_values:
                self.properties[key] = self.ceil_values
                number_violation = True
        if number_violation:
            self.caster.messages.append(("Some spell properties reached maximum value of {}".format(self.ceil_values), 120))

        print("Multiplied spell properties:", self.properties)

    def add_property(self, property, value):
        if not (type(value) == int or type(value) == float):
            return
        if property not in self.properties:
            self.properties[property] = 0
        self.properties[property] += value
        if self.properties[property] > self.ceil_values:
            self.properties[property] = self.ceil_values
            self.caster.messages.append(("Spell property '{}' reached maximum value of {}".format(property, self.ceil_values), 120))

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
