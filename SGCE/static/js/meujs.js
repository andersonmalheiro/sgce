function chamarModal(p) {
    document.getElementById('partida').value = p;    
    console.log(p,t);
};


// Envia dados do novo lance da partida
$(document).on('submit','#form', function(e){
    e.preventDefault();
    $.ajax({
        type:'POST',
        url: '/manager/campeonatos/criar_lance/',
        data:{
            jogador:$('#jogador').val(),
            partida:$('#partida').val(),            
            lance:$('#lance').val(),
            desc:$('#desc').val(),
            tempo:$('#tempo').val(),
            minuto:$('#minuto').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(){            
            $('#modalLance').modal('hide');                        
            $('#modalSuccess').modal('show');
        },
        error:function(){
            $('#modalLance').modal('hide');
            $('#modalDanger').modal('show');
        },
        fail:function(){
            $('#modalLance').modal('hide');
            $('#modalDanger').modal('show');
        },
    });
});

// Muda as opções no form de criação de campeonato
$(function() {
    $('#formato').change(function(){      
      if ($(this).val() == 'PC'){
        $('#q_gr').hide();  
        $('#q_grupos').val(1);
        $('#n_equipes').hide();
        $('#n_equipes').removeAttr('name');
        $('#n_equipes').removeAttr('required');
        $('#num_e').show();
        $('#n_eq').attr('required', true);
        $('#n_eq').attr('name', 'qtd_times');
      }else{
        $('#q_gr').show();  
        $('#q_grupos').attr('required', true);
        $('#n_equipes').show();
        $('#n_equipes').attr('required', 'true');
        $('#n_equipes').attr('name', 'qtd_times');
        $('#num_e').hide();
        $('#n_eq').removeAttr('required');
        $('#n_eq').removeAttr('name');
      }
    });
  });

// Esconde opções na tela de criação do campeonato
$(document).ready(function(){
    $('#q_gr').hide();
    $('#n_equipes').hide();
    $('#num_e').hide();
})

var contador = 0;

function conta(){
    contador++;
    document.write(contador);   
}

function reseta_conta(){
    contador = 0;
}