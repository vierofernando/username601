const prm = new URLSearchParams(window.location.search);
let message = "Inspect element huh? Nope! Go away! shoo!";

if (document.layers) {
	document.captureEvents(Event.MOUSEDOWN);
	document.onmousedown = function(e) {
		if (document.layers || document.getElementById && !document.all) {
			if (e.which==2 || e.which==3){
				alert(message);
				return false;
			}
		}
	}
} else if ((document.all)&&(!document.getElementById)){
	document.onmousedown = function() {
		if (event.button==2){
			alert(message);
			return false;
		}
	}
}

document.oncontextmenu = new Function("alert(message);return false")

function loadCommands() {
	const prefix = (prm.has('prefix')) ? prm.get('prefix') : '1';
    fetch('https://vierofernando.github.io/username601/assets/json/commands.json') // decided to use this because client kept giving me 404s
    .then (res => res.json())
    .then (out => {
        let links = "";
		let libs = ["Bot Help", "Moderation", "Economy", "Utilities", "Fun", "Games", "Encoding", "Memes", "Images", "Apps", "Owner"];
        let total = links;
        let totalcount = 0;
        let elementCounter = totalcount;
        for (i = 0; i < out.length; i++) {
            let categoryCounter = 0;
            total = total+'<div id="category'+elementCounter.toString()+'"><strong style="font-size:30px;">'+libs[i]+'</strong></div><br><br>';
            let count = 1;
            for (num = 0; num < out[i][libs[i]].length; num++) {
                let api = 'No API used.';
                let par = 'No parameters.';
                if (out[i][libs[i]][num]['a'].length>0) {
					for (n = 0; n < out[i][libs[i]][num]['a'].length; n++) {
						api = '<a href="'+out[i][libs[i]][num]['a'][n]+'">'+out[i][libs[i]][num]['a'][n]+'</a>';
					}
				}
                if (out[i][libs[i]][num]['p'].length>0) {
                    par = '<br>';
                    let subcount = 1;
                    for (k = 0; k < out[i][libs[i]][num]['p'].length; k++) {
                        par = par+'<strong>'+subcount.toString()+'.</strong> '+out[i][libs[i]][num]['p'][k].split(": ")[0]+': '+prefix+out[i][libs[i]][num]['p'][k].split(": ")[1]+'<br>';
                        subcount++;
                    }
                }
                let name = prefix+out[i][libs[i]][num]['n'].toString();
                let func = out[i][libs[i]][num]['f'];
                total = total+'<strong>'+count.toString()+'. '+name+'</strong><br><ul><li>Function: '+func+'</li><li>Parameters: '+par+'</li><li>APIs used: '+api+'</li></ul>';
                count++;
                totalcount++;
                categoryCounter++;
            }
            total = total.replace('<strong style="font-size:30px;">'+libs[i]+'</strong>', '<strong style="font-size:30px;">'+libs[i]+' ('+categoryCounter.toString()+')</strong>')
            links = links + '<button id="linkz" onclick="fastScroll('+elementCounter.toString()+');">'+libs[i]+'</button>   ';
            elementCounter++;
        }
        document.getElementById('all').innerHTML = total;
        document.getElementById('title').innerHTML = 'Username601 Commands ('+totalcount.toString()+')'
        document.getElementById('links').innerHTML = links;

        // load other stuff
        if (prm.has('category')) {
            let category = document.getElementById('category'+prm.get('category'));
            if (category==null) {
                document.write("<strong>ERROR 404</strong><br>Invalid parameters!");
            } else {
                fastScroll(prm.get('category'));
            }
        }
    });
}
function loadMySanity() {
	if (prm.has('credits')) {
		window.location.href = 'https://vierofernando.github.io/username601/modules/credits.txt';
	}
    // very true.
    fetch('https://vierofernando.github.io/username601/assets/json/webtitle.json') // decided to use this because client kept giving me 404s
    .then (res => res.json())
    .then (out => {
        let randomTitle = "Username601 | "+out[Math.floor(Math.random() * out.length)];
        window.document.title = randomTitle;
    });
}