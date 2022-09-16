$("#team-sort-by").change(getTeams);
$("#team-price-min").change(getTeams);
$("#team-price-max").change(getTeams);
$("#team-rating-min").change(getTeams);
$("#team-rating-max").change(getTeams);
$("#team-formation-filter").change(getTeams);

async function getTeams() {
  let sort = $("#team-sort-by").val();
  let minPrice = $("#team-price-min").val();
  let maxPrice = $("#team-price-max").val();
  let minRating = $("#team-rating-min").val();
  let maxRating = $("#team-rating-max").val();
  let formation = $("#team-formation-filter").val();

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
