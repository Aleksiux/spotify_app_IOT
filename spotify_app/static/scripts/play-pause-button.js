// Last item is last song was played
const lastItem = [];
var buttons = document.querySelectorAll(".fa.fa-play.playing-button");
buttons.forEach(function(button) {
  button.addEventListener("click", function() {
    var song_uri = this.getAttribute("data-value");
    var data = {
      selected_song: song_uri
    };
    var csrfToken = getCookie('csrftoken');
    if (button.classList.contains("fa-play")) {
        buttons.forEach(function(button) {
            button.classList.remove('fa-pause');
            button.classList.add("fa-play");
        });
        button.classList.remove("fa-play");
        button.classList.add("fa-pause");
            fetch("play_selection", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
              },
              body: JSON.stringify(data),
            })
            .then(response => response.json())
            .catch(error => {
              console.error("Error:", error);
            });
    }
    else if (button.classList.contains("fa-pause")){
        button.classList.remove("fa-pause");
        button.classList.add("fa-play");
    }
    else {
        button.classList.add(".fa.fa-play");
    }
  });
});




function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}