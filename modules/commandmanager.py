from .username601 import cfg
import requests
def __gcmd__(cmdn, commands):
    for i in commands:
        if cmdn.lower() in i["name"].lower():
            return i
    return None
def __command_type__(param, commands, categories):
    name = __gcmd__(param, commands)
    if name==None:
        if param.lower() in [i.lower() for i in categories]:
            return "category"
        return None
    else: return "command"

class BotCommands:
    def __init__(self):
        try:
            self.raw_data = requests.get(config('WEBSITE_MAIN')+"/assets/json/commands.json").json()
            self.categories = [list(i.keys())[0] for i in self.raw_data]
            self.commands = []
            self._get_command = __gcmd__
            self._get_type = __command_type__
            for i in range(len(self.categories)):
                for j in self.raw_data[i][self.categories[i]]:
                    self.commands.append({
                        "name": j["n"], "function": j["f"], "parameters": j["p"], "apis": j["a"], "category": self.categories[i]
                    })
            self.length = len(self.commands)
        except Exception as e:
            return print(f"error: please put config.ini file in the same directory\nand/or make sure commands.json is stored in <JSON_DIR key in config.ini file>.\n\nraw error message: {e}")
    def get_command(self, command_name):
        return self._get_command(command_name, self.commands)
    def get_commands_from_category(self, category_name):
        category = None
        for i in range(len(self.categories)):
            if category_name.lower() in self.categories[i].lower():
                category = self.categories[i].lower()
                break
        if category == None: return None
        return [i for i in self.commands if i['category'].lower() == category.lower()]
    def get_commands_auto(self, parameter):
        command_type = self._get_type(parameter, self.commands, self.categories)
        if command_type == None: return None
        if command_type == "command": return self._get_command(parameter, self.commands)
        return self.get_commands_from_category(parameter)