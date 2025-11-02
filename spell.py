import pyray as rl
import copy

class Spell:
    def __init__(self, caster, body = None, subbody = None, element = None, hand_position = None, properties = None):
        self.caster = caster
        self.game = caster.game
        self.body = body
        self.subbody = subbody
        self.element = element
        self.hand_position = hand_position
        self.ceil_values = 1024
        self.alive = True
        self.pos = rl.Vector3(caster.pos.x, caster.pos.y+caster.casting_height, caster.pos.z)
        self.vel = rl.Vector3(0,0,0)
        if properties:
            self.properties = properties
        else:
            self.properties = dict()
            self.add_native_atributes()

    def render(self):
        # Render em 3D no mundo
        # Get color from properties, default to white if not present
        color = rl.Color(*self.game.assets_loader.elements_properities.get(self.element, 'None')["cor"],)
        rl.draw_sphere(self.pos, 0.1*self.properties.get("mass", 0.5), color)
        pass

    def update(self, dt):
        # Atualiza a posiçao do feitico no mundo
        self.pos = rl.Vector3(
            self.pos.x + self.vel.x * dt,
            self.pos.y + self.vel.y * dt,
            self.pos.z + self.vel.z * dt
        )
        # Verifica colisao com o mundo ou entidades
        # Se colidir, aplicar efeitos e definir self.alive = False
        pass

    def copy(self):
        return Spell(
            caster=self.caster,
            body=self.body,
            subbody=self.subbody,
            element=self.element,
            hand_position=self.hand_position,
            properties=copy.deepcopy(self.properties)
        )

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
        print("properties before merge:", self.properties, other_spell.properties)
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

    def cast(self):
        self.pos = rl.Vector3(self.caster.pos.x, self.caster.pos.y+self.caster.casting_height, self.caster.pos.z)
        self.vel = rl.vector3_normalize(self.caster.target_dir)
        self.vel = rl.vector3_scale(self.vel, self.properties.get("velocity", 0))
        if self.properties.get("mass", 0) > 0:
            self.caster.game.add_spell(self)

    def action(self, pilha_conjuracao):
        if self.element:
            self.cast()
            print("Casting spell with element:", self.element, "and properties:", self.properties)
            return
        # nao ha elemento, logo eh uma posicao de mao
        match self.hand_position:
            case "double":
                self.action_double(pilha_conjuracao)
                return
            case "invert":
                self.action_invert(pilha_conjuracao)
                return
            case "unite":
                self.action_unite(pilha_conjuracao)
                return

        # se nada ativou, mesclar com o ultimo feitico na pilha
        pilha_conjuracao[-1].merge(self)

        if pilha_conjuracao[-1].element:    # se o ultimo feitico agora eh um elemento, acaba a cadeia
            return
        new_spell = pilha_conjuracao.pop()  # senao, remove o ultimo feitico e ativa ele recursivamente
        new_spell.action(pilha_conjuracao)


    def action_double(self, pilha_conjuracao):
        if len(pilha_conjuracao) ==0:
            return
        if pilha_conjuracao[-1].element:    # e se o ultimo feitico for um elemento
            for _ in range(self.properties["multipling"] -1):   # duplica esse elemento
                pilha_conjuracao.append(pilha_conjuracao[-1].copy())
            return
        if pilha_conjuracao[-1].hand_position: # ja se for uma posicao de mao
            pilha_conjuracao[-1].multiply_all_properties(self.properties["multipling"]) # dobra as propriedades
            return

    def action_invert(self, pilha_conjuracao):
        if len(pilha_conjuracao) ==0:
            return
        pilha_conjuracao[-1].multiply_all_properties(-1)

    def action_unite(self, pilha_conjuracao):
        for spell in pilha_conjuracao:
            print(f"Spell properties: {spell.properties}")
        for _ in range(1,self.properties["uniting"]):
            if len(pilha_conjuracao) < 2:
                return
            if pilha_conjuracao[-1].element and pilha_conjuracao[-2].element:
                last_element = pilha_conjuracao.pop()
                pilha_conjuracao[-1].merge(last_element)