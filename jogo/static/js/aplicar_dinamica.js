function aplicar_acao(acao) {
    $.ajax({
        url : "aplicar_acao/", // the endpoint
        type : "POST", // http method
        data : { acao : acao}, // data sent with the post request
        success : function(json) {
          console.log(json);
          button = document.getElementById("b_iniciar_jogo");
          button.disabled = true;
        },
        error : function(xhr,errmsg,err) {
          button = document.getElementById("b_iniciar_jogo");
          button.disabled = true;
        }
    });
};
