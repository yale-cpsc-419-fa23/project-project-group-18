<template>
	<div id="container">
		<template v-if="this.gameType === 'Tic-Tac-Toe'">
			<TicTacToe :socket="socket" :room_id="room_id" :player_id="player_id" :message="message" @updateMessage="updateMessage" @showButtons="showButtons"/>
		</template>
		<template v-else-if="this.gameType === 'Gomoku'">
			<Gomoku :socket="socket" :room_id="room_id" :player_id="player_id" :message="message" @updateMessage="updateMessage" @showButtons="showButtons"/>
		</template>
		<v-label id="message">{{ message }}</v-label>
	</div>
	<v-row class="button-row">
		<v-col cols="4">
			<v-btn id="leave-button" @click="leaveRoom" v-show="leaveButtonVisible">Leave</v-btn>
		</v-col>
		<v-col cols="4">
			<v-btn id="restart-button" @click="restartRoom" v-show="restartButtonVisible">Restart</v-btn>
		</v-col>
	</v-row>
</template>

<script>
	import { io } from "socket.io-client";
	import { SERVER_ADDRESS } from '../config.js';
	import { useRouter } from 'vue-router';
	import { get_cookie } from '@/utils';
	import TicTacToe from "../components/Tic-Tac-Toe.vue";
	import Gomoku from '../components/Gomoku.vue';
	
	const router = useRouter();
	let socket, player_id, room_id;
	export default {
    props: ['gameType'],
    data() {
        return {
            message: 'Inactive Game Room',
            leaveButtonVisible: false,
			restartButtonVisible: false,
            socket: io.connect(SERVER_ADDRESS.IP + ':' + SERVER_ADDRESS.PORT),
            player_id: get_cookie('player_id'),
            room_id: get_cookie('room_id'),
        };
    },
    mounted() {
        this.initialize();
    },
    methods: {
        initialize() {
            document.getElementById('leave-button').addEventListener('click', this.leaveRoom);
			player_id = this.player_id;
			room_id = this.room_id;
			socket = this.socket;
			let userName = localStorage.getItem('userName') || '';
			if (userName != '')
				player_id = userName;
            socket.emit('joinroom', { player_id: player_id, room_id: room_id });
            socket.on('joinroom_message', (data) => {
                if (data.is_success === true) {
                    this.message = 'Waiting for players to join...';
                }
            });
        },
        leaveRoom() {
            socket.disconnect();
            window.location.href = '/';
        },
        restartRoom() {
			socket.emit('restart', { player_id: player_id, room_id: room_id });
			socket.on('rejoin_message', (data) => {
                if (data.is_success === true) {
                    this.message = 'Waiting for players to join...';		
					this.leaveButtonVisible = false;
					this.restartButtonVisible = false;
                }
            });
        },
		updateMessage(newMessage) {
			this.message = newMessage;
		},
		showButtons() {
			this.leaveButtonVisible = true;
			this.restartButtonVisible = true;
		}
    },
    components: { TicTacToe, Gomoku }
};
</script>

<style scoped>
	#container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}
	#message {
		position: absolute;
		bottom: 10vh;
		font-size: 24px;
		color: #2c3e50;
		font-weight: bold;
		user-select: none;
	}

	.button-row {
		position: absolute;
		bottom: 0;
		width: 80%;
		justify-content: center;
		align-items: center;
		display: flex;
	}

	#leave-button,
	#restart-button {
		font-size: 16px;
		margin-top: -50px;
		background-color: #266f9f;
		border-radius: 5px;
	}
</style>