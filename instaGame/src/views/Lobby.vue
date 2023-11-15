<template>
  <div>
    <RoomList />

    <select id="game-list">
      <option value="tic-tac-toe">Tic-Tac-Toe</option>
    </select>
    <button id="create-room-button" @click="createRoom">Create Room</button>

    <LeaderBoard />
  </div> 
</template>
  
<script setup>
import RoomList from '../components/RoomList.vue'
import LeaderBoard from '../components/LeaderBoard.vue'
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '../config.js';
import { useRouter } from 'vue-router';
const router = useRouter();

const createPlayer = () => {
fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/newplayer`)
.then(response => {
  console.log(response.message)
  let player_id = response.player_id
  console.log("player id:", player_id)
  document.cookie = `player_id=${player_id}`
  // return player_id
})
.catch(error => console.error('Error:', error));
}

const createRoom = () => {
  console.log("create");

  let player_id = get_cookie('player_id');
  let game_type = document.getElementById('game-list').value;
  console.log(game_type);

  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/createroom`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player_id: player_id, game_type: game_type })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
    let room_id = data.room_id;
    document.cookie = `room_id=${room_id}`;
    console.log(room_id)
    let gameType = 'TicTacToe';
    router.push({ path: '/game', query: { gameType: gameType } });
  })
  .catch(error => console.error('Error:', error));
};

// Additional function for cookie retrieval
function get_cookie(name) {
let cookieArr = document.cookie.split("; ");
for(let i = 0; i < cookieArr.length; i++) {
  let cookiePair = cookieArr[i].split("=");
  if (name === cookiePair[0].trim()) {
    return cookiePair[1];
  }
}
return null;
}

onMounted(() => {
let player_id = get_cookie('player_id');
if (player_id) {
    console.log('player_id exists:', player_id);
  } else {
    console.log('player_id does not exist\n create new player from server');
    createPlayer();
  }
// fetchLeaderBoard();
// setInterval(fetchLeaderBoard, 60000);
});
</script>
