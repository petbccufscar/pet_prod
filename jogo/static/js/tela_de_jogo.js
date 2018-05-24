/* Atualizações em tempo real (Timer e Rodada) */
socket_rodada = new WebSocket("ws://" + window.location.host + "/rodada/");
var rodada_atual = 0;
socket_rodada.onmessage = function(e) {
    document.getElementById("t_rodada").innerHTML = e.data;
/*    rodada_atual += 1;
    s = document.getElementById("select");
    var option = document.createElement("option");
    option.text = rodada_atual;
    option.value = rodada_atual;
    x.add(option);*/
     location.reload();
}

socket_rodada = new WebSocket("ws://" + window.location.host + "/timer/");
socket_rodada.onmessage = function(e) {
    document.getElementById("t_timer").innerHTML = e.data;
}


socket_rodada.onopen = function() {
    socket_rodada.send("hello world");
}
// Call onopen directly if socket is already open
if (socket_rodada.readyState == WebSocket.OPEN) socket_rodada.onopen();

/* Areas e modulos */

function mudar_area_modulos(aba,classe){
   var anterior = document.querySelector(".area.ativo");
   var seletor_ant = document.querySelector(".subaba-ativa");
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
function mudar_aba(aba){
  aba_atual.style.display = "none";
  aba_atual = document.getElementById(aba);
  aba_atual.style.display = "flex";
}

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

function confirmacao(card){
  if(card.classList.contains("modal-card-modulo")){
    return;
  }

  card.classList.add("modal-card-modulo");
  var modal = document.getElementById("modalB");
  modal.style.display= "block";
  var confimar = document.createElement("button");
  var cancelar = document.createElement("button");
  confimar.innerHTML = "Confimar";
  cancelar.innerHTML = "Cancelar";
  card.appendChild(confimar);
  card.appendChild(cancelar);
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
          card.classList.remove("modal-card-modulo");

          card.removeChild(card.lastChild);
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
            //console.log(parseFloat(json));
            //console.log("coisos"+ caixa.innerHTML + json);
            animar_incremento(600,parseFloat(caixa.innerHTML),parseFloat(json), caixa);
            alert("Modulo comprado!");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //console.log("erro"); // provide a bit more info about the error to the console
            alert("Algo de errado não está certo!");
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
            atualizar_hospital();
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
            atualizar_hospital();

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //console.log("erro");
        }
    });
};

function busca_modulo(id_modulo_buscar, acao){
  $.ajax({
      url : "busca_modulo/",
      type : "POST",
      data : {modulo_id: id_modulo_buscar}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          //console.log("success");
          var modulo = JSON.parse(json)[0];
          abrir_informacoes_modulo(modulo, acao);
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });
}

function abrir_informacoes_modulo(modulo, acao){

  var modal = document.getElementById('modalModulo');

  var b_cmpr = document.getElementById("b_comprar");

  var close = document.getElementsByClassName("close")[0];

  var codigo = document.getElementById("codigo_modal_modulo");
  codigo.innerHTML = modulo.pk;

  var preco = document.getElementById("preco_modal_modulo");
  preco.innerHTML = modulo.fields.custo_de_aquisicao;

  var custo = document.getElementById("custo_modal_modulo");
  custo.innerHTML = modulo.fields.custo_mensal;

  var tratamento = document.getElementById("tratamento_modal_modulo");
  tratamento.innerHTML = modulo.fields.preco_do_tratamento;

  var capacidade = document.getElementById("capacidade_modal_modulo");
  capacidade.innerHTML = modulo.fields.capacidade;

  var conforto = document.getElementById("conforto_modal_modulo");
  conforto.innerHTML = ""
  for (i = 0; i < modulo.fields.conforto; i++)
  {
    conforto.innerHTML = "<i class=\"fa fa-heart\" style=\"font-size:25px;color:#ef4646\"></i>" + conforto.innerHTML;
  }

  var tecnologia = document.getElementById("tecnologia_modal_modulo");
  tecnologia.innerHTML = ""
  for (i = 0; i < modulo.fields.tecnologia; i++)
  {
    tecnologia.innerHTML = "<i class=\"fa fa-medkit\" style=\"font-size:25px;color:blue\"></i>" + tecnologia.innerHTML;
  }

  modal.style.display = "block";
  close.onclick = function() {
      modal.style.display = "none";
  }
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }

  switch(acao) {
    case "comprar_modulo":
        b_cmpr.innerHTML= "Comprar";
        b_cmpr.onclick = function() {
          //console.log("kay");
          comprar_modulo(modulo.pk);
          modal.style.display = "none"
        }
        break;
    case "vender_modulo":
          b_cmpr.innerHTML= "Vender";
          b_cmpr.onclick = function() {
          //console.log("kay");
          vender_modulo(modulo.pk);
          modal.style.display = "none"
        }
        break;
    default:
        ;
  }
}

function busca_medico(id_medico_buscar, acao){
  $.ajax({
      url : "busca_medico/",
      type : "POST",
      data : {medico_id: id_medico_buscar}, // data sent with the post request

      // handle a successful response
      success : function(json) {
          //console.log("success");
          var medico = JSON.parse(json)[0];
          abrir_informacoes_medico(medico, acao);
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });
}

function abrir_informacoes_medico(medico, acao){

  var modal = document.getElementById('modalMedico');

  var b_cmpr = document.getElementById("b_comprar_med");

  var close = document.getElementById("b_cancelar_med");

  var perfil = document.getElementById("perfil_modal_medico");
  perfil.innerHTML = medico.pk;

  var salario = document.getElementById("salario_modal_medico");
  salario.innerHTML = medico.fields.salario;

  var pontualidade = document.getElementById("pontualidade_modal_medico");
  pontualidade.innerHTML = ""
  for (i = 0; i < medico.fields.pontualidade; i++)
  {
    pontualidade.innerHTML = "<i class=\"far fa-clock\" style=\"font-size:25px;color:blue\"></i>" + pontualidade.innerHTML;
  }

  var expertise = document.getElementById("expertise_modal_medico");
  expertise.innerHTML = ""
  for (i = 0; i < medico.fields.expertise; i++)
  {
    expertise.innerHTML = "<i class=\"fas fa-graduation-cap\" style=\"font-size:25px\">" + expertise.innerHTML;
  }

  var atendimento = document.getElementById("atendimento_modal_medico");
  atendimento.innerHTML = ""
  for (i = 0; i < medico.fields.atendimento; i++)
  {
    atendimento.innerHTML = "<i class=\"fas fa-user-md\" style=\"font-size:25px;color:green\"></i>" + atendimento.innerHTML;
  }

  modal.style.display = "block";
  close.onclick = function() {
      modal.style.display = "none";
  }
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }

  switch(acao) {
    case "contratar_medico":
        b_cmpr.innerHTML= "Contratar";
        b_cmpr.onclick = function() {
          contratar_medico(medico.pk);
          modal.style.display = "none"
        }
        break;
    case "despedir_medico":
          b_cmpr.innerHTML= "Despedir";
          b_cmpr.onclick = function() {
          despedir_medico(medico.pk);
          modal.style.display = "none"
        }
        break;
    default:
        ;
  }
}

function atualizar_hospital(){
  $.ajax({
      url : "hospital/",
      type : "GET",
      success : function(data) {
        document.getElementById("hospit").innerHTML = data;
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

/* COISAS PRO GRÁFICO DE PIZZA */
/*
var ctx = document.getElementById("myPieChart");
//console.log(ctx);
var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["Capacidade Ociosa", "Capacidade Utilizada"],
        datasets: [{
            label: '# of Votes',
            data: [12, 19],
            backgroundColor: [
                'rgba(240, 128, 128, 1)',
                'rgba(0, 191, 255, 1)',
            ],
            borderColor: [
                'rgba(240, 128, 128, 1)',
                'rgba(0, 191, 255, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
  }
});
*/


/* COISAS PRO GRÁFICO DE COLUNAS */
function atualizar_graficos(r){
  $.ajax({
      url : "dados_graficos/",
      type : "POST",
      data : {rodada: r},
      success : function(data) {
        console.log(data);
        grafico_barra(data.labels, data.total_atendidos, data.procuraram_atendimento);
      },
      error : function(xhr,errmsg,err) {
          //console.log("erro");
      }
  });

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
}

/**
 * setup para protecao com token csrftoken
 **/

$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


});
