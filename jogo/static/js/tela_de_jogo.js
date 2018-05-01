/* Atualizações em tempo real (Timer e Rodada) */
socket_rodada = new WebSocket("ws://" + window.location.host + "/rodada/");
socket_rodada.onmessage = function(e) {
    document.getElementById("t_rodada").innerHTML = e.data;
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


/* Funções e variaveis para mudança de abas */
var aba_atual = 0;
document.getElementsByClassName("aba")[0].style.display = "flex";

function mudar_aba(aba){
  var index = Array.prototype.indexOf.call(aba.parentElement.children, aba);
  var abas = document.getElementsByClassName("aba");
  console.log(abas[index].children[1])
  /* se mudar para aba do hospital .. atualiza */
  if(abas[index] == document.getElementById("hospit").parentElement){
    atualizar_hospital();
  }
  if(abas.length <= index)
    return;
  abas[aba_atual].style.display = "none";
  aba_atual = index;
  abas[aba_atual].style.display = "flex";
}

function comprar_modulo(id) {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "comprar_modulo/", // the endpoint
        type : "POST", // http method
        data : { modulo_id : id}, // data sent with the post request

        // handle a successful response
        success : function(json) {
          //  $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            alert("Modulo comprado!");

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("erro"); // provide a bit more info about the error to the console
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
            console.log(json);
            console.log("success");
            atualizar_hospital();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("erro");
        }
    });
};

function contratar_medico() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "contratar_medico/", // the endpoint
        type : "POST", // http method
        data : { medico_id : document.getElementById("medico_id").value}, // data sent with the post request

        // handle a successful response
        success : function(json) {
          //  $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("erro"); // provide a bit more info about the error to the console
        }
    });
};

function despedir_medico() {
    $.ajax({
        url : "despedir_medico/",
        type : "POST",
        data : { medico_id : document.getElementById("despedir_medico_id").value}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json);
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("erro");
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
          console.log("success");
          var modulo = JSON.parse(json)[0];
          abrir_informacoes_modulo(modulo, acao);
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log("erro");
      }
  });
}

function abrir_informacoes_modulo(modulo, acao){

  var modal = document.getElementById('modalModulo');

  var b_cmpr = document.getElementById("b_comprar");

  var close = document.getElementsByClassName("close")[0];

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
        b_cmpr.onclick = function() {
          console.log("kay");
          comprar_modulo(modulo.pk);
          modal.style.display = "none"
        }
        break;
    case "vender_modulo":
        b_cmpr.innerHTML= "Vender"
        b_cmpr.onclick = function() {
          console.log("kay");
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
          console.log("success");
          var medico = JSON.parse(json)[0];
          abrir_informacoes_medico(medico, acao);
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log("erro");
      }
  });
}

function abrir_informacoes_medico(medico, acao){

  var modal = document.getElementById('modalMedico');

  var b_cmpr = document.getElementById("b_comprar");

  var close = document.getElementsByClassName("close")[0];

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
        b_cmpr.onclick = function() {
          console.log("kay");
          contratar_medico(medico.pk);
          modal.style.display = "none"
        }
        break;
    case "despedir_medico":
        b_cmpr.innerHTML= "Despedir"
        b_cmpr.onclick = function() {
          console.log("kay");
          vender_modulo(medico.pk);
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
          console.log("erro");
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
