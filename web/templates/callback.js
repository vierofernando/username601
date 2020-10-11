var oauth_url = "https://discord.com/api/oauth2/authorize?client_id=764755177583411210&redirect_uri=https%3A%2F%2F601.vierofernando.repl.co%2Fauth-callback&response_type=token&scope=guilds%20identify";
if (window.localStorage.registertime) {
  const timestampThen = parseInt(window.localStorage.registertime);
  const timestampNow = Math.round(new Date().getTime() / 1000);
  if ((timestampNow - timestampThen) > 604800) { window.location.href = oauth_url; }
  if (window.localStorage.code) {
    window.location.href = "https://601.vierofernando.repl.co/dashboard";
  }
}
const code = window.location.hash.split("token_type=")[1].split("&")[0] + ' ' + window.location.hash.split("access_token=")[1].split("&")[0];
if (!code) window.location.href = oauth_url;
try {
  fetch("https://cors-anywhere.herokuapp.com/https://discord.com/api/users/@me", {headers: {'authorization': code, 'Content-Type': 'application/json'}}).then(res => res.json()).then(res => {
    window.location.hash = "";
    if (!res[0]) window.location.href = oauth_url;
    window.localStorage.code = code;
    window.localStorage.registertime = Math.round(new Date().getTime() / 1000);
  });
  window.location.href = "https://601.vierofernando.repl.co/dashboard";
} catch { window.location.href = oauth_url; }
code = undefined;