<template>
  <v-table fixed-header height="500px">
    <thead>
      <tr>
        <th class="text-left">Room ID</th>
        <th class="text-left">Players</th>
        <th class="text-left"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="room in roomList" :key="room.room_id">
        <td>{{ room.room_id }}</td>
        <td>{{ room.player_count }}/{{ room.max_player_count }}</td>
        <td>
          <v-btn class="join-button" @click="joinRoom(room.room_id)">
          Join
          </v-btn>
        </td>

      </tr>
    </tbody>
  </v-table>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '../config.js';
import { get_cookie } from '@/utils';
import { useRouter } from 'vue-router';

const roomList = ref([]);
const router = useRouter();

const fetchRooms = () => {
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/roomlist`)
    .then(response => response.json())
    .then(data => {
      roomList.value = data;
    })
    .catch(error => console.error('Error:', error));
};

const joinRoom = (roomId) => {
  console.log('join room');
  let player_id = get_cookie('player_id');
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/joinroom`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player_id: player_id, room_id: roomId })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
    if (data.success) {
      let room_id = data.room_id;
      document.cookie = `room_id=${room_id}`;
      let gameType = 'TicTacToe';
      router.push({ path: '/game', query: { gameType: gameType } });
    } else {
      alert(data.message);
    }
  })
  .catch(error => console.error('Error:', error));
};

onMounted(() => {
  fetchRooms();
  setInterval(fetchRooms, 3000);
});
</script>
  