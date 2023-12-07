<template>
    <v-card min-width="250">
        <v-list>
          <v-list-item
            prepend-avatar="https://avatars.githubusercontent.com/t/8715767?s=116&v=4"
          >
            <template v-slot:title>{{ userName }}</template>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <v-list-item>
            <v-row>
              <v-col cols="8" class="rank-description"> Ranking </v-col>
              <v-col cols="4" class="rank-number"> {{ rank }} </v-col>
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
import {ref, onMounted, defineProps} from 'vue';

const userName = ref('');
const emit = defineEmits(['logout']);
const props = defineProps(['rank']);

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
