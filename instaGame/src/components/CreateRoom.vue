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
    console.log('Create New Room');
}

</script>