var data = null;

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



function hasMenu()
{
  var v = getCookie("menukey")
  return ((getCookie("menukey") != "no") && (getCookie("menukey") != ""));
}


function render(state)
{
  console.log(state);
  var root = document.getElementById("root");

  root.innerHTML = "";

  root.innerHTML += "<div>";

  root.innerHTML += "<label for=\"menukey\"><b>Menu Key:</b></label>";
  root.innerHTML += "<input id=\"menukey\" type=\"text\" placeholder=\"menu key\">";

  root.innerHTML += "<button onclick=\"loadMenu();\">Load Menu</button>";

  root.innerHTML += "</div>";

  if (!hasMenu()) {
    console.log("No \"menukey\" cookie.");
    return;
  }
  else {
    if (state == 0) {
      var req = new XMLHttpRequest();
      req.addEventListener("load", loadCallback);
      req.open("POST", "/shopping_api");
      req.send(JSON.stringify({menukey: getCookie("menukey")}))
    }
  }

  root.innerHTML += "<div>";
  root.innerHTML += "<button onclick=\"showMenu();\">Week's Menu</button> <span class=\"separator\">|</span>";
  root.innerHTML += "<button onclick=\"showList();\">Shopping List</button> <span class=\"separator\">|</span>";
  root.innerHTML += "<button onclick=\"showSortedList();\">Sorted List</button>";
  root.innerHTML += "</div>";
  root.innerHTML += "<br />";

  console.log(data);
  if (data != null) {
    for (var i = 0; i < data.menu.length; i++) {
      console.log(data.menu[i]);
      root.innerHTML += "<input type=\"text\" placeholder=\"meal\" id=\"meal_" + i + "\" value=\"" + data.menu[i] + "\"><button onclick=\"remItem("+i+");\">x</button><br />"
    }
  }

  if (state == 1) {
    root.innerHTML += "<div>";
    root.innerHTML += "<input type=\"text\" placeholder=\"meal\" id=\"meal\"><button onclick=\"addItem();\">+</button>"
    root.innerHTML += "</div>";
  }


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

function loadCallback()
{
  // "this" is the request object
  var rec = JSON.parse(this.responseText);

  if (rec.reply == "yes") {
    console.log("Menu is in database.");
    data = rec.data;
  }
  else {
    console.log("Menu is new." + rec.menukey);
    data = JSON.parse('{"menu": ["macaroni and cheese", "mince and potatoes", "pasta bake"], "shoppinglist": [], "sorted_list" : []}');
  }
  
  setCookie("menukey", rec.menukey, 0);
  render(1);
}

function loadMenu()
{
  var menu_key = document.getElementById("menukey").value;

  var req = new XMLHttpRequest();
  req.addEventListener("load", loadCallback);
  req.open("POST", "/shopping_list");
  req.send(JSON.stringify({menukey: menu_key}))
}

function addItem()
{
  var meal = document.getElementById("meal").value;
  data.menu.push(meal);
  render(1);
}

function remItem(i)
{
  data.menu.splice(i, 1);
  render(1);
}
