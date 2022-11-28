const queryString = window.location.pathname;
const userID = parseInt(queryString.substring(7));

$(getTeams());

async function getTeams() {
  let sort = $("#sort-by").val();

  resp = await axios.get(`/api/users/${userID}`, {
    params: {
      sort: sort,
    },
  });

  $("#teams-created").empty();

  for (let i = 0; i < resp.data.user_teams.length; i++) {
    let FORMATION = resp.data.user_teams[i].team.formation.replace(/-/g, "");
    let playerNum = 0;
    $("#teams-created").append(
      `<div class='movie-item-style-2'>
        <div id="created-${i}" class="team-thumbnail">
        </div>
        <div id='team-info' class='mv-item-infor'>
          <h6><a href="/teams/${resp.data.user_teams[i].team.id}"> ${resp.data.user_teams[i].team.name}</a></h6>
          <p class="rate">Team Rating: <span>${resp.data.user_teams[i].team.rating}</span></p>
          <p class="run-time"> Formation: ${resp.data.user_teams[i].team.formation}
          <p>Price: ${resp.data.user_teams[i].team.price}</p>
          <p id='created-players${i}'>Players: </p>
          <p>Likes: ${resp.data.user_teams[i].likes}</p>
          <p>Last Edited: ${resp.data.user_teams[i].team.timestamp} </p>
        </div>
      </div>`
    );
    for (let j = FORMATION.length - 1; j >= 0; j--) {
      $(`#created-${i}`).append(
        `<div id="created-${i}row${j}" class="player-row"></div>`
      );
      let currRow = FORMATION.charAt(j);
      for (let rowLen = 0; rowLen < parseInt(currRow); rowLen++) {
        $(`#created-${i}row${j}`).append(
          `<img src="../${resp.data.user_teams[i].team.players[playerNum].image}" alt="">`
        );
        playerNum++;
      }
    }
    $(`#created-${i}`).append(
      `<div id="created-${i}gk" class="player-row"></div>`
    );
    $(`#created-${i}gk`).append(
      `<img src="../${resp.data.user_teams[i].team.players[playerNum].image}" alt="">`
    );

    for (
      let k = 0;
      k < Object.keys(resp.data.user_teams[i].team.players).length;
      k++
    ) {
      $(`#created-players${i}`).append(
        `<a href="/player/${resp.data.user_teams[i].team.players[k].id}">${resp.data.user_teams[i].team.players[k].name}, </a>`
      );
    }
  }

  $("#teams-created").append(`
    <div id='pagination'class="topbar-filter">
      <label>Teams per page:</label>
      <select>
        <option value="range">5 Teams</option>
        <option value="saab">10 Teams</option>
      </select>
      <div class="pagination2">
        <span>Page 1 of 2:</span>
        <a class="active" href="#">1</a>
        <a href="#">2</a>
        <a href="#"><i class="ion-arrow-right-b"></i></a>
      </div>
    </div>
  `);

  $("#teams-liked").empty();

  for (let i = 0; i < resp.data.liked_teams.length; i++) {
    let FORMATION = resp.data.liked_teams[i].team.formation.replace(/-/g, "");
    let playerNum = 0;
    $("#teams-liked").append(
      `<div class='movie-item-style-2'>
        <div id="liked-${i}" class="team-thumbnail">
        </div>
        <div id='team-info' class='mv-item-infor'>
          <h6><a href="/teams/${resp.data.liked_teams[i].team.id}"> ${resp.data.liked_teams[i].team.name}</a></h6>
          <p class="rate">Team Rating: <span>${resp.data.liked_teams[i].team.rating}</span></p>
          <p class="run-time"> Formation: ${resp.data.liked_teams[i].team.formation}
          <p>Price: ${resp.data.liked_teams[i].team.price}</p>
          <p id='liked-players${i}'>Players: </p>
          <p>Likes: ${resp.data.liked_teams[i].likes}</p>
          <p>Last Edited: ${resp.data.liked_teams[i].team.timestamp} </p>
        </div>
      </div>`
    );
    for (let j = FORMATION.length - 1; j >= 0; j--) {
      $(`#liked-${i}`).append(
        `<div id="liked-${i}row${j}" class="player-row"></div>`
      );
      let currRow = FORMATION.charAt(j);
      for (let rowLen = 0; rowLen < parseInt(currRow); rowLen++) {
        $(`#liked-${i}row${j}`).append(
          `<img src="../${resp.data.liked_teams[i].team.players[playerNum].image}" alt="">`
        );
        playerNum++;
      }
    }
    $(`#liked-${i}`).append(`<div id="liked-${i}gk" class="player-row"></div>`);
    $(`#liked-${i}gk`).append(
      `<img src="../${resp.data.liked_teams[i].team.players[playerNum].image}" alt="">`
    );

    for (
      let k = 0;
      k < Object.keys(resp.data.liked_teams[i].team.players).length;
      k++
    ) {
      $(`#liked-players${i}`).append(
        `<a href="/player/${resp.data.liked_teams[i].team.players[k].id}">${resp.data.liked_teams[i].team.players[k].name}, </a>`
      );
    }
  }

  $("#teams-liked").append(`
    <div id='pagination'class="topbar-filter">
      <label>Teams per page:</label>
      <select>
        <option value="range">5 Teams</option>
        <option value="saab">10 Teams</option>
      </select>
      <div class="pagination2">
        <span>Page 1 of 2:</span>
        <a class="active" href="#">1</a>
        <a href="#">2</a>
        <a href="#"><i class="ion-arrow-right-b"></i></a>
      </div>
    </div>
  `);
}
