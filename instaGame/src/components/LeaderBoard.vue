<!-- LeaderBoard.vue -->
<template>
    <div id="leaderboard">
      <v-table v-if="leaderboardData.length > 0">
        <tr>
          <th colspan="2">Leader Board</th>
        </tr>
        <tr>
          <th>Player ID</th>
          <th>Score</th>
        </tr>
        <tbody>
          <tr v-for="row in leaderboardData" :key="row.player_id">
          <td>{{ row.player_id }}</td>
          <td>{{ row.score }}</td>
          </tr>
        </tbody>
      </v-table>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { SERVER_ADDRESS } from '../config.js';

const leaderboardData = ref([]);

const fetchLeaderBoard = () => {
	console.log("fetch in leaderboard.vue")
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/leaderboard`)
    .then(response => response.json())
    .then(data => {
      // console.log(data)
      leaderboardData.value = data;
    })
    .catch(error => console.error('Error:', error));
};

onMounted(() => {
fetchLeaderBoard();
setInterval(fetchLeaderBoard, 60000);
});


</script>

<style>
table.v-table tbody td {
    height: 10px;
    border: none;
    color: red;
}
</style>
  