$("#sort-by").change(getTeams);
$("#price-min").change(getTeams);
$("#price-max").change(getTeams);
$("#rating-min").change(getTeams);
$("#rating-max").change(getTeams);
$("#formation").change(getTeams);

async function getTeams() {
  let sort = $("#sort-by").val();
  let minPrice = $("#price-min").val();
  let maxPrice = $("#price-max").val();
  let minRating = $("#rating-min").val();
  let maxRating = $("#rating-max").val();
  let formation = $("#formation").val();

  resp = await axios.get("/api/teams", {
    params: {
      sort: sort,
      price_min: minPrice,
      price_max: maxPrice,
      rating_min: minRating,
      rating_max: maxRating,
      formation: formation,
    },
  });
  console.log(resp.data);

  $(".movie-item-style-2").remove();
  $("#pagination").remove();

  for (let i = 0; i < resp.data.length; i++) {
    $("#teams-list").append(
      `<div id=${i} class='movie-item-style-2'>
        <img src='static/images/uploads/mv1.jpg' alt=''>
        <div class='mv-item-infor'>
          <h6><a href="#"> ${resp.data[i].team.name}</a></h6>
          <p class="rate">Team Rating: <span>${resp.data[i].team.rating}</span></p>
          <p class="run-time"> Formation: ${resp.data[i].team.formation}
          <p>Price: ${resp.data[i].team.price}</p>
          <p id='players${i}'>Players: </p>
          <p>Likes: ${resp.data[i].likes}</p>
          <p>Last Edited: ${resp.data[i].team.timestamp} </p>
        </div>
      </div>`
    );
    console.log(Object.keys(resp.data[i].team.players).length);
    for (let k = 0; k < Object.keys(resp.data[i].team.players).length; k++) {
      $(`#players${i}`).append(
        `<a href="#">${resp.data[i].team.players[k].name}, </a>`
      );
    }
  }

  $("#teams-list").append(`
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
