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

  this.animacao = function f(timestamp) {  // Public Method
    if(this.before == null){
      this.before = timestamp;
      console.log(this.before);
      requestAnimationFrame(f.bind(this));
      return;
    }

    this.delta = timestamp - this.before;
    this.before = timestamp;
    this.duracao += this.delta;
    var x = (this.delta * this.range)/this.max;
    this.v_atual = this.v_atual + x;
    if(this.max <= this.duracao || Math.abs(this.v_atual) > Math.abs(this.fim)){
      this.elemento.innerHTML ="$ "+ numeroComVirgulas(this.fim.toFixed(2))
      return;
    }else{
      this.elemento.innerHTML ="$ "+ numeroComVirgulas(this.v_atual.toFixed(2));

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
