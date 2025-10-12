from pyray import load_model, unload_model

class Assets_Loader():
    
    def __init__(self, game):
        self.game = game
        self.models_loaded = dict()

    def get_model(self,name):
        if name in self.models_loaded.keys():
            return self.models_loaded[name]
        self.models_loaded[name] = load_model(name.encode('utf-8'))
        return self.models_loaded[name]

    def clear_all(self):
        for key in self.models_loaded.keys():
            unload_model(self.models_loaded[key])
            self.models_loaded[key] = None

        self.models_loaded = None

