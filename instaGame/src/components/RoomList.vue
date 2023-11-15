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

const roomList = ref([]);

const fetchRooms = () => {
  console.log('fetch rooms')
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/roomlist`)
    .then(response => response.json())
    .then(data => {
      console.log(data)
      roomList.value = data;
    })
    .catch(error => console.error('Error:', error));
};

const joinRoom = (roomId) => {
// Implementation of join room
};

onMounted(() => {
fetchRooms();
setInterval(fetchRooms, 5000);
});
</script>
  