var passoAtual = 0;
var times = []; 

function mostraPasso(n) {
  var x = document.getElementsByClassName("passo");
  x[passoAtual].style.display = "none";
  x[n].style.display = "block";
  passoAtual = n;
}
