const prm = new URLSearchParams(window.location.search);
const prefix = prm.has("prefix") ? prm.get("prefix") : "1"
function redirectTo(url) {
  window.location.href = `https://601.vierofernando.repl.co/${url}`;
}
function onClickCategoryButton(index, arrayInput) {
  if (isNaN(index)) return;
  document.getElementById("right").innerHTML = "";
  let elements = document.getElementsByClassName("categoryButton");
  for (let elementsIndex = 0; elementsIndex < elements.length; elementsIndex++) {
    elements[elementsIndex].style.backgroundColor = (elementsIndex == index) ? "red" : "#555";
  }
  arrayInput = arrayInput.split("NEWCMD");
  arrayInput.pop();
  for (let commandsIndex = 0; commandsIndex < arrayInput.length; commandsIndex++) {
    let func = arrayInput[commandsIndex].split(':');
    func.shift()
    document.getElementById("right").innerHTML += "<div class='commandDisplay'><cmdname>"+prefix+arrayInput[commandsIndex].split(':')[0]+"</cmdname><br><cmddesc>"+func.join(":").replace(",", ":")+"</cmddesc></div>";
  }
}
fetch("https://raw.githubusercontent.com/vierofernando/username601/master/assets/json/commands.json").then(res => res.json()).then(res => {
  for (let categoryIndex = 0; categoryIndex < res.length; categoryIndex++) {
    const categoryName = Object.keys(res[categoryIndex])[0];
    let dataString = new Array();
    let categoryCommands = "";
    for (let commandsIndex = 0; commandsIndex < res[categoryIndex][categoryName].length; commandsIndex++) {
      const command = res[categoryIndex][categoryName][commandsIndex];
      const string = command.n + ':'+ command.f.replace("\n", "<br>") + 'NEWCMD'
      categoryCommands += string;
      dataString.push(string);
    }
    const code = `<button onclick='onClickCategoryButton(${categoryIndex.toString()}, \"${categoryCommands}\")' class='categoryButton'>${categoryName}</button>`;
    document.getElementById("left").innerHTML += code;
  }
});