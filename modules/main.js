const prm = new URLSearchParams(window.location.search);

function loadCommands() {
	if (!prm.has('prefix')) {
		var prefix = '1';
	} else {
		var prefix = prm.get('prefix').toString();
	}
    fetch('https://vierofernando.github.io/username601/assets/json/commands.json') // decided to use this because client kept giving me 404s
    .then (res => res.json())
    .then (out => {
        var links = "";
		var libs = ["Bot Help", "Moderation", "Utilities", "Math", "Fun", "Games", "Encoding", "Memes", "Images", "Apps", "Owner"];
        var cmds = out;
        var total = ''
        var totalcount = 0;
        var elementCounter = 0;
        for (i = 0; i < cmds.length; i++) {
            var categoryCounter = 0;
            var total = total+'<div id="category'+elementCounter.toString()+'"><strong style="font-size:30px;">'+libs[i]+'</strong></div><br><br>';
            var count = 1;
            for (num = 0; num < cmds[i][libs[i]].length; num++) {
                var api = 'No API used.';
                var par = 'No parameters.';
                if (cmds[i][libs[i]][num]['a'].length>0) {
					for (n = 0; n < cmds[i][libs[i]][num]['a'].length; n++) {
						var api = '<a href="'+cmds[i][libs[i]][num]['a'][n]+'">'+cmds[i][libs[i]][num]['a'][n]+'</a>';
					}
				}
                if (cmds[i][libs[i]][num]['p'].length>0) {
                    var par = '<br>';
                    var subcount = 1;
                    for (k = 0; k < cmds[i][libs[i]][num]['p'].length; k++) {
                        var par = par+'<strong>'+subcount.toString()+'.</strong> '+cmds[i][libs[i]][num]['p'][k].split(": ")[0]+': '+prefix+cmds[i][libs[i]][num]['p'][k].split(": ")[1]+'<br>';
                        subcount++;
                    }
                }
                var name = prefix+cmds[i][libs[i]][num]['n'].toString();
                var func = cmds[i][libs[i]][num]['f'];
                var total = total+'<strong>'+count.toString()+'. '+name+'</strong><br><ul><li>Function: '+func+'</li><li>Parameters: '+par+'</li><li>APIs used: '+api+'</li></ul>';
                count++;
                totalcount++;
                categoryCounter++;
            }
            var total = total.replace('<strong style="font-size:30px;">'+libs[i]+'</strong>', '<strong style="font-size:30px;">'+libs[i]+' ('+categoryCounter.toString()+')</strong>')
            var links = links + '<button id="linkz" onclick="fastScroll('+elementCounter.toString()+');">'+libs[i]+'</button>   ';
            elementCounter++;
        }
        document.getElementById('all').innerHTML = total;
        document.getElementById('title').innerHTML = 'Username601 Commands ('+totalcount.toString()+')'
        document.getElementById('links').innerHTML = links;
    })
}
function loadMySanity() {
    fetch('https://vierofernando.github.io/username601/assets/json/webtitle.json') // decided to use this because client kept giving me 404s
    .then (res => res.json())
    .then (out => {
        var randomTitle = out[Math.floor(Math.random() * out.length)];
        window.document.title = randomTitle;
    });
    while (true) {
        if (document.getElementById('thebotsname').value!='Username601') {
            alert("DO NOT CHANGE MY NAME!");
        }
    }
}