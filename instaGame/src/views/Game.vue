<template>
	<div id="container">
		<template v-if="this.gameType === 'Tic-Tac-Toe'">
			<TicTacToe :socket="socket" :room_id="room_id" :player_id="player_id" :message="message" @updateMessage="updateMessage" @showLeave="showLeave"/>
		</template>
		<template v-else-if="this.gameType === 'Gomoku'">
			<Gomoku :socket="socket" :room_id="room_id" :player_id="player_id" :message="message" @updateMessage="updateMessage" @showLeave="showLeave"/>
		</template>
		<p id="message">{{ message }}</p>
		<button id="leave-button" @click="leaveRoom" v-show="leaveButtonVisible">Leave</button>
	</div>
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
		updateMessage(newMessage) {
			this.message = newMessage;
		},
		showLeave() {
			this.leaveButtonVisible = true;
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
	#renderCanvas {
		width: 144%;
		height: 81%;
		padding: 0;
	}
	#message {
		position: absolute;
		bottom: 10vh;
		font-size: 24px;
		color: #2c3e50;
		font-weight: bold;
		user-select: none;
	}

	#leave-button {
		padding: 10px 20px;
		font-size: 16px;
		background-color: #3498db;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s ease;
		position: absolute;
		bottom: 3vh;
	}
	
	#leave-button:hover {
		background-color: #2980b9;
	}
</style>