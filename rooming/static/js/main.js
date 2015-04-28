$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
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
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
function sendreq(room, data) {
    $("#roomInterface").show();
    $("#roomInterfaceRoom").text(room);
    $("#roomInterfaceResult").text("");
    $("#roomInterfaceAddField").val("");
    $("#roomInterfaceAddField").select();
    $("#roomInterfaceResidents").empty();
    for (var i = 0; i < data.residents.length; i++) {
        var kerb = data.residents[i];
        $("#roomInterfaceResidents").append('<li>' + kerb + ' <button type="button" onclick="removeresident(\'' + kerb + '\')">Remove</button></li>');
    }
}
function addResident() {
    var roomNum = $("#roomInterfaceRoom").text();
    var name = $("#roomInterfaceAddField").val();
    $("#roomInterfaceAddField").val("");
    $.post("update", 
        {
            roomnum: roomNum,
            name: name,
        },
    function(result) {
        $("#roomInterfaceResult").text(result);
	syncRoomingData();
	/*        result_obj = JSON.parse(result);*/
/*	if (obj.status == 0) {
	    alert("Success!" + obj.msg);
	} else {
	    alert("ERROR:" + obj.msg);
	}*/
    });
}
function removeresident(athena) {
    $.post("removeresident",
	   {
	       athena: athena
	   },
	   function(result) {
               $("#roomInterfaceResult").text(result);
	       syncRoomingData();
	   });
}
