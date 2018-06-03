/**
 * Recebe numero como parametro e retorna string formatada com virgula
 * nas casas de milhares, milhoes e etc..
 **/
const numeroComVirgulas = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function AnimadorIncremento(duracao, v_ini, v_fim, elem){
  this.delta = 0;
  this.before;
  this.duracao = 0;
  this.elemento = elem;
  this.max = duracao;
  this.v_atual = v_ini;
  this.fim = v_fim;
  this.range = v_fim - v_ini;
  console.log(this.range);

  this.animacao = function f(timestamp) {  // Public Method
    if(this.before == null){
      this.before = timestamp;
      requestAnimationFrame(f.bind(this));
      return;
    }

    this.delta = timestamp - this.before;
    this.before = timestamp;
    this.duracao += this.delta;
    var x = (this.delta * this.range)/this.max;
    this.v_atual = this.v_atual + x;
    if(this.max <= this.duracao ){
      this.elemento.innerHTML = this.fim.toFixed(2)
      return;
    }else{
      this.elemento.innerHTML = this.v_atual.toFixed(2);

      requestAnimationFrame(f.bind(this));
    }
  };
}

/**
 * Executa animação de incremento no elemento 'elem' saindo do valor 'v_ini'
 * e terminando no valor 'v_fim' por 'duracao' ms
 **/
function animar_incremento(duracao, v_ini, v_fim, elem){
  var anim = new AnimadorIncremento(duracao, v_ini, v_fim, elem);
  requestAnimationFrame(anim.animacao.bind(anim));
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
