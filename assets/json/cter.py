from requests import get
data = get('https://vierofernando.github.io/username601/assets/json/commands.json').json()

def getLength():
    count = 0
    for i in range(len(data)):
        l = data[i][list(data[i].keys())[0]]
        count += len(l)
    return count

print(getLength())