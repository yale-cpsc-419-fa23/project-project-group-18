import {SERVER_ADDRESS} from './global.js'

function fetch_rooms() {
    // also receive PlayerID, and store it somewhere,
    $.get(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/roomlist`, function(rooms) {
        console.log(rooms)
        const roomList = $('#room-list');
        roomList.empty();
        rooms.forEach(room => {
            console.log(room)
            const listItem = $(`<li>Room ID: ${room.room_id}, Players: ${room.player_count} <button class="join-button" data-room-id="${room.room_id}">Join</button></li>`);
            roomList.append(listItem);
            listItem.find('.join-button').on('click', function() {
                const roomId = $(this).data('room-id');
                join_room(roomId);
            });
        });
    });
}

function fetch_leader_board() {
    $.get(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/leaderboard`, function(data) {
        if (data && data.length > 0) {
            const leaderboard = $('#leaderboard');
            leaderboard.html('<table><h2>Leader Board</h2><tr><th>Player ID</th><th>Score</th></tr></table>');
            const table = leaderboard.find('table');
            data.forEach(row => {
                table.append(`<tr><td>${row.player_id}</td><td>${row.score}</td></tr>`);
            });
        }
    });
}


function create_player() {
    $.get(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/newplayer`, function(response) {
        console.log(response.message)
        let player_id = response.player_id
        console.log("player id:", player_id)
        document.cookie = `player_id=${player_id}`
        return player_id
    });
}


function create_room() {
    console.log("create")
    let player_id = get_cookie('player_id');
    let game_type = $('#game-list').val();
    console.log(game_type);
    $.post(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/createroom`, { player_id: player_id, game_type: game_type }, function(response) {
        let room_id = response.room_id
        document.cookie = `room_id=${room_id}`;
        jump_to_game()
    });
}

function jump_to_game() {
    console.log("jump to game room: ")
    window.location.href = 'tictactoe.html';
}


function join_room(room_id) {
    console.log(room_id)
    let player_id = get_cookie('player_id')
    $.post(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/joinroom`, { player_id: player_id, room_id: room_id}, function(response) {
        document.cookie = `room_id=${room_id}`;
        alert('Joined room ' + room_id);
        jump_to_game()
    });
}

function set_up_lobby() {
    fetch_rooms();
    fetch_leader_board()
    window.setInterval(fetch_rooms, 5000)
    let player_id = get_cookie('player_id');
    if (player_id) {
        console.log('player_id exists:', player_id);
    } else {
        console.log('player_id does not exist\n create new player from server');
        create_player();
    }
    $("#creat-room-button").on('click', create_room);
}


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


// Fetch the initial list of rooms
$(document).ready(function() {
    set_up_lobby();
});