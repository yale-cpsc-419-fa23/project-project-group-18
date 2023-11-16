<template>
  <div>
    <v-btn variant="tonal" @click="testLogin">
      Test
    </v-btn>
    <v-row>
      <v-col cols="6">

        <div class="room-list">
          <RoomList />
        </div>

        <v-select
          label="SelectGame"
          :items="['tic-tac-toe', 'Others']"
          variant="solo-inverted"
          v-model = "selectedGame"
        ></v-select>

        <v-btn variant="tonal" @click="createRoom">
          Create Room
        </v-btn>
      </v-col>

      <v-col cols="3" class="leaderboard-col">

        <div class="leaderboard">
        <LeaderBoard />
        </div>
      </v-col>

    </v-row>
  </div> 
</template>
  
<script setup>
import RoomList from '../components/RoomList.vue'
import LeaderBoard from '../components/LeaderBoard.vue'
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '../config.js';
import { useRouter } from 'vue-router';
import { get_cookie } from '@/utils';

const router = useRouter();
const selectedGame = ref('')


const testLogin = () => {
  let player_id = get_cookie('player_id');
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/testcookies`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player_id: player_id })
  })
  .then(response => response.json())
  .then(response => {
    console.log(response.message)
  })
  .catch(error => console.error('Error:', error));

}


const createPlayer = () => {
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/newplayer`)
  .then(response => response.json())
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
  let game_type = selectedGame.value;
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
    router.push({ path: '/game', query: { gameType: game_type } });
  })
  .catch(error => console.error('Error:', error));
};

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

<style>
  .leaderboard-col {
    max-height: 50vh;
    overflow: auto; /* Optional, for scroll if content exceeds max height */
  }
</style>