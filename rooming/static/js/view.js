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


var roomData = null;

$(document).ready(function(){
    
    // The JSON (simplejson) Django repsonse looks like:
    // {"lat": "23.5017777778", "alt": " 371405.03125", "lon": " 92.0223333333"}
    $.getJSON("data",
              function(data) {
                  roomData = data;
		  updateRooms();
              });
});

function updateRooms() {
    for(roomnum in roomData) {
	if(roomData[roomnum].room.status == 1) {
	    rm = document.getElementById(roomnum)
	    if(rm == null) {
		alert("NUll room"+roomnum);
	    } else {
		rm.style.fill="#777777";
	    }
	} else if (roomData[roomnum].room.status == 2) {
	    rm = document.getElementById(roomnum)
	    if(rm == null) {
		alert("NUll room"+roomnum);
	    } else {
		rm.style.fill="#B20000";
	    }
	} else if (roomData[roomnum].room.status == 3) {
	    rm = document.getElementById(roomnum)
	    if(rm == null) {
		alert("NUll room"+roomnum);
	    } else {
		// Pink Alert!
		rm.style.fill="#FF3399";
	    }
	}
    }
    dt = new Date();
    document.getElementById('loading').innerHTML = "Rooming Status as of "+dt.toLocaleTimeString()+":";
}




