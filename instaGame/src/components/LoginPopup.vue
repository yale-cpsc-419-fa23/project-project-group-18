<template>
  <v-dialog v-model="showLoginPopup" persistent max-width="600px">
    <v-card>
      <v-card-title class="headline">{{ isLoginView ? 'Login' : 'Register' }}</v-card-title>
      <v-card-text>
        <form @submit.prevent="isLoginView ? handleLogin() : handleRegister()">
          <v-row>
            <v-col cols="12">
              <v-text-field label="Username" v-model="username" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Password" v-model="password" type="password" required></v-text-field>
            </v-col>

            <!-- Registration specific fields -->
            <v-col cols="12" v-if="!isLoginView">
              <v-text-field label="Email" v-model="email" type="email" required></v-text-field>
              <!-- Add other registration fields here -->
            </v-col>
          </v-row>

          <v-row justify="center">
            <v-btn type="submit" color="primary" variant="tonal">{{ isLoginView ? 'Login' : 'Register' }}</v-btn>
          </v-row>

        </form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <!-- Toggle View Button -->
        <v-btn color="blue" text @click="toggleView">
          {{ isLoginView ? 'Create Account' : 'Back to Login' }}
        </v-btn>
        <v-btn color="green darken-1" text @click="closePopup">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

  
<script setup>
import { ref, watch, onMounted } from 'vue';
import { SERVER_ADDRESS } from '../config.js';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue', 'login-success']);

const showLoginPopup = ref(props.modelValue);
const isLoginView = ref(true); // New state to track the current view
const username = ref('');
const password = ref('');
const email = ref(''); // For registration

watch(() => props.modelValue, (newValue) => {
  showLoginPopup.value = newValue;
  if (newValue) { // clean previouse input
    // username.value = '';
    password.value = '';
    email.value = '';
  }
});

const toggleView = () => {
  isLoginView.value = !isLoginView.value;
};

const closePopup = () => {
  emit('update:modelValue', false);
};

const handleLogin = () => {
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/login`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: username.value, password: password.value})
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('login success', data.user_id);
      localStorage.setItem('userName', data.user_id);
      emit('login-success', data.user_id);
      emit('update:modelValue',false);
    } else {
      alert(data.message);
    }
  })
  .catch(error => console.error('Error:', error));
};

const handleRegister = () => {
  fetch(`http://${SERVER_ADDRESS.IP}:${SERVER_ADDRESS.PORT}/register`, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: username.value, password: password.value, email:email.value })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('login success', data.user_id);
      localStorage.setItem('userName', data.user_id);
      emit('login-success', data.user_id);
      emit('update:modelValue',false);
    } else {
      alert(data.message);
    }
  })
  .catch(error => console.error('Error:', error));
};
</script>

