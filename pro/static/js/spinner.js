jQuery(function($){
    $(document).ajaxSend(function(){
  
      $("spinner-border").fadeIn(500);
  
    var loading = `<div class="spinner-border spinner-border-sm"></div>&nbsp;&nbsp; please wait...`
    $("#btn-sent").html(loading);
  
    });
    
    $("#btn-sent").click(function(){
      $.ajax({
        type:'POST',
        success: function(data){
          console.log(data);
        }
      }).done(function(){
        setTimeout(function(){
          $(".spinner-border").fadeOut(500);
        },700);
      });
    });
  });