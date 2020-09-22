"""
P.S: This python does NOT have anything to do with the BOT itself,
it's just to wrap your head around the commands.json chaos.

be sure to make every category name in lowercase. (case sensitive? maybe)
"""

import json
from configparser import ConfigParser

def __gcmd__(cmdn, commands):
    for i in commands:
        if cmdn.lower() in i["name"].lower():
            return i
    return None

class BotCommands:
    def __init__(self):
        try:
            config = ConfigParser()
            config.read("config.ini")
            self.json_path = config.get("bot", "JSON_DIR") + "/commands.json"
            del config
            self.raw_data = json.loads(open(self.json_path, "r").read())
            self.categories = [list(i.keys())[0] for i in self.raw_data]
            self.commands = []
            self._get_command = __gcmd__
            for i in range(len(self.categories)):
                for j in self.raw_data[i][self.categories[i]]:
                    self.commands.append({
                        "name": j["n"], "function": j["f"], "parameters": j["p"], "apis": j["a"], "category": self.categories[i]
                    })
        except Exception as e:
            return print(f"error: please put config.ini file in the same directory\nand/or make sure commands.json is stored in <JSON_DIR key in config.ini file>.\n\nraw error message: {e}")
    
    def get_command(self, command_name):
        """
        Gets a single command data.
        Parameters: command_name (string)
        Returns: a dict or None if not found.
        """
        return self._get_command(command_name, self.commands)
    
    def get_commands_from_category(self, category_name):
        """
        Get a list of command from category.
        Parameters: category_name (string)
        Returns: An list of dict of commands, or None if not found.
        """
        category = None
        for i in range(len(self.categories)):
            if category_name.lower() in self.categories[i].lower():
                category = self.categories[i].lower()
                break
        if category == None: return None
        return [i for i in self.commands if i['category'].lower() == category.lower()]
    
    def delete_command(self, command_name):
        """
        Deletes a command.
        Parameters: command_name (string)
        Returns: None
        Exceptions: FileNotFoundError if command not found
        """
        data = self._get_command(command_name, self.commands)
        if data == None: raise FileNotFoundError("Command not found")
        for i in range(len(self.commands)):
            if self.commands[i]['name'].lower() == data['name'].lower():
                del self.commands[i]
                break
    
    def add_command(self, name, function, parameters, apis, category_name):
        """
        Adds a command.
        Parameters: name (string), function (string), parameters (list), apis (list), category_name (string)
        Returns: None
        Exceptions: Exception if category_name doesn't exist

        WARNING: category_name is case sensitive
        """
        if category_name.lower() not in [i.lower() for i in self.categories]: raise Exception("Category name of %s does not exist" % category_name)
        self.commands.append({
            "name": name,
            "function": function,
            "parameters": parameters,
            "apis": apis,
            "category": category_name
        })
    
    def save(self):
        """
        Saves the data to the JSON file.

        Parameters: None
        Returns: None
        """
        total = [{i: []} for i in self.categories]
        index = 0
        for i in total:
            category_name = list(i.keys())[0]
            for j in self.commands:
                if j['category'] == category_name:
                    total[index][category_name].append({
                        'n': j['name'],
                        'f': j['function'],
                        'p': j['parameters'],
                        'a': j['apis']
                    })
                    del j
            index += 1
        editor = open(self.json_path, "w+")
        editor.write(json.dumps(total))
        editor.close()