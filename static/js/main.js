$("p").on("click", function(){
   $("#form1").submit();
});

$(document).ready(function(){
    $("#form1").on("change", "input:checkbox", function(){
        $("#form1").submit();
    });
});

