function main() {
  const code = 'function Oopsies() {\n\treturn "You reached the end of the tunnel. Now go away.";\n}\n\nif (error.statusCode == 404) {\n\tconst text = Oopsies();\n}\n\nwindow.alert(text);X';
  function typeCode(i) {
    setTimeout(function() {
      let end = false;
      switch (code[i]) {
        case "\n":
          document.getElementById('code').innerHTML += "<br>"; 
          break;
        case "\t":
          document.getElementById('code').innerHTML += "‏‏‎ ‎".repeat(4);
          break;
        case "X":
          end = true;
          break;
        default:
          document.getElementById('code').innerHTML += code[i];
          break;
      }
      if (end) {
        setTimeout(function() {
          window.alert("You reached the end of the tunnel. Now go away.");
        }, 1000);
      }
    }, i * 50);
  }
  for (let i = 0; i < code.length; i++) {
    typeCode(i);
  }
}

main();
delete main;