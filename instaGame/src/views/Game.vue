<template>
	<div id="container">
		<!-- Game: {{ gameType }} -->
		<canvas id="renderCanvas" ref="renderCanvas"></canvas>
		<p id="message">{{ message }}</p>
		<button id="leave-button" @click="leaveRoom" v-show="leaveButtonVisible">Leave</button>
	</div>
</template>

<script>
	import * as BABYLON from 'babylonjs';
	import 'babylonjs-loaders';
	import { io } from "socket.io-client";
	import { SERVER_ADDRESS } from '../config.js';
	import { ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { get_cookie } from '@/utils';
	
	const router = useRouter();
	const gameType = ref('');
	let cells = [];
	let engine, scene, socket, currentPiece, player_id, room_id;
	let checkerboardTask, circleTask, crossTask, turn, vm;
	export default {
	data() {
		return {
			message: 'Inactive Game Room',
			leaveButtonVisible: false,
		};
	},
	mounted() {
		vm = this;
		this.initialize();
	},
	methods: {
		initialize() {
			const canvas = this.$refs.renderCanvas;
			engine = new BABYLON.Engine(canvas, true);
			scene = this.createScene(canvas, engine);

			this.$nextTick(() => {
				this.listenForLeaveButton();
				player_id = get_cookie('player_id');
				room_id = get_cookie('room_id');
				socket = io.connect(SERVER_ADDRESS.IP + ':' + SERVER_ADDRESS.PORT);
				socket.emit('joinroom', { player_id: player_id, room_id: room_id });

				socket.on('joinroom_message', (data) => {
				if (data.is_success === true) {
					this.message = 'Waiting for players to join...';
				}
				});

				socket.on('gamestart_message', (data) => {
				this.message = data.message;
				currentPiece = data.piece_map[player_id];
				this.run();
				});
			});
		},
		listenForLeaveButton() {
			document.getElementById('leave-button').addEventListener('click', this.leaveRoom);
		},
		run() {
			socket.on('turnstart_message', (data) => {
				if (data.turn === currentPiece) {
				this.enableCellClickEvents();
				this.message = data.message + ', make a move.';
				} else {
				this.message = data.message + ', waiting for opponent...';
				}
			});

			socket.on('turnend_message', (data) => {
				this.updateState(data);
			});

			socket.on('gameover_message', (data) => {
				this.endGame(data);
			});
		},
		makeMove(index) {
			this.disableCellClickEvents();
			socket.emit('makemove', { player_id: player_id, room_id: room_id, index: index });
		},
		updateState(data) {
			this.placePiece(data.index, data.turn);
		},
		endGame(data) {
			const winner = data.winner;
			if (winner === '') {
				this.message = 'Tie!';
			} else if (winner === player_id) {
				this.message = 'You Win!';
			} else {
				this.message = 'You Lose!';
			}
			this.disableCellClickEvents();
			this.leaveButtonVisible = true;
		},
		leaveRoom() {
			socket.disconnect();
			window.location.href = '/';
		},
		disableCellClickEvents() {
			turn = false;
		},
		enableCellClickEvents() {
			turn = true;
		},
		findClosestCell(point) {
			var idx = 0,
				min_dist = Infinity;
			for (var i = 0; i < 9; i++) {
				var distance = BABYLON.Vector3.Distance(cells[i].position, point);
				if (distance < min_dist) {
				min_dist = distance;
				idx = i;
				}
			}
			return {
				index: idx,
				occupied: cells[idx].occupied,
			};
		},
		placePiece(idx, piece) {
			var position = cells[idx].position;
			cells[idx].occupied = true;
			if (piece == 'O') {
				var circle = circleTask.loadedMeshes[0].getChildren()[0].createInstance();
				circle.position = position;
				circle.scaling.x *= 0.6;
				circle.scaling.y *= 0.3;
				circle.scaling.z *= 0.6;
				circle.setEnabled(true);
			} else if (piece == 'X') {
				var cross = crossTask.loadedMeshes[0].getChildren()[0].createInstance();
				cross.position = position;
				cross.scaling.x *= 0.8;
				cross.scaling.y *= 0.8;
				cross.scaling.z *= 0.3;
				cross.rotationQuaternion = null;
				cross.rotation.x = BABYLON.Tools.ToRadians(90);
				cross.rotation.z = BABYLON.Tools.ToRadians(45);
			}
		},
		createScene(canvas, engine) {
			var scene = new BABYLON.Scene(engine);

			scene.environmentTexture = BABYLON.CubeTexture.CreateFromPrefilteredData(
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/textures/environment.env',
				scene
			);
			const skydome = BABYLON.MeshBuilder.CreateBox('sky', { size: 1000, sideOrientation: BABYLON.Mesh.BACKSIDE }, scene);
			skydome.position.y = 500;
			skydome.isPickable = false;
			skydome.receiveShadows = true;
			const sky = new BABYLON.BackgroundMaterial('skyMaterial', scene);
			sky.reflectionTexture = scene.environmentTexture.clone();
			sky.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
			sky.enableGroundProjection = true;
			sky.projectedGroundRadius = 20;
			sky.projectedGroundHeight = 3;
			skydome.material = sky;

			var camera = new BABYLON.ArcRotateCamera('camera1', 0, 0, 10, new BABYLON.Vector3(0, 0, 0), scene);
			camera.beta = BABYLON.Tools.ToRadians(60);
			camera.lowerBetaLimit = BABYLON.Tools.ToRadians(0);
			camera.upperBetaLimit = BABYLON.Tools.ToRadians(80);
			camera.lowerRadiusLimit = 8;
			camera.upperRadiusLimit = 15;
			camera.setTarget(BABYLON.Vector3.Zero());
			camera.attachControl(canvas, false, false);

			var assetsManager = new BABYLON.AssetsManager(scene);
			checkerboardTask = assetsManager.addMeshTask(
				'checkboard',
				'',
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/',
				'checkerboard.glb'
			);
			checkerboardTask.onSuccess = function (task) {
				var checkerboard = task.loadedMeshes[0];
				checkerboard.position = new BABYLON.Vector3(0, 0, 0);
				checkerboard.scaling.x = 0.8;
				checkerboard.scaling.z = 0.8;
				const boundingBox = checkerboard.getChildren()[0].getBoundingInfo().boundingBox;
				const cellSize = (Math.max(boundingBox.maximumWorld.x - boundingBox.minimumWorld.x, boundingBox.maximumWorld.z - boundingBox.minimumWorld.z) / 3.0) * 0.8;
				for (let i = 0; i < 3; i++) {
					for (let j = 0; j < 3; j++) {
						const x = boundingBox.minimumWorld.x * 0.8 + i * cellSize + cellSize / 2;
						const z = boundingBox.minimumWorld.z * 0.8 + j * cellSize + cellSize / 2;

						const cell = {
						position: new BABYLON.Vector3(x, boundingBox.maximumWorld.y, z),
						occupied: false,
						};
						cells.push(cell);
					}
				}
			};
			circleTask = assetsManager.addMeshTask(
				'circle',
				'',
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/',
				'circle.glb'
			);
			circleTask.onSuccess = function (task) {
				task.loadedMeshes[0].setEnabled(false);
			};
			crossTask = assetsManager.addMeshTask(
				'cross',
				'',
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/',
				'cross.glb'
			);
			crossTask.onSuccess = function (task) {
				task.loadedMeshes[0].setEnabled(false);
			};
			assetsManager.onFinish = function (tasks) {
				canvas.addEventListener('click', (event) => {
					if (!turn) return;
					var pickResult = scene.pick(scene.pointerX, scene.pointerY);
					if (pickResult.hit && pickResult.pickedMesh && pickResult.pickedMesh.name === 'Checkerboard') {
						const closestCell = vm.findClosestCell(pickResult.pickedPoint);
						if (!closestCell.occupied) vm.makeMove(closestCell.index);
					}
				});
				engine.runRenderLoop(() => {
					scene.render();
				});
				window.addEventListener('resize', () => {
					engine.resize();
				});
			};
			assetsManager.load();
			return scene;
		},
	},
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