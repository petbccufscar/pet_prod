var passoAtual = 0;
mostraPasso(passoAtual)
var emprestimos = [];
var times = [];

function mostraPasso(n) {
  var x = document.getElementsByClassName("passo");
  x[n].style.display = "block";
  if (n == 0) {
    document.getElementById("voltBtn").style.display = "none";
  } else {
    document.getElementById("voltBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("proxBtn").innerHTML = "Finalizar";
  } else {
    document.getElementById("proxBtn").innerHTML = "Avançar";
  }
}

function avancarPasso(n){

  var x = document.getElementsByClassName("passo");
  if(passoAtual + n >= x.length){
      enviar_dados()
      return;
  }
  x[passoAtual].style.display = "none";
  passoAtual = passoAtual + n;
  mostraPasso(passoAtual);
}

function enviar_dados(){
  /**
  var xhr = new XMLHttpRequest();
  var url = "/irrelevante/";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  var data = {"times":times,
  "emprestimos":emprestimos};
  xhr.send(JSON.stringify(data));
  */
  var data = {"times":times,
              "emprestimos":emprestimos};
  post("/irrelevante/", {"js":JSON.stringify(data)})
}

function adiciona_emprestimo(){
  var table = document.getElementById("t_emprestimo").getElementsByTagName('tbody')[0];
  var row = table.insertRow(-1);
  var input = document.getElementById("in_emprestimo");
  var cell1 = row.insertCell(-1);
  var cell2 = row.insertCell(-1);
  emprestimos.push(input.value)
  cell1.innerHTML = input.value;
  cell2.setAttribute("style", "text-align:right");
  cell2.innerHTML = "<button onclick=\"remover_emprestimo(this)\" class=\"btn btn-default inline\">x</button>"
}

function remover_emprestimo(but){
  linha_selecionada = but.parentElement.parentElement.rowIndex;
  emprestimos.splice(linha_selecionada -1, 1)
  document.getElementById("t_emprestimo").deleteRow(linha_selecionada);
}

function adiciona_time(){
  var table = document.getElementById("t_times").getElementsByTagName('tbody')[0];
  var row = table.insertRow(-1);
  var input = document.getElementById("in_times");
  var cell1 = row.insertCell(-1);
  var cell2 = row.insertCell(-1);
  times.push(input.value)
  cell1.innerHTML = input.value;
  cell2.setAttribute("style", "text-align:right");
  cell2.innerHTML = "<button onclick=\"remover_time(this)\" class=\"btn btn-default inline\">x</button>"
}

function remover_time(but){
  linha_selecionada = but.parentElement.parentElement.rowIndex;
  times.splice(linha_selecionada - 2, 1)
  document.getElementById("t_times").deleteRow(linha_selecionada);
}

function post(path, params) {
    method ="post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);
    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }
    var inputElem = document.createElement('input');
    inputElem.type = 'hidden';
    inputElem.name = 'csrfmiddlewaretoken';
    inputElem.value = csrftoken;
    form.appendChild(inputElem);


    document.body.appendChild(form);
    form.submit();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
