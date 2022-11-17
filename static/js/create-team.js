$(displayTeam());

$('#formation').on('change', displayTeam);

function displayTeam() {
    $(".team-roster").empty();
    let FORMATION = $("#formation").val();
    let playerNum = 0;

    for (let i = FORMATION.length - 1; i >= 0; i--) {
        $(".team-roster").append(`<div id="row${i}" class="player-row"></div>`);
        let currRow = FORMATION.charAt(i);
        for (let rowLen = 0; rowLen < parseInt(currRow); rowLen++) {
            $(`#row${i}`).append(
                `<a href="#" data-player="${playerNum}" class="empty-player-div">
                    <img src="../static/images/add_circle_FILL0_wght400_GRAD0_opsz48.png" alt="">
                </a>`
            );
            playerNum++;
        }
    }
    $(`.team-roster`).append(`<div id="gk" class="player-row"></div>`);
    $(`#gk`).append(
        `<div data-player="10" class="empty-player-div">
            <img src="../static/images/add_circle_FILL0_wght400_GRAD0_opsz48.png" alt="">
        </div>`
    );
}
