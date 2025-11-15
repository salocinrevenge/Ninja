import pyray


class Inventario:
    def __init__(self,jogador):
        self.number_of_slots = 12
        self.hotbar = [None] * self.number_of_slots  # 12 slots na hotbar
        self.selected_slot = 0  # Slot selecionado inicialmente
        self.jogador = jogador
        self.assets_loader = jogador.game.assets_loader
        self.alpha_hotbar = 200  # Transparência da hotbar (0-255)

        # Posicoes de mao
        self.hand_positions = ["up", "down", "move", "stop", "expand", "condense", "divide", "unite", "invert", "double", None, None]

    def render(self):
        # Get screen dimensions
        screen_width = pyray.get_screen_width()
        screen_height = pyray.get_screen_height()
        
        # Calculate dimensions for hotbar (p% of screen height)
        p = 0.10
        hotbar_height = int(screen_height * p)
        slot_size = hotbar_height * 0.9  # Slots slightly smaller than hotbar height
        slot_spacing = slot_size * 1.1  # Small gap between slots
        initial_space = slot_spacing - slot_size
        hotbar_width = slot_spacing * self.number_of_slots + initial_space  # Width to accommodate n slots
        
        # Ensure hotbar fits screen width
        if hotbar_width > screen_width:
            scale_factor = screen_width / hotbar_width
            hotbar_width *= scale_factor
            hotbar_height *= scale_factor
            slot_size *= scale_factor
            slot_spacing *= scale_factor
            initial_space = slot_spacing - slot_size
        
        # Calculate center positions
        hotbar_x = (screen_width - hotbar_width) / 2
        hotbar_y = screen_height - hotbar_height - (hotbar_height * 0.1)  # Small gap from bottom
        
        # Draw hotbar background
        pyray.draw_rectangle_rounded(pyray.Rectangle(hotbar_x, hotbar_y, hotbar_width, hotbar_height), 0.1, 1, pyray.Color(200, 200, 200, self.alpha_hotbar))

        # Draw slots
        for i in range(self.number_of_slots):
            x = hotbar_x + (i * slot_spacing) + initial_space
            y = hotbar_y + (hotbar_height - slot_size) / 2  # Center slots vertically
            if i == self.selected_slot:
                size_selection = 6
                pyray.draw_rectangle_rounded(pyray.Rectangle(x - (size_selection + 2), y - (size_selection + 2), slot_size + 2 * (size_selection + 2), slot_size + 2 * (size_selection + 2)), 0.2, 1, pyray.Color(0, 0, 0, self.alpha_hotbar))
                pyray.draw_rectangle_rounded(pyray.Rectangle(x - size_selection, y - size_selection, slot_size + 2 * size_selection, slot_size + 2 * size_selection), 0.2, 1, pyray.Color(255, 255, 255, self.alpha_hotbar))
            pyray.draw_rectangle_rounded(pyray.Rectangle(x, y, slot_size, slot_size), 0.1, 1, pyray.Color(55, 55, 55, self.alpha_hotbar))
            
        if self.jogador.modo == 'chakra':
            self.draw_chakra_bar(hotbar_x, hotbar_y, hotbar_width, hotbar_height, slot_size, slot_spacing, initial_space)
        elif self.jogador.modo == 'mobilidade':
            self.draw_itens(hotbar_x, hotbar_y, hotbar_width, hotbar_height, slot_size, slot_spacing, initial_space)

    def get_selected_hand_position(self):
        if 0 <= self.selected_slot < len(self.hand_positions):
            return self.hand_positions[self.selected_slot]
        return None

    def draw_chakra_bar(self, hotbar_x, hotbar_y, hotbar_width, hotbar_height, slot_size, slot_spacing, initial_space):
        for i, hand_position in enumerate(self.hand_positions):
            if i < self.number_of_slots and hand_position is not None:
                x = hotbar_x + (i * slot_spacing) + initial_space
                y = hotbar_y + (hotbar_height - slot_size) / 2
                image_path = f"{self.assets_loader.hand_positions_path}{hand_position}.png"
                texture = self.assets_loader.get_texture(image_path)
                
                # Calculate scale to fit slot size while maintaining aspect ratio
                scale_x = slot_size / texture.width
                scale_y = slot_size / texture.height
                scale = min(scale_x, scale_y)
                
                # Calculate scaled dimensions
                scaled_width = texture.width * scale
                scaled_height = texture.height * scale
                
                # Draw texture centered in slot
                dest_rect = pyray.Rectangle(
                    x + (slot_size - scaled_width) / 2,
                    y + (slot_size - scaled_height) / 2,
                    scaled_width,
                    scaled_height
                )
                pyray.draw_texture_pro(
                    texture,
                    pyray.Rectangle(0, 0, texture.width, texture.height),
                    dest_rect,
                    pyray.Vector2(0, 0),
                    0,
                    pyray.WHITE
                )
            

    def draw_itens(self, hotbar_x, hotbar_y, hotbar_width, hotbar_height, slot_size, slot_spacing, initial_space):
        pass

    def input(self, event):
        match event:
            case 'KEY_ONE_DOWN':
                self.selected_slot = 0
            case 'KEY_TWO_DOWN':
                self.selected_slot = 1
            case 'KEY_THREE_DOWN':
                self.selected_slot = 2
            case 'KEY_FOUR_DOWN':
                self.selected_slot = 3
            case 'KEY_FIVE_DOWN':
                self.selected_slot = 4
            case 'KEY_SIX_DOWN':
                self.selected_slot = 5
            case 'KEY_SEVEN_DOWN':
                self.selected_slot = 6
            case 'KEY_EIGHT_DOWN':
                self.selected_slot = 7
            case 'KEY_NINE_DOWN':
                self.selected_slot = 8
            case 'KEY_ZERO_DOWN':
                self.selected_slot = 9
            case 'KEY_MINUS_DOWN':
                self.selected_slot = 10
            case 'KEY_EQUAL_DOWN':
                self.selected_slot = 11
            case 'MOUSE_WHEEL_UP':
                self.selected_slot = (self.selected_slot - 1) % self.number_of_slots
            case 'MOUSE_WHEEL_DOWN':
                self.selected_slot = (self.selected_slot + 1) % self.number_of_slots

    def update(self, dt):
        pass  # Implementar logica de atualizacao do inventario aqui