/* Atualizações em tempo real (Timer e Rodada) */
socket_rodada = new WebSocket("ws://" + window.location.host + "/rodada/");
var rodada_atual = 0;
socket_rodada.onmessage = function(e) {
    document.getElementById("t_rodada").innerHTML = e.data;
     location.reload();
}

socket_rodada = new WebSocket("ws://" + window.location.host + "/timer/");
socket_rodada.onmessage = function(e) {
    document.getElementById("t_timer").innerHTML = e.data;
}

socket_rodada = new WebSocket("ws://" + window.location.host + "/mercado/");
socket_rodada.onmessage = function(e) {
    msg = JSON.parse(e.data);
    var cards = undefined
    if(msg.tipo == "Modulo")
      cards = document.getElementsByClassName("modulo")
    else if(msg.tipo == "Medico")
      cards = document.getElementsByClassName("medico")

    for(var i = 0; i < cards.length; i++){
      if(cards[i].attributes["data-value"].value == msg.id){
        cards[i].querySelector(".qtd-disponiveis").innerHTML = msg.qtd;
        break;
      }
    }

}

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}


socket_rodada.onopen = function() {
    socket_rodada.send("hello world");
}
// Call onopen directly if socket is already open
if (socket_rodada.readyState == WebSocket.OPEN) socket_rodada.onopen();

/* Areas e modulos */

function mudar_area_modulos(aba, classe){
   var anterior = document.querySelector(".area.ativo");
   var seletor_ant = document.querySelector(".subaba-ativa");
   if(aba == null){
     aba = document.querySelector(".nav.modulos > li");
   }
   if(anterior!= null){
     anterior.classList.remove("ativo");
   }
   if(seletor_ant != null){
     seletor_ant.classList.remove("subaba-ativa");
   }
   document.querySelector(classe).classList.add("ativo");
   if(aba != null){
     aba.classList.add("subaba-ativa");
   }
}
/* Funções e variaveis para mudança de abas */
var aba_atual = document.getElementById("loja-medicos");
aba_atual.style.display = "flex";

function mudar_aba(aba, sec, subsec){
  if(sec != undefined){
    document.getElementById("h-sec").innerHTML=sec;
    document.getElementById("h-aba").innerHTML=subsec;
  }else{
    document.getElementById("h-sec").innerHTML='---';
    document.getElementById("h-aba").innerHTML='---';

  }
  aba_atual.style.display = "none";
  aba_atual = document.getElementById(aba);
  aba_atual.style.display = "flex";
}

function centralizar(){
    central  = document.querySelector(".central");
    console.log("dfdf");
    c = central.children[0].offsetWidth + 20;
    valor = (Math.floor(central.parentElement.offsetWidth/c)*c) + "px";
    central.style.maxWidth = "calc("+valor +" + 0.3em)" ;
    console.log((Math.floor(central.parentElement.offsetWidth/c)*c));
}
centralizar();

window.addEventListener('resize', function(){
  centralizar();
}, true);
mudar_aba('loja-modulos','Loja','Modulos');
mudar_area_modulos(null,'.area-Pediatria');

elements = document.querySelectorAll(('.nav.lateral > li'))
var l = elements.length;

for(var x = 0; x < l; x++){
  elements[x].addEventListener('mouseenter', function(){
    submenu = document.querySelector('li:hover .submenu');
    if(submenu != null){
      submenu.classList.add("submenu-ativo");
    }
  });

  elements[x].addEventListener('mouseleave', function(){
    submenu = document.querySelector('.submenu-ativo');
    console.log(submenu);
    if(submenu != null){
      submenu.classList.remove("submenu-ativo");
    }
  });

  elements[x].onclick = function(){
    close_this(elements[x]);
    submenu = document.querySelector('submenu-ativo');
    if(submenu != null){
      submenu.classList.remove("submenu-ativo");
    }
  };
}

function close_this(el){

}

function confirmacao(card, tipo){
  if(card.classList.contains("modal-card-" + tipo)){
    return;
  }

  card.classList.add("modal-card-" + tipo);
  var modal = document.getElementById("modalB");
  modal.style.display= "block";
  var div = document.createElement("div");
  div.classList.add("bottom");
  var confirmar = document.createElement("button");
  var cancelar = document.createElement("button");
  div.appendChild(confirmar);
  div.appendChild(cancelar);
  confirmar.innerHTML = "Confirmar";
  cancelar.innerHTML = "Cancelar";
  confirmar.classList.add("btn");
  cancelar.classList.add("btn");
  card.appendChild(div);

  window.onclick = function(event) {
      if (event.target == confirmar){
        modal.style.display = "none";
        card.classList.remove("modal-card-" + tipo);
        card.removeChild(card.lastChild);
        switch(tipo) {
          case "modulo":
              comprar_modulo(card.getAttribute('data-value'));
              break;
          case "medico":
              contratar_medico(card.getAttribute('data-value'))
              break;
          default:
              ;
        }
        }
      if (event.target == modal || event.target == cancelar) {
          modal.style.display = "none";
          card.classList.remove("modal-card-"+tipo);
          card.removeChild(card.lastChild);
      }
  }
}

function comprar_modulo(id) {
    //console.log("create post is working!") // sanity check
    $.ajax({
        url : "comprar_modulo/", // the endpoint
        type : "POST", // http method
        data : { modulo_id : id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
          //  $('#post-text').val(''); // remove the value from the input
            //console.log(json); // log the returned json to the console
            //console.log("success"); // another sanity check
            caixa = document.getElementById("t_caixa");
            toast("Modulo Comprado");
            //console.log(parseFloat(json));
            //console.log("coisos"+ caixa.innerHTML + json);
            animar_incremento(600,parseFloat(caixa.innerHTML),parseFloat(json), caixa);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            toast(xhr.responseText);
        }
    });
};

function vender_modulo(id) {
    $.ajax({
        url : "vender_modulo/",
        type : "POST",
        data : { modulo_id : id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            //console.log(json);
            caixa = document.getElementById("t_caixa");
            animar_incremento(800,parseFloat(caixa.innerHTML), parseFloat(json), caixa);
            //console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //console.log("erro");
        }
    });
};

function contratar_medico(id) {
    //console.log("create post is working!") // sanity check
    $.ajax({
        url : "contratar_medico/", // the endpoint
        type : "POST", // http method
        data : { medico_id : id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
          //  $('#post-text').val(''); // remove the value from the input
            //console.log(json); // log the returned json to the console
            //console.log("success"); // another sanity check
            toast("Medico Contratado");

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //console.log("erro"); // provide a bit more info about the error to the console
        }
    });
};

function despedir_medico(id) {
    $.ajax({
        url : "despedir_medico/",
        type : "POST",
        data : { medico_id :id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            //console.log(json);
            //console.log("success");

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //console.log("erro");
        }
    });
};

function abre_emprestimos(id_medico_buscar, acao){
  $.ajax({
      url : "abre_emprestimos/",
      type : "POST",
      data : {medico_id: id_medico_buscar}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          //console.log("success");
          var medico = JSON.parse(json)[0];
          abrir_informacoes_emprestimo();
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });
}

function abrir_informacoes_emprestimo(){
  var modal = document.getElementById("modalA");
  modal.style.display = "block";

  window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
  }
}

function atualizar_hospital_medicos(){
  $.ajax({
      url : "hospital/medicos/",
      type : "GET",
      success : function(data) {
        document.getElementById("hospital-medicos").innerHTML = data;
      },
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });
}

function atualizar_hospital_modulos(){
  $.ajax({
      url : "hospital/modulos/",
      type : "GET",
      success : function(data) {
        hosp_mod = document.getElementById("hospital-modulos");
        hosp_mod.innerHTML = data;
        area = hosp_mod.querySelector(".area");
        area.classList.add("ativo");
      },
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });
}

function atualizar_dashboard(){
  $.ajax({
      url : "dashboard/",
      type : "GET",
      success : function(data) {
        document.getElementById("dashboard").innerHTML = data;
        atualizar_graficos(0);
      },
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });
}

function onScroll(a){
  var b = document.getElementById("tf_head");
  var c = document.getElementById("tf_label");
  console.log(a.scrollLeft/a.scrollWidth)

  b.scrollLeft = a.scrollLeft;
  c.scrollTop = a.scrollTop;
}

/* COISAS PRO GRÁFICO DE COLUNAS */
function atualizar_graficos(r){
  $.ajax({
      url : "dados_graficos/",
      type : "POST",
      data : {rodada: r},
      success : function(json) {
        console.log(json);
        var chart = null;
        // pegando o grafico
        areas =  Object.keys(json.dados_graf_pizza)
        Chart.helpers.each(Chart.instances, function(instance){
          instance.atualizar(json);
        })
        if(chart == null){
          for(var i = 0; i < areas.length; i++){
            grafico_pizza(areas[i],
              json.dados_graf_pizza[areas[i]].total_atendidos,
              json.dados_graf_pizza[areas[i]].capacidade)
          }
          grafico_barra(json.labels, json.total_atendidos, json.procuraram_atendimento);
          return;
        }
      },
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });

}

function grafico_pizza(area, total_atendidos, capacidade){
  ctx = document.getElementById("chart-pie-"+area);
  options = {
				responsive: true,
				legend: {
					position: 'top',
				},
				title: {
					display: true,
					text: area
				},
				animation: {
					animateScale: true,
					animateRotate: true
				}
			}
  data = {
    datasets: [{
        data: [total_atendidos, capacidade - total_atendidos],
        backgroundColor: [
            'rgb(255, 99, 132)',
            "rgb(54, 162, 235)",
        ],
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
        'Total Utilizado',
        'Total Livre '
    ]
  };
  var myPieChart = new Chart(ctx,{
      type: 'pie',
      data: data,
      options: options
  });
  myPieChart.atualizar = function (json){
    data = {
      datasets: [{
          data: [json.dados_graf_pizza[area].total_atendidos,
          json.dados_graf_pizza[area].capacidade] - json.dados_graf_pizza[area].total_atendidos,
          backgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(54, 162, 235)",
          ],
      }],

      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: [
          'Total Utilizado',
          'Total Livre '
      ]
    };
    this.update()
  }.bind(myPieChart)
}

function grafico_barra(areas, total_atendidos, procuraram_atendimento){
  var ctx = document.getElementById("myBarChart");
  var data = {
      labels: areas,
      datasets: [
          {
              label: "Pacientes que procuraram o hospital",
              backgroundColor: "blue",
              data: procuraram_atendimento
          },
          {
              label: "Pacientes que foram atendidos",
              backgroundColor: "red",
              data: total_atendidos
          },

      ]
  };


  var myBarChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
          barValueSpacing: 20,
          scales: {
              yAxes: [{
                  ticks: {
                      min: 0,
                  }
              }]
          }
      }
  });
  myBarChart.atualizar = function (json){
    var data = {
        labels: json.labels,
        datasets: [
            {
                label: "Pacientes que procuraram o hospital",
                backgroundColor: "blue",
                data: json.procuraram_atendimento
            },
            {
                label: "Pacientes que foram atendidos",
                backgroundColor: "red",
                data: json.total_atendidos
            },

        ]
    };
    this.data = data;
    this.update()
  }.bind(myBarChart);
}

function toast(texto) {
    var x = document.createElement("div")
    document.body.appendChild(x)
    x.className = "toast show";
    x.innerHTML = texto
    setTimeout(function(){
      x.className = x.className.replace("show", "");
      setTimeout (function(){document.body.removeChild(x)},2500)
    }, 2000);
}
