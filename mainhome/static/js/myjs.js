
const episodeList = document.querySelectorAll('.episode');
episodeList.forEach((episode) => {
  episode.addEventListener('click', (event) => {
    const videoSrc = event.target.dataset.src;
    const videoPlayer = document.querySelector('#the_frame');

    videoPlayer.setAttribute('src', videoSrc);
  });
});

const seasonsTab = document.querySelector('#season');
const overviewTab = document.querySelector('#overview');
const allSeasonsTitle = document.querySelector('#all-seasons');

allSeasonsTitle.addEventListener('click', () => {
  overviewTab.classList.remove('active');
  seasonsTab.classList.add('active');
});


