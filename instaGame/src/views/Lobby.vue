<template>
  <div>
    <!-- Top Bar -->
    <v-row class="top-bar">
      <v-col cols="8" class="logo-col">
        <!-- <img src="path" alt="Logo" /> -->
      </v-col>

      <v-col cols="4" class="login-btn-col">
        <!-- Login -->
        <div v-if="userName" class="user-name-display">
          Welcome, <span class="user-name" @click="showProfileMenu()">{{ userName }}</span>
        </div>
        <v-btn v-else @click="showLogin()" class="login-btn">Login</v-btn>
        <v-btn v-if="userName" @click="testlogout()" class="logout-btn" variant="tonal">Logout</v-btn>
      </v-col>


    </v-row>
    <!-- Leader Board -->
    <v-row>
      <v-col cols="6">
        <RoomList />
      </v-col>

      <v-col cols="1"></v-col>
      
      <v-col cols="4" class="leaderboard-col">
        <LeaderBoard />
      </v-col>

    </v-row>
    <v-row>
      <v-col cols="2"></v-col>
      <v-col cols="4">
        <!-- <SelectGame /> -->
        <v-btn variant="tonal" @click="showCreateRoomModal">
          Create Room
        </v-btn>
      </v-col>
    </v-row>
    <LoginPopup @login-success="handleLoginSuccess" v-model="showLoginPopup" />
    <!-- <LoginTest v-model="showLoginPopup" /> -->
    <CreateRoom v-model="showCreateRoom"></CreateRoom>

  </div> 
</template>
  
<script setup>
import RoomList from '@/components/RoomList.vue'
import LeaderBoard from '@/components/LeaderBoard.vue'
import SelectGame from '@/components/SelectGame.vue';
import LoginPopup from '@/components/LoginPopup.vue';
import CreateRoom from '@/components/CreateRoom.vue';
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '@/config.js';
import { useRouter } from 'vue-router';
import { get_cookie } from '@/utils';
// import LoginTest from '@/components/LoginTest.vue';


const router = useRouter();

const showLoginPopup = ref(false);
const showCreateRoom = ref(false);
const userName = ref('');

const showCreateRoomModal = () => {
  showCreateRoom.value = true;
}

const testlogout = () => {
  localStorage.removeItem('userName');
  userName.value = '';
}

const showLogin = () => {
  showLoginPopup.value = true;
}

const showProfileMenu = () => {
  
}

const handleLoginSuccess = (userId) => {
  userName.value = userId;
  showLoginPopup.value = false;
};

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

onMounted(() => {
  // localStorage.removeItem('userName');
  let player_id = get_cookie('player_id');
  if (player_id) {
      console.log('player_id exists:', player_id);
    } else {
      console.log('player_id does not exist\n create new player from server');
      createPlayer();
    }
    userName.value = localStorage.getItem('userName') || '';
    if (userName.value) {
      console.log('username exists:', userName)
      document.cookie = `player_id=${player_id}`
    }
});
</script>

<style>
  .top-bar {
  padding: 10px;
}

  .logo-col {
    display: flex;
    align-items: center; /* Vertically center the logo */
  }

  .login-btn-col {
    display: flex;
    justify-content: flex-end; /* Align the button to the right */
    align-items: center; /* Vertically center the button */
  }

  .user-name-display {
    font-size: large;
    padding-right: 10px;
  }

  .user-name {
    font-weight: bold;
  }
</style>