<template>
    <v-dialog v-model="showCreateRoom" persistent max-width="600px">
        <v-card>
            <v-card-title class="headline d-flex justify-space-between">
                <v-col cols="6">Create New Room</v-col>
                
                <v-btn icon @click="close">
                    <v-icon>mdi-close</v-icon> 
                </v-btn>
                <!-- <v-col cols="6">
                    <v-btn icon="$close" variant="text" @click="close"></v-btn>
                </v-col> -->
            </v-card-title>
            <v-card-text>
                <v-form ref="form">
                    <v-text-field
                        v-model="name"
                        :counter="10"
                        :rules="nameRules"
                        label="Room Name"
                        required
                    ></v-text-field>

                    <v-select
                        v-model="gameType"
                        :items="items"
                        :rules="[v => !!v || 'Game Type is required']"
                        label="Game Type"
                        required
                    ></v-select>

                    <v-checkbox
                        v-model="needPassword"
                        label="Add a password?"
                        required
                    ></v-checkbox>

                    <v-text-field
                        v-if="needPassword"
                        label="Password"
                        v-model="password"
                        type="password"
                        required
                    ></v-text-field>

                    <div class="d-flex flex-column">
                        <v-btn color="success" class="mt-4" block @click="createNewRoom" variant="tonal">
                        Create
                        </v-btn>
                    </div>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script setup>
import {ref, watch} from 'vue';
import { SERVER_ADDRESS } from '../config.js';
import { get_cookie } from '@/utils';
import { useRouter } from 'vue-router';

const router = useRouter();
const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue', 'login-success']);
const showCreateRoom = ref(props.modelValue);

const name = ref('');
const gameType = ref(null);
const nameRules = [v => (v && v.length <= 10) || 'Name must be less than 10 characters'];
const items = ['Tic-Tac-Toe', 'Gomoku'];
const needPassword = ref(false);
const password = ref('');

watch(() => props.modelValue, (newValue) => {
  showCreateRoom.value = newValue;
});

const close = () => {
  emit('update:modelValue', false);
};

const createNewRoom = () => {
  console.log("Create New Room");
  let userName = localStorage.getItem('userName') || '';
  if (!userName) {
    userName = get_cookie('player_id');
  }
  let game_type = gameType.value;
  console.log(game_type);

  let hasPassword = false;
  if (password) {
    hasPassword = true;
  }

  let requestBody = '';
  if (hasPassword) {
    requestBody = JSON.stringify({ 
        player_id: userName, 
        game_type: game_type, 
        room_name: name.value, 
        has_password: hasPassword,
        password: password.value
    })
  } else {
    requestBody = JSON.stringify({ 
        player_id: userName, 
        game_type: game_type, 
        room_name: name, 
        has_password: hasPassword
    })
  }

  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/createroom`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: requestBody
  })
  .then(response => response.json())
  .then(data => {
    console.log(data)
    let room_id = data.room_id;
    document.cookie = `room_id=${room_id}`;
    console.log(room_id)
    router.push({ path: '/game', query: { gameType: game_type } });
  })
  .catch(error => console.error('Error:', error));
};
</script>