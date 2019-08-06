function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function setCookie(cname, cvalue, exdays) {

  var cstr = cname + "=" + cvalue + ";";

  if (exdays > 0) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
  }

  cstr += expires + ";";
  document.cookie = cstr;
}



function isLoggedIn()
{
  return getCookie("logged") == "in";
}


function render(state)
{
  var root = document.getElementById("root");

  root.innerHTML = "";

  if (!isLoggedIn()) {

    root.innerHTML += "<div>";
    root.innerHTML += "<form>";

    root.innerHTML += "<label for=\"uname\"><b>Username</b></label>";
    root.innerHTML += "<input id=\"uname\" type=\"text\" placeholder=\"Username\" name=\"uname\" required>";

    root.innerHTML += "<label for=\"psw\"><b>Password</b></label>";
    root.innerHTML += "<input id=\"psw\" type=\"password\" placeholder=\"Password\" name=\"psw\" required>";

    root.innerHTML += "<button type=\"submit\" onclick=\"login();\">Login</button>";

    root.innerHTML += "</form>";
    root.innerHTML += "</div>";

    return;

  }
  else {
    root.innerHTML += "<div>";
    root.innerHTML += "<form>";

    root.innerHTML += "<button type=\"submit\" onclick=\"logout();\">Logout</button>";

    root.innerHTML += "</form>";
    root.innerHTML += "</div>";
  }

  root.innerHTML += "<div>";
  root.innerHTML += "<button onclick=\"showMenu();\">Week's Menu</button> <span class=\"separator\">|</span>";
  root.innerHTML += "<button onclick=\"showList();\">Shopping List</button> <span class=\"separator\">|</span>";
  root.innerHTML += "<button onclick=\"showSortedList();\">Sorted List</button>";
  root.innerHTML += "</div>";

}

function showMenu()
{
  render(1);
}

function showList()
{
  render(2);
}

function showSortedList()
{
  render(3);
}

function loginCallback(repl)
{
  if (repl != "aye")
    return;
  
  setCookie("logged", "in", 7);
  render(1);
}

function login()
{
  var uname = document.getElementById("uname").value;
  var psw = document.getElementById("psw").value;

  console.log(uname);
  console.log(psw);

  // TODO XHR request to server to check credentials
  loginCallback("aye");
}

function logout()
{
  setCookie("logged", "out", 0);
  render(0);
}
