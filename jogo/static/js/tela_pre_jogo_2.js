/*
*  TODO
*  - Tratar input pra que seja só números (inteiros? depende da medida de tempo)
*  - Modificar e melhorar o trigger do menu de eventos. O ideal é que ao clicar em um
*  botão de evento em uma das rodadas faça ele ficar "selecionado" e depois ele perde
*  a seleção se:
*       1 - é escolhido um evento do menu, modificando o texto do evento daquela rodada ou
*       2 - o botão de evento é novamente clicado
*       3 - outro botão evento é clicado
*  Ocorrendo a transição de menus entre cada seleção (resize-up) e desseleção (resize-down). Aí no caso (3),
*  o botão atualmente "selecionado" seria "desselecionado" e o novo botão clicado "selecionado" de uma vez.
* */


// Variavel global bostinha, ela fede
var nro_de_rodadas = 1;

// essas daqui eu ja gosto mais um pouco
var quem_clicou; //usada para saber qual botao "Evento" foi clicado
// coloquei global por ser usada em duas funcoes, verificar se melhor jeito
var popup_eventos = document.getElementById("popup-eventos");

function adiciona_rodada(){
    // Find a <table> element with id="myTable":
    var table = document.getElementById("my_table").getElementsByTagName('tbody')[0];
    // Create an empty <tr> element and add it to the 1st position of the table:
    var row = table.insertRow(-1);
    var input = document.getElementById("my_input");
    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var cell1 = row.insertCell(-1);
    var cell2 = row.insertCell(-1);
    var cell3 = row.insertCell(-1);
    var cell4 = row.insertCell(-1);
    // Add some text to the new cells:
    cell1.innerHTML = nro_de_rodadas;
    cell2.innerHTML = input.value;
    cell3.innerHTML = "<button class=\"btn btn-secondary\" type=\"button\" onclick=\"seleciona_evento(this)\">Evento</button>";
    cell4.setAttribute("style", "text-align:right");
    cell4.innerHTML = "<button onclick=\"remover_rodada(this)\" class=\"btn btn-default inline\">x</button>"

    // oh ela de novo ai
    nro_de_rodadas++;
}

function remover_rodada(but){
    var linha_selecionada = but.parentElement.parentElement.rowIndex;
    document.getElementById("my_table").deleteRow(linha_selecionada);

    // chama a funcao frescurenta
    atualiza_id_rodada(linha_selecionada);

    // e aqui tbm
    nro_de_rodadas--;
}

/* Funcao frescurenta pra atualizar nro da rodada (id)
   caso seja excluida uma linha do meio da 'stack' de rodadas */
function atualiza_id_rodada(linha_selecionada){
    // o total de linhas conta <td> dos cabecalhos da tabela
    var total_linhas = (document.getElementById("my_table").rows.length);

    // percorre linhas acima e subtrai 1
    for(var i = linha_selecionada; i < total_linhas; i++) {
        var id_rodada = document.getElementById("my_table").rows[i].cells[0];
        id_rodada.innerHTML = id_rodada.innerHTML - 1;
    }
}

// Funcao para fazer o pop-up do menu de eventos.
function seleciona_evento(trigger) {

    // Qual botao evento foi clicado?
    quem_clicou = trigger;

    // Toogle da visibilidade do menu de eventos
    popup_eventos.style.display = popup_eventos.style.display === 'block' ? 'none' : 'block';
}

// Funcao para mudar texto do botao clicado
function atualiza_evento__rodada(trigger) {

    // Muda texto de acordo com item do menu de eventos selecionado
    quem_clicou.innerHTML = trigger.innerText;

    // Pop-out do menu de eventos
    popup_eventos.style.display = 'none';
}
