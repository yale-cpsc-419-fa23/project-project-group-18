import {SERVER_ADDRESS} from './global.js'

var socket;
var currentPiece, opponentPiece;
var player_id, room_id;

function get_cookie(name) {
    // get cookie by name
    let cookieArr = document.cookie.split("; ");
    for(let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0]) {
            return cookiePair[1];
        }
    }
    return null;
}
initialize();

function initialize() {
    $('.cell').each(function(index) {
        $(this).on('click', function() {
            make_move(index);
        });
        $(this).addClass('disabled');
    });
    player_id = get_cookie("player_id");
    room_id = get_cookie("room_id");
    socket = io.connect(SERVER_ADDRESS.IP + ':' + SERVER_ADDRESS.PORT);
    socket.on('joinroom_message', (data) => {
        if (data.is_success == true)
            $('#message').html("Waiting for players to join...");
    });
    socket.on('gamestart_message', (data) => {
        $('#message').html(data.message);
        currentPiece = data.piece[player_id];
        opponentPiece = currentPiece == 'X' ? 'O' : 'X';
        console.log(currentPiece)
        run();
    });
}

function run() {
    socket.on('turnstart_message', (data) => {
        if (data.turn == currentPiece) {
            enable_cell_click_events();
            $('#message').html(data.message);
        }
        else
            $('#message').html(data + " Waiting for opponent...");
    });
    socket.on('turnend_message', update_state(data))
    socket.on('over', end_game(data))
}

function make_move(index) {
    disable_cell_click_events();
    socket.emit('makemove', {player_id: player_id, room_id: room_id, index: index});
}

function update_state(data) {
    const index = data.index;
    $('#board').children().eq(index).text(data.turn);
    $('#board').children().eq(index).off('click');
}

function end_game(data) {
    const winner = data.winner
    if (winner == player_id)
        $('#message').html("You lose!");
    else
        $('#message').html("You Win!");
    disable_cell_click_events();
}

function disable_cell_click_events() {
    $('.cell').each(function() {
        $(this).addClass('disabled');
    });
}

function enable_cell_click_events() {
    $('.cell').each(function() {
        $(this).removeClass('disabled');
    });
}
