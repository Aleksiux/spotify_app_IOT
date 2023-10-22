const playButton = document.getElementById('play');
const progressContainer = document.querySelector('.progress-container');
const progressBar = document.querySelector('.progress-bar');
const playPauseContainer = document.getElementById('play-pause-container');
const currentTimeDisplay = document.querySelector('.current-time');
document.getElementById("play").hidden = true;
document.getElementById("pause").hidden = false;




let isPlaying = false;
let startTime;
let pausedTime = parseInt(currentTimeDisplay.getAttribute('data-duration'));
let interval;
const duration = parseInt(progressBar.getAttribute('data-duration'));


function listenToSpotifyAPI() {
  fetch('listen_to_spotify_api')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      updatePlayerData(data);
      listenToSpotifyAPI();
    })
    .catch(error => {
      console.error('Error:', error);
      setTimeout(listenToSpotifyAPI, 5000); // Retry after 30 seconds
    });
}
listenToSpotifyAPI();

function updateProgress(currentTimeFromApi) {
  const currentTime = currentTimeFromApi
  const progressPercentage = (currentTime / duration) * 100;
  progressBar.style.width = `${progressPercentage}%`;

  if (currentTime >= duration) {
    clearInterval(interval);
    isPlaying = false;
    progressBar.style.width = '0%';
  }
}

function padZero(num) {
  return (num < 10 ? '0' : '') + num;
}
function nextTrack() {
    document.querySelector("#skip-form input[name='action']").value = "next_track";
    document.getElementById("skip-form").submit();
}
function prevTrack() {
    document.querySelector("#prev-form input[name='action']").value = "prev_track";
    document.getElementById("prev-form").submit();
}
function playTrack(){
    document.querySelector("#play-pause-form input[name='action']").value = "play_track";
    document.getElementById("play-pause-form").submit();
}
function pauseTrack(){
    document.querySelector("#play-pause-form input[name='action']").value = "pause_track";
    document.getElementById("play-pause-form").submit();
}
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function updatePlayerData(data) {
  document.querySelector('.track-name').textContent = data.track_name;
  document.querySelector('.track-artist').textContent = data.artist_name;
  document.querySelector('.current-time').textContent = data.progress_duration;
  const progressBar = document.querySelector('.progress-bar');
  progressBar.style.width = data.percentage + '%';
  document.querySelector('.total-duration').textContent = data.duration;
  const trackArtImage = document.querySelector('.track-art img');
  for (image of data.images){
    if (image.height == 300 && image.width == 300)
    {
        trackArtImage.src = image.url;
        }
  }
  if (data.is_currently_playing) {
  document.getElementById("pause").hidden = false;
  document.getElementById("play").hidden = true;
  }
  else{
  document.getElementById("play").hidden = false;
  document.getElementById("pause").hidden = true;
  }
}

function changeVolume(volume_data) {
    console.log('Volume Data:', volume_data);
    fetch('change_volume', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ volume_data: volume_data }),
    })
      .then(response => response.json())
      .then(data => {
      })
      .catch(error => {
        console.error('Error:', error);
      });
}
const volume = document.querySelector('#volume');
volume.addEventListener('change', function(){
    console.log(volume.value);
    changeVolume(volume.value);
})



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