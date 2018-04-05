function adiciona_time(){
  // Find a <table> element with id="myTable":
  var table = document.getElementById("my_table").getElementsByTagName('tbody')[0];
  // Create an empty <tr> element and add it to the 1st position of the table:
  var row = table.insertRow(-1);
  var input = document.getElementById("my_input");
  // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
  var cell1 = row.insertCell(-1);
  var cell2 = row.insertCell(-1);
    // Add some text to the new cells:
  cell1.innerHTML = input.value;
  cell2.setAttribute("style", "text-align:right");
  cell2.innerHTML = "<button onclick=\"remover_time(this)\" class=\"btn btn-default inline\">x</button>"
}

function remover_time(but){
  linha_selecionada = but.parentElement.parentElement.rowIndex;
  document.getElementById("my_table").deleteRow(linha_selecionada);
}
