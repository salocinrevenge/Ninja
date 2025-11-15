import pyray

class Controler():
    def __init__(self):
        self.key_map = {
            pyray.KEY_W: "W",
            pyray.KEY_A: "A",
            pyray.KEY_S: "S",
            pyray.KEY_D: "D",
            pyray.KEY_SPACE: "SPACE",
            pyray.KEY_LEFT_SHIFT: "SHIFT",
            pyray.KEY_F1: "F1",
            pyray.KEY_F3: "F3",
            pyray.KEY_F5: "F5",
            pyray.KEY_F11: "F11",
            pyray.MOUSE_BUTTON_LEFT: "LEFT_MOUSE",
            pyray.MOUSE_BUTTON_RIGHT: "RIGHT_MOUSE",
            pyray.KEY_ONE: "KEY_ONE",
            pyray.KEY_TWO: "KEY_TWO",
            pyray.KEY_THREE: "KEY_THREE",
            pyray.KEY_FOUR: "KEY_FOUR",
            pyray.KEY_FIVE: "KEY_FIVE",
            pyray.KEY_SIX: "KEY_SIX",
            pyray.KEY_SEVEN: "KEY_SEVEN",
            pyray.KEY_EIGHT: "KEY_EIGHT",
            pyray.KEY_NINE: "KEY_NINE",
            pyray.KEY_ZERO: "KEY_ZERO",
            pyray.MOUSE_BUTTON_MIDDLE: "MOUSE_WHEEL_DOWN",
            pyray.MOUSE_BUTTON_MIDDLE: "MOUSE_WHEEL_UP"
        }
        self.key_state = {value: False for value in self.key_map.values()}

        self.actions = []

    def get_controls(self):
        self.actions.clear()
        for key, value in self.key_map.items():
            is_pressed = pyray.is_key_down(key)
            is_pressed = pyray.is_mouse_button_down(key) if "MOUSE" in value else is_pressed
            if is_pressed != self.key_state[value]:
                self.key_state[value] = is_pressed
                if is_pressed:
                    self.actions.append(value + "_DOWN")
                else:
                    self.actions.append(value + "_UP")
        
        # Check mouse wheel movement
        wheel_move = pyray.get_mouse_wheel_move()
        if wheel_move > 0:
            self.actions.append("MOUSE_WHEEL_UP")
        elif wheel_move < 0:
            self.actions.append("MOUSE_WHEEL_DOWN")
            
        return self.actions
