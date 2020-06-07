function loadCommands() {
    fetch('./commands.json')
    .then (res => res.json())
    .then (out => {
        var links = "";
        var cmds = out;
        var total = ''
        var libs = ['Bot Help', 'Moderation', 'Utilities', 'Math', 'Fun', 'Games', 'Encoding', 'Memes', 'Images', 'Apps'];
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
                    var api = '<a href="'+cmds[i][libs[i]][num]['a'][0]+'">'+cmds[i][libs[i]][num]['a'][0]+'</a>';
                }
                if (cmds[i][libs[i]][num]['p'].length>0) {
                    var par = '<br>';
                    var subcount = 1;
                    for (k = 0; k < cmds[i][libs[i]][num]['p'].length; k++) {
                        var par = par+'<strong>'+subcount.toString()+'.</strong> '+cmds[i][libs[i]][num]['p'][k]+'<br>';
                        subcount++;
                    }
                }
                var name = cmds[i][libs[i]][num]['n'].toString();
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