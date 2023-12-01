<template>
  <div>
    <!-- Top Bar -->
    <v-row class="top-bar">
      <v-col cols="6" class="logo-col">
        <!-- <img src="path" alt="Logo" /> -->
      </v-col>

      <v-col cols="6" class="login-btn-col">
        <!-- Login -->
        <div v-if="userName" class="user-name-display">
          Welcome, {{ userName }}
        </div>
        <button v-else @click="showLogin()" class="login-btn">Login</button>
      </v-col>


    </v-row>
    <v-col cols ="6 " class="test-log-out">
        <button @click="testlogout()">Test Logout</button>
      </v-col>
    <!-- Leader Board -->
    <v-row>
      <v-col cols="6">
        <RoomList />

        <SelectGame />
      </v-col>

      <v-col cols="3" class="leaderboard-col">

        <div class="leaderboard">
        <LeaderBoard />
        </div>
      </v-col>

    </v-row>
    <LoginPopup @login-success="handleLoginSuccess" v-model="showLoginPopup" />
    <!-- <LoginTest v-model="showLoginPopup" /> -->

  </div> 
</template>
  
<script setup>
import RoomList from '@/components/RoomList.vue'
import LeaderBoard from '@/components/LeaderBoard.vue'
import SelectGame from '@/components/SelectGame.vue';
import LoginPopup from '@/components/LoginPopup.vue';
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '@/config.js';
import { useRouter } from 'vue-router';
import { get_cookie } from '@/utils';
// import LoginTest from '@/components/LoginTest.vue';


const router = useRouter();

const showLoginPopup = ref(false);
const userName = ref('');

const testlogout = () => {
  localStorage.removeItem('userName');
  userName.value = '';
}

const showLogin = () => {
  showLoginPopup.value = true
  console.log(showLoginPopup.value)
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
  .leaderboard-col {
    max-height: 50vh;
    overflow: auto; /*for scroll if content exceeds max height */
  }
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
</style>