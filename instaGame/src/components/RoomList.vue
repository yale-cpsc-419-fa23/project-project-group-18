<template>
  <v-table fixed-header height="500px">
    <thead>
      <tr>
        <th colspan="3"><h2>Room List</h2></th>
      </tr>
      <tr>
        <th class="text-left">Room Name</th>
        <th class="text-left">Room ID</th>
        <th class="text-left">Players</th>
        <th class="text-left"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="room in roomList" :key="room.room_id">
        <td>
          <v-icon v-if="room.has_password" icon="mdi-lock"></v-icon>
          <!-- <v-btn v-if="room.has_password">lock</v-btn> -->
          <!-- <v-img src="../assets/instaGame-light.svg" v-if="room.has_password" width="20px" height="20px"></v-img> -->
          {{ room.room_name }}
        </td>
        <td>{{ room.room_id }}</td>
        <td>{{ room.player_count }}/{{ room.max_player_count }}</td>
        <td>
          <v-btn class="join-button" @click="joinRoom(room.room_id, room.game_type)">
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

const joinRoom = (roomId, roomType) => {
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
      console.log(roomList);
      router.push({ path: '/game', query: { gameType: roomType } });
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
<style scoped>
table {
  table-layout: fixed;
}
td {
  overflow:hidden;
  white-space: nowrap;
}
</style>
  