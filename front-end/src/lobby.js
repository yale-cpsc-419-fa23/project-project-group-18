// Mock data
var mock_rooms = [
    {id: "0001", players: 2},
    {id: "0002", players: 3},
];


function fetchRooms() {
    // also receive PlayerID, and store it somewhere,
    $.get('http://192.168.4.48:5001/roomlist', function(rooms) {
        console.log(rooms)
        const roomList = $('#room-list');
        roomList.empty();
        rooms.forEach(room => {
            console.log(room)
            roomList.append(`<li>Room ID: ${room.id}, Players: ${room.player_count} <button onclick="joinRoom(${room.id})">Join</button></li>`);
        });
    });
}


function createRoom() {
    // send player_id, 
    // receive room_id,
    // navigate to room page,
    // store room_id, room_state
    $.post('url/api/create-room', function() {
        fetchRooms();  // Fetch the updated list of rooms
    });
}


function joinRoom(roomId) {
    $.post(`url/api/join-room/${roomId}`, function() {
        alert('Joined room ' + roomId);
    });
}


// Fetch the initial list of rooms
$(document).ready(function() {
    fetchRooms();
});