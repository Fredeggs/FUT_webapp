let playerList = [];

$(document).ready(function () {
  displayPlayers();
});

$("#sort-by").change(function () {
  displayPlayers();
});

$("#search").submit(function (e) {
  e.preventDefault();
  displayPlayers();
});

async function getPlayerData() {
  let name = $("#search-name").val();

  let resp = await axios.get("/api/players", {
    params: {
      name: name,
    },
  });
  return resp.data;
}

function filterPlayers(players) {
  let sort = $("#sort-by").val();
  switch (sort) {
    case "rating":
      players.sort((a, b) => (a.rating > b.rating ? -1 : 1));
      break;
    case "price":
      players.sort((a, b) => (a.rating > b.rating ? -1 : 1));
      break;
    case "nationality":
      players.sort((a, b) => (a.nation > b.nation ? 1 : -1));
      break;
  }
  for (let i = 0; i < players.length; i++) {
    $(".flex-wrap-movielist").append(
      `<div class="movie-item-style-2 movie-item-style-1">
          <img src='${players[i].image}' alt="">
          <div class="hvr-inner">
            <a href="/player/${players[i].id}"> Player Page <i class="ion-android-arrow-dropright"></i> </a>
          </div>
          <div class="mv-item-infor">
            <h6><a href="#">${players[i].name}</a></h6>
            <p class="rate">Rating: <span>${players[i].rating}</span></p>
          </div>
        </div>`
    );
  }
}

async function displayPlayers() {
  $(".movie-item-style-2").remove();
  let playerList = await getPlayerData();
  filterPlayers(playerList);
}
