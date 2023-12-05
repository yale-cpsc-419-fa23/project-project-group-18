<template>
	<div id="gameContainer">
		<canvas id="renderCanvas" ref="renderCanvas"></canvas>
	</div>
</template>

<script>
	import * as BABYLON from 'babylonjs';
	import 'babylonjs-loaders';
	import { ref } from 'vue';
	import { useRouter } from 'vue-router';
	import LoadingScreen from '../scripts/LoadingScreen.js';
	
	const router = useRouter();
	const gameType = ref('');
	let cells = [];
	let engine, scene, currentPiece, player_id, room_id;
	let gomokuboardTask, pieceTask, turn, vm;
	export default {
    props: ['socket', 'player_id', 'room_id', 'message'],
	data() {
		return {
			
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
			var loadingScreen = new LoadingScreen("I'm loading!!");
			engine.loadingScreen = loadingScreen;
			engine.displayLoadingUI();
			
			scene = this.createScene(canvas, engine);

			this.$nextTick(() => {
				let userName = localStorage.getItem('userName') || '';
				if (userName != '')
					player_id = userName;
				else
					player_id = this.player_id;
				room_id = this.room_id;
				this.socket.on('gamestart_message', (data) => {
				this.updateMessage(data.message);
				currentPiece = data.piece_map[player_id];
				this.run();
				});
			});
		},
		run() {
			this.socket.on('turnstart_message', (data) => {
				if (data.turn === currentPiece) {
				this.enableCellClickEvents();
				this.updateMessage(data.message + ', make a move.');
				} else {
				this.updateMessage(data.message + ', waiting for opponent...');
				}
			});

			this.socket.on('turnend_message', (data) => {
				this.updateState(data);
			});

			this.socket.on('gameover_message', (data) => {
				this.endGame(data);
			});
		},
		makeMove(index) {
			this.disableCellClickEvents();
			this.socket.emit('makemove', { player_id: player_id, room_id: room_id, index: index });
		},
		updateState(data) {
			this.placePiece(data.index, data.turn);
		},
		endGame(data) {
			const winner = data.winner;
			if (winner === '') {
				this.updateMessage('Tie!');
			} else if (winner === player_id) {
				this.updateMessage('You Win!');
			} else {
				this.updateMessage('You Lose!');
			}
			this.disableCellClickEvents();
			this.$emit('showLeave');
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
			for (var i = 0; i < 225; i++) {
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
			if (piece == 'White') {
				var newPiece = pieceTask.loadedMeshes[0].getChildren()[0].createInstance();
			} else if (piece == 'Black') {
				var newPiece = pieceTask.loadedMeshes[1].getChildren()[0].createInstance();
			}
			newPiece.position = position;
			newPiece.scaling.x /= 5.0;
			newPiece.scaling.y *= 0.3;
			newPiece.scaling.z /= 5.0;
		},
		updateMessage(newMessage) {
			this.$emit('updateMessage', newMessage);
		},
		createScene(canvas, engine) {
			var scene = new BABYLON.Scene(engine);

			scene.environmentTexture = BABYLON.CubeTexture.CreateFromPrefilteredData(
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/textures/environment.env',
				scene
			);
			const skydome = BABYLON.MeshBuilder.CreateBox('sky', { size: 2000, sideOrientation: BABYLON.Mesh.BACKSIDE }, scene);
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
			gomokuboardTask = assetsManager.addMeshTask(
				'gomokuboard',
				'',
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/',
				'gomokuboard.glb'
			);
			gomokuboardTask.onSuccess = function (task) {
				var gomokuboard = task.loadedMeshes[0];
				gomokuboard.position = new BABYLON.Vector3(0, 0, 0);
				gomokuboard.scaling.x = 2;
				gomokuboard.scaling.z = 2;
				const boundingBox = gomokuboard.getChildren()[0].getBoundingInfo().boundingBox;
				const cellSize = (Math.max(boundingBox.maximumWorld.x - boundingBox.minimumWorld.x, boundingBox.maximumWorld.z - boundingBox.minimumWorld.z) / 15.0) * 2;
				for (let i = 0; i < 15; i++) {
					for (let j = 0; j < 15; j++) {
						const x = boundingBox.minimumWorld.x * 2 + i * cellSize + cellSize / 2;
						const z = boundingBox.minimumWorld.z * 2 + j * cellSize + cellSize / 2;

						const cell = {
						position: new BABYLON.Vector3(x, boundingBox.maximumWorld.y, z),
						occupied: false,
						};
						cells.push(cell);
					}
				}
			};
			pieceTask = assetsManager.addMeshTask(
				'piece',
				'',
				'https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/beta/instaGame/src/assets/models/',
				'piece.glb'
			);
			pieceTask.onSuccess = function (task) {
				task.loadedMeshes[0].setEnabled(false);
				task.loadedMeshes[1] = task.loadedMeshes[0].clone();
				pieceTask.loadedMeshes[0].getChildren()[0].material = pieceTask.loadedMeshes[0].getChildren()[0].material.clone();
				pieceTask.loadedMeshes[0].getChildren()[0].material.albedoColor = BABYLON.Color3.FromHexString("#FFFFFF");
			};
			assetsManager.onFinish = function (tasks) {
				canvas.addEventListener('dblclick', (event) => {
					if (!turn) return;
					var pickResult = scene.pick(scene.pointerX, scene.pointerY);
					if (pickResult.hit && pickResult.pickedMesh && pickResult.pickedMesh.name === 'GomokuBoard') {
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
	#gameContainer {
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
</style>