function adiciona_modulo(nome){
  // Find a <table> element with id="myTable":
  var table = document.getElementById("my_table").getElementsByTagName('tbody')[0];
  // Create an empty <tr> element and add it to the 1st position of the table:
  var row = table.insertRow(-1);
  var input = document.getElementById("my_input");
  // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
  var cell1 = row.insertCell(-1);
  var cell2 = row.insertCell(-1);
  var cell3 = row.insertCell(-1);
    // Add some text to the new cells:
  cell1.innerHTML = "<div style = \"width: 175px\" align = \"center\">"+nome+"</div>";
  cell2.setAttribute("style", "text-align:right; margin:auto");
  cell2.innerHTML = "<div style = \"width: 140px\" align = \"center\"> <input style=\"width:100px; height:22px; font-size:10px \" type=\"number\" id=\"my_input\" class=\"form-control\" placeholder=\"\" value=\"1\" required></div>"
  cell3.setAttribute("style", "text-align:right; margin:auto");
  cell3.innerHTML = "<div style = \"margin-left: 25px\" align = \"left\"> <input type=\"checkbox\" align=\"center\"></div>"
}
