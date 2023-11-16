<template>
    <div>
        <v-select
          label="SelectGame"
          :items="['Tic-Tac-Toe', 'Others']"
          variant="solo-inverted"
          v-model = "selectedGame"
        ></v-select>

        <v-btn variant="tonal" @click="createRoom">
          Create Room
        </v-btn>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { get_cookie } from '@/utils';
import { SERVER_ADDRESS } from '../config.js';
import { useRouter } from 'vue-router';
const selectedGame = ref('')
const router = useRouter();

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
</script>