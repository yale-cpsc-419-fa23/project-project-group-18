<template>
  <div>
    <!-- <v-btn variant="tonal" @click="testLogin">
      Test
    </v-btn> -->
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
    <!-- Login -->
    <button @click="showLogin()">Login</button>
    <LoginPopup v-model="showLoginPopup" />

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


const router = useRouter();

const showLoginPopup = ref(false);

const showLogin = () => {
  showLoginPopup.value = true
  console.log(showLoginPopup.value)
}

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

onMounted(() => {
let player_id = get_cookie('player_id');
if (player_id) {
    console.log('player_id exists:', player_id);
  } else {
    console.log('player_id does not exist\n create new player from server');
    createPlayer();
  }
});
</script>

<style>
  .leaderboard-col {
    max-height: 50vh;
    overflow: auto; /* Optional, for scroll if content exceeds max height */
  }
</style>