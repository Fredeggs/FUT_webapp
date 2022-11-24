let playerList = [];
let playerRoster = {};
let rosterPosition;
var playersearchctc = $("#playersearch-content");
var overlay = $(".overlay");

$(displayTeam());

$("#formation").on("change", displayTeam);

$("#search").submit(function (e) {
  e.preventDefault();
  displayPlayers();
});

//pop up for player search form
$("body").on("click", ".empty-player-div", function (event) {
  event.preventDefault();
  playersearchctc.parents(overlay).addClass("openform");
  rosterPosition = $(event.target).parent().data("player");
  $(document).on("click", function (e) {
    var target = $(e.target);
    if ($(target).hasClass("overlay")) {
      $(target)
        .find(playersearchctc)
        .each(function () {
          $(this).removeClass("openform");
        });
      setTimeout(function () {
        $(target).removeClass("openform");
      }, 350);
    }
  });
});

function displayTeam() {
  $(".team-roster").empty();
  let FORMATION = $("#formation option:selected").text().replace(/-/g, "");
  let playerNum = 0;

  for (let i = FORMATION.length - 1; i >= 0; i--) {
    $(".team-roster").append(`<div id="row${i}" class="player-row"></div>`);
    let currRow = FORMATION.charAt(i);
    for (let rowLen = 0; rowLen < parseInt(currRow); rowLen++) {
      if (!playerRoster[playerNum]) {
        $(`#row${i}`).append(
          `<a href="#" data-player="${playerNum}" class="empty-player-div">
                      <img src="../static/images/add_circle_FILL0_wght400_GRAD0_opsz48.png" alt="">
                  </a>`
        );
        playerNum++;
      } else {
        $(`#row${i}`).append(
          `<a href="#" data-player="${playerNum}" class="player-img-link">
            <p id='player-rating'><b>${playerRoster[playerNum]["playerRating"]}</b></p>
            <img src="../${playerRoster[playerNum]["playerImg"]}" alt="">
          </a>`
        );
        playerNum++;
      }
    }
  }
  if (!playerRoster[playerNum]) {
    $(`.team-roster`).append(`<div id="gk" class="player-row"></div>`);
    $(`#gk`).append(
      `<a href="#" data-player="${playerNum}" class="empty-player-div">
              <img src="../static/images/add_circle_FILL0_wght400_GRAD0_opsz48.png" alt="">
          </a>`
    );
  } else {
    $(`.team-roster`).append(`<div id="gk" class="player-row"></div>`);
    $(`#gk`).append(
      `<a href="#" data-player="${playerNum}" class="player-img-link">
        <p id='player-rating'><b>${playerRoster[playerNum]["playerRating"]}</b></p>
        <img src="../${playerRoster[playerNum]["playerImg"]}" alt="">
      </a>`
    );
  }
}

async function getPlayerData() {
  let name = $("#search-name").val();

  let resp = await axios.get("/api/players", {
    params: {
      name: name,
    },
  });
  return resp.data;
}

async function displayPlayers() {
  $("#search-popup").empty();
  let playerList = await getPlayerData();
  filterPlayers(playerList);
}

function filterPlayers(players) {
  for (let i = 0; i < players.length; i++) {
    $("#search-popup").append(
      `<a class="player-listing" data-playerid=${players[i].id} data-playerimg=${players[i].image} data-playername='${players[i].name}' data-playerrating=${players[i].rating} href="#">
            <img id="listing-img" src='${players[i].image}' alt="">
            <p>${players[i].name}</p>
            <p>${players[i].rating}</p>
        </a>`
    );
  }
}

$("body").on("click", ".player-listing", function (event) {
  event.preventDefault();
  let target = $(event.target);
  let playerID = target.parent().data("playerid");
  let playerRating = target.parent().data("playerrating");
  let playerImg = target.parent().data("playerimg");
  let playerName = target.parent().data("playername");

  playerRoster[rosterPosition] = {
    playerID: playerID,
    playerName: playerName,
    playerRating: playerRating,
    playerImg: playerImg,
  };

  $(`a[data-player="${rosterPosition}"]`)
    .removeClass("empty-player-div")
    .addClass("player-img-link")
    .empty()
    .append(
      `<p id='player-rating'><b>${playerRating}</b></p>
      <img src="../${playerImg}" alt="">`
    );

  if (Object.keys(playerRoster).length === 11) {
    $("button").prop("disabled", false);
  }

  $(".openform").removeClass("openform");
});

$("body").on("click", "#create-team-btn", async function (event) {
  event.preventDefault();
  newTeamData = {
    name: $("#team-name").val(),
    formation: $("#formation").val(),
    rating: 37,
    players: playerRoster,
  };
  console.log(newTeamData);
  await axios.post("/api/create-team", { newTeamData });
  console.log("data sent!");
});
