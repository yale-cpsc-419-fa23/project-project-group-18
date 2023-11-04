// Mock data
var mock_rooms = [
    {id: "0001", players: 2},
    {id: "0002", players: 3},
];

const SERVER_IP = '192.168.4.48'
const PORT = '5001'

function fetch_rooms() {
    // also receive PlayerID, and store it somewhere,
    $.get(`http://${SERVER_IP}:${PORT}/roomlist`, function(rooms) {
        console.log(rooms)
        const roomList = $('#room-list');
        roomList.empty();
        rooms.forEach(room => {
            console.log(room)
            roomList.append(`<li>Room ID: ${room.room_id}, Players: ${room.player_count} <button onclick="join_room(${room.room_id})">Join</button></li>`);
        });
    });
}


function create_player() {
    $.get(`http://${SERVER_IP}:${PORT}/newplayer`, function(response) {
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
    $.post(`http://${SERVER_IP}:${PORT}/createroom`, { player_id: player_id }, function(response) {
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
    $.post(`http://${SERVER_IP}:${PORT}/joinroom`, { player_id: player_id, room_id: room_id}, function(response) {
        document.cookie = `room_id=${room_id}`;
        alert('Joined room ' + room_id);
        jump_to_game()
    });
}

function set_up_lobby() {
    fetch_rooms();
    let player_id = get_cookie('player_id');
    if (player_id) {
        console.log('player_id exists:', player_id);
    } else {
        console.log('player_id does not exist\n create new player from server');
        create_player();
    }
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