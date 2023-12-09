<template>
    <v-dialog v-model="showEnterPassword" persistent max-width="600px">
        <v-card>
            <v-card-title class="headline d-flex justify-space-between">
                <v-col cols="12">Enter Password</v-col>

                <!-- <v-col cols="6">
                    <v-btn icon="$close" variant="text" @click="close"></v-btn>
                </v-col> -->
            </v-card-title>
            <v-card-subtitle>
                <v-col cols="6">A password is required to join</v-col>
            </v-card-subtitle>
            <v-card-text>
                <v-form ref="form" @submit.prevent="sendJoinRoomRequest">
                    <v-text-field
                        v-model="password"
                        type = "password"
                        required
                    ></v-text-field>

                    <div class="d-flex flex-column">
                        <v-spacer></v-spacer>
                        <v-btn type="submit" color="success" class="mt-4" block variant="tonal" >
                            Join
                        </v-btn>
                        <v-btn variant="tonal" text @click="close">Cancle</v-btn>
                    </div>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>
<script setup>
import {ref, watch, computed} from 'vue';
import { SERVER_ADDRESS } from '../config.js';
import { get_cookie } from '@/utils';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  modelValue: {},
  roomId: {
    type: String,
    default: ''
  },
  roomType: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'login-success']);
const showEnterPassword = ref(props.modelValue);
const form = ref(null);
const isFormValid = computed(() => form.value?.validate());

const password = ref('');

watch(() => props.modelValue, (newValue) => {
  showEnterPassword.value = newValue;
});

const close = () => {
  emit('update:modelValue', false);
};

const sendJoinRoomRequest = () => {
    let player_id = localStorage.getItem('userName');
    if (!player_id) {
        player_id = get_cookie('player_id');
    }
    console.log('Joining room password:', props.roomId);
    console.log('RoomID', props.roomId);
    fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/joinroompassword`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player_id: player_id, room_id: props.roomId, password: password.value })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      let room_id = data.room_id;
      document.cookie = `room_id=${room_id}`;
      router.push({ path: '/game', query: { gameType: props.roomType } });
    } else {
      alert(data.message);
    }
  })
  .catch(error => console.error('Error:', error));
}


</script>