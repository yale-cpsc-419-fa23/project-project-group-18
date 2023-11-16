<template>
    <ul id="room-list">
      <li v-for="room in roomList" :key="room.room_id">
        Room ID: {{ room.room_id }}, Players: {{ room.player_count }}/{{ room.max_player_count }}
        <button class="join-button" @click="joinRoom(room.room_id)">Join</button>
      </li>
    </ul>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '../config.js';
import { get_cookie } from '@/utils';

const roomList = ref([]);

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
  setInterval(fetchRooms, 5000);
});
</script>
  