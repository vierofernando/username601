/*

WARNING: THE CURRENT CODE IS NOT THE FINISHED PRODUCT.

DASHBOARD FOR USERNAME601 IS STILL NOT MEANT TO BE PUBLIC YET.

*/

var oauth_url = "https://discord.com/api/oauth2/authorize?client_id=764755177583411210&redirect_uri=https%3A%2F%2F601.vierofernando.repl.co%2Fauth-callback&response_type=token&scope=guilds%20identify";

if (!window.localStorage.code) window.location.href = oauth_url;
const currentTime = Math.round(new Date().getTime() / 1000);
if ((currentTime - parseInt(window.localStorage.registertime)) > 604800) {
  window.location.href = oauth_url;
}
try {
  fetch("https://cors-anywhere.herokuapp.com/https://discord.com/api/users/@me/guilds", {headers: {authorization: window.localStorage.code}}).then(res => res.json()).then(res => {
    console.assert(res[0]);
    let ids = new Array();
    res.forEach(guild => {
      ids.push(guild.id);
    });
    fetch("https://cors-anywhere.herokuapp.com/https://useless-api.vierofernando.repl.co/601/dashboard/sort_dashboard_guilds", {headers: {serverids: ids.join(",")}}).then(out => out.json()).then(out => {
      console.log(out);
      out.forEach(guild => {
        document.getElementById("guilds").innerHTML += JSON.stringify(guild);
      });
    });
  });
} catch { window.location.href = oauth_url; }