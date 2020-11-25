import requests

class BotCommands:
    def __init__(self, client):
        try:
            self.raw_data = requests.get("https://raw.githubusercontent.com/vierofernando/username601/master/assets/json/commands.json").json()
            self.categories = list(map(lambda i: list(i.keys())[0], self.raw_data))
            self.commands = []
            for i in range(len(self.categories)):
                for j in self.raw_data[i][self.categories[i]]:
                    self.commands.append({
                        "name": j["n"], "function": j["f"], "parameters": j["p"], "apis": j["a"], "category": self.categories[i], "type": "COMMAND"
                    })
            self.length = len(self.commands)
        except Exception as e:
            return print(f"error: please put config.ini file in the same directory\nand/or make sure commands.json is stored in <JSON_DIR key in config.ini file>.\n\nraw error message: {e}")
    
    def get_commands_from_category(self, category_name):
        category = list(filter(lambda x: x.lower().startswith(category_name) or category_name in x.lower(), self.categories))
        if category == []: return None
        return [i for i in self.commands if i['category'].lower() == category[0].lower()]
    
    def get_command_info(self, command_name):
        query = list(filter(lambda x: x["name"].lower().startswith(command_name) or command_name in x["name"].lower(), self.commands))
        if query == []: return None
        return query[0]
    
    def query(self, text):
        _temp, _full_total = [a for a in self.categories if a.lower().startswith(text) or text in a.lower()], []
        if _temp != []:
            for elem in _temp:
                _full_total.append({
                    "name": elem,
                    "type": "CATEGORY"
                })
        
        _res = list(filter(lambda x: x["name"].lower().startswith(text) or text in x["name"].lower(), self.commands))
        _full_total += _res
        if _full_total == []: return None
        return _full_total