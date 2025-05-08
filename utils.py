import json, os, base64

class Utils:
    @staticmethod
    def load_json(filename, default):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return default
        return default

    @staticmethod
    def save_json(filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def encrypt(data):
        return base64.b64encode(data.encode()).decode()

    @staticmethod
    def decrypt(data):
        return base64.b64decode(data.encode()).decode()
