<template>
  <v-table fixed-header height="500px">
    <RoomPassword
      v-model="showEnterPassword"
      :roomId="clickedRoomId"
      :roomType="clickedRoomType"
    ></RoomPassword>
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
          <v-btn class="join-button" @click="joinRoom(room.room_id, room.game_type, room.has_password)">
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
import RoomPassword from '@/components/RoomPassword.vue';

const roomList = ref([]);
const router = useRouter();
const showEnterPassword = ref(false);
const clickedRoomId = ref('');
const clickedRoomType = ref('');

const fetchRooms = () => {
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/roomlist`)
    .then(response => response.json())
    .then(data => {
      roomList.value = data;
      // console.log('Room list:', roomList.value);
    })
    .catch(error => console.error('Error:', error));
};

const joinRoom = (roomId, roomType, has_password) => {
  console.log('Joining room:', roomId);

  if (has_password) {
    console.log('Room has password');
    clickedRoomId.value = roomId;
    clickedRoomType.value = roomType;
    showEnterPassword.value = true;
  } else {
    sendJoinRoomRequest(roomId, roomType)
    .then(data => {
      if (data.success) {
        router.push({ path: '/game', query: { gameType: data.roomType } });
      } else {
        alert(data.message);
      }
    }).catch(error => {
      console.error('Error joining room:', error);
    });

  }
};

const sendJoinRoomRequest = (roomId, roomType) => {
  let player_id = localStorage.getItem('userName');
  if (!player_id) {
      player_id = get_cookie('player_id');
      return;
  }
  return fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/joinroom`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player_id: player_id, room_id: roomId })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      let room_id = data.room_id;
      document.cookie = `room_id=${room_id}`;
      return { success: true, roomType: roomType, roomId: room_id };
    } else {
      return { success: false, message: data.message };
    }
  })
  .catch(error => {
    console.error('Error:', error);
    return { success: false, message: error.message };
  });
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
  