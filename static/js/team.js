const queryString = window.location.pathname;
const teamID = parseInt(queryString.substring(7));
console.log(window.location.href);

$(getTeams());

async function getTeams() {
  resp = await axios.get("/api/team", {
    params: {
      team_id: teamID,
    },
  });


  let FORMATION = resp.data.formation.replace(/-/g, "");
  let playerNum = 0;
  $("#team-page-roster").append(
    `<div class='movie-item-style-2'>
        <div class="team-roster">
        </div>
      </div>`
  );
  for (let j = FORMATION.length - 1; j >= 0; j--) {
    $(".team-roster").append(`<div id="row${j}" class="player-row"></div>`);
    let currRow = FORMATION.charAt(j);
    for (let rowLen = 0; rowLen < parseInt(currRow); rowLen++) {
      $(`#row${j}`).append(
        `<a class='player-img-link' href="../player/${resp.data.players[playerNum].id}">
            <p id='player-rating'><b>${resp.data.players[playerNum].rating}</b></p>
            <img src="../${resp.data.players[playerNum].image}" alt="">
        </a>`
      );
      playerNum++;
    }
  }
  $(`.team-roster`).append(`<div id="gk" class="player-row"></div>`);
  $(`#gk`).append(
    `<a class='player-img-link' href="../player/${resp.data.players[playerNum].id}">
        <p id='player-rating'><b>${resp.data.players[playerNum].rating}</b></p>
        <img src="../${resp.data.players[playerNum].image}" alt="">
    </a>`
  );

  for (let k = 0; k < Object.keys(resp.data.players).length; k++) {
    $(`#players`).append(
      `<a href="/player/${resp.data.players[k].id}">${resp.data.players[k].name}, </a>`
    );
  }
}
