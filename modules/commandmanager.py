from json import loads
from discord import Embed, Color

class BotCommands:
    def __init__(self, client):
        self.client = client
    
    async def initiate(self):
        try:
            raw_data = await self.client.http._HTTPClient__session.get("https://raw.githubusercontent.com/vierofernando/username601/master/assets/json/commands.json")
            raw_data = await raw_data.text()
            self.raw_data = loads(raw_data)
            self.categories = list(map(lambda i: list(i.keys())[0], self.raw_data))
            self.categories = self.categories[:-1]
            self.commands = []
            for i in range(len(self.categories)):
                for j in self.raw_data[i][self.categories[i]]:
                    self.commands.append({
                        "name": j["n"], "function": j["f"], "parameters": j["p"], "apis": j["a"], "category": self.categories[i], "type": "COMMAND"
                    })
            self.length = len(self.commands)
        except Exception as e:
            return print(f"error: please put config.ini file in the same directory\nand/or make sure commands.json is stored in <JSON_DIR key in config.ini file>.\n\nraw error message: {e}")
    
    async def invalid_args(self, ctx, name = None):
        name = name if name else ctx.command.name
        command_info = [i for i in self.commands if i["name"] == name][0]
        embed = Embed(title="Invalid arguments", color=Color.red())
        embed.add_field(name="Description", value=command_info["function"], inline=False)
        embed.add_field(name="Usage", value="```"+"\n".join([i.split(": ")[1] for i in command_info["parameters"]])+"```", inline=False)
        
        if ctx.command.aliases:
            embed.add_field(name="Command Aliases", value=", ".join([f'`{i}`' for i in ctx.command.aliases]), inline=False)
        await ctx.send(embed=embed)
        del command_info, embed
    
    def get_commands_from_category(self, category_name):
        category = list(filter(lambda x: x.lower().startswith(category_name) or category_name in x.lower(), self.categories))
        if not category: return
        return [i for i in self.commands if i['category'].lower() == category[0].lower()]
    
    def get_command_info(self, command_name):
        query = list(filter(lambda x: x["name"].lower().startswith(command_name) or command_name in x["name"].lower(), self.commands))
        if not query: return
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
        if not _full_total: return
        return _full_total