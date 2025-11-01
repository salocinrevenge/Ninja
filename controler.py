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
            pyray.KEY_F3: "F3",
            pyray.KEY_F5: "F5",
        }
        self.key_state = {value: False for value in self.key_map.values()}

        self.actions = []

    def get_controls(self):
        self.actions.clear()
        for key, value in self.key_map.items():
            is_pressed = pyray.is_key_down(key)
            if is_pressed != self.key_state[value]:
                self.key_state[value] = is_pressed
                if is_pressed:
                    self.actions.append(value + "_DOWN")
                else:
                    self.actions.append(value + "_UP")
        return self.actions
