$("#search").submit(function (e) {
  e.preventDefault();
  getPlayers();
});

async function getPlayers() {
  console.log("poop");
  let name = $("#search-name").val();

  resp = await axios.get("/api/players", {
    params: {
      name: name,
    },
  });
  console.log(resp.data);
}
