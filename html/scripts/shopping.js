
function render(state)
{
  var root = document.getElementById("root");
  root.innerHTML = "<div>";
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
