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
function sendreq(room) {
    var name = prompt("Name of person to add:")
    $.post("update", 
        {
            roomnum: room,
            name: name,
        },
    function(result) {
	alert(result)
/*        result_obj = JSON.parse(result);*/
/*	if (obj.status == 0) {
	    alert("Success!" + obj.msg);
	} else {
	    alert("ERROR:" + obj.msg);
	}*/
	location.reload();
    });
}
function removeresident(athena) {
    $.post("removeresident",
	   {
	       athena: athena
	   },
	   function(result) {
	       alert(result);
	       location.reload();
	   });
}
