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

  await axios.get("/api/teams", {
    params: {
      sort: sort,
      price_min: minPrice,
      price_max: maxPrice,
      rating_min: minRating,
      rating_max: maxRating,
      formation: formation,
    },
  });
}
