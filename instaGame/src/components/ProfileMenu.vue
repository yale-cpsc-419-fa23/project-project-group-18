<template>
    <v-card min-width="250">
        <v-list>
          <v-list-item
            prepend-avatar="https://cdn.vuetifyjs.com/images/john.jpg"
          >
            <template v-slot:title>{{ userName }}</template>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <v-list-item>
            <v-row>
              <v-col cols="8" class="rank-description"> Ranking </v-col>
              <v-col cols="4" class="rank-number"> 343 </v-col>
            </v-row>
          </v-list-item>
        </v-list>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn variant="text" @click="logout"> Logout </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import {ref, onMounted} from 'vue';

const userName = ref('');
const emit = defineEmits(['logout']);

const logout = () => {
    // localStorage.removeItem('userName');
    // userName.value = '';
    emit("logout");
}

onMounted(() => {
    userName.value = localStorage.getItem('userName') || '';
    if (!userName.value) {
        console.log('no username exists:', userName)
    }
});
</script>