// Mock data
var mock_rooms = [
    {id: "0001", players: 2},
    {id: "0002", players: 3},
];

const SERVER_IP = '192.168.4.48'
const port = '5001'

function fetch_rooms() {
    // also receive PlayerID, and store it somewhere,
    $.get(`http://${SERVER_IP}:${port}/roomlist`, function(rooms) {
        console.log(rooms)
        const roomList = $('#room-list');
        roomList.empty();
        rooms.forEach(room => {
            console.log(room)
            roomList.append(`<li>Room ID: ${room.id}, Players: ${room.player_count} <button onclick="joinRoom(${room.id})">Join</button></li>`);
        });
    });
}


function create_player() {
    $.get(`http://${SERVER_IP}:${port}/newplayer`, function(response) {
        console.log(response.message)
        let player_id = response.player_id
        console.log("player id:", player_id)
        return
    });
}


function create_room() {
    // send player_id, 
    // receive room_id,
    // navigate to room page,
    // store room_id, room_state
    $.post('url/api/create-room', function() {
        fetch_rooms();  // Fetch the updated list of rooms
    });
}


function join_room(roomId) {
    $.post(`url/api/join-room/${roomId}`, function() {
        alert('Joined room ' + roomId);
    });
}


// Fetch the initial list of rooms
$(document).ready(function() {
    fetch_rooms();
    create_player()
});