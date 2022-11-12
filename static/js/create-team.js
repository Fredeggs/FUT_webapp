$(displayTeam());

function displayTeam() {

    let FORMATION = $("#formation").val()
    console.log(FORMATION)
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
