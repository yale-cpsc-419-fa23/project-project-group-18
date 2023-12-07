<!-- LeaderBoard.vue -->
<template>
  <v-table fixed-header height="500px" v-if="leaderboardData.length > 0">
    <thead>
      <tr>
        <th colspan="3"><h2>Leader Board</h2></th>
      </tr>
      <tr>
        <th>#</th>
        <th>Player</th>
        <th>Score</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row, index in leaderboardData" :key="row.player_id">
        <td>{{ index + 1 }}</td>
        <td>{{ row.player_id.slice(0,6) }}</td>
        <td>{{ row.score }}</td>
      </tr>
    </tbody>
  </v-table>
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
    height: 5px;
    border: none;
}
</style>
  