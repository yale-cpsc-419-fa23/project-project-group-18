import {SERVER_ADDRESS} from './global.js'

var socket;
var currentPiece, opponentPiece;
var player_id, room_id;
var cells = [], pieces = [];
var checkerboardTask, circleTask, crossTask;

function get_cookie(name) {
    // get cookie by name
    let cookieArr = document.cookie.split("; ");
    for(let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0]) {
            return cookiePair[1];
        }
    }
    return null;
}

function run() {
    socket.on('turnstart_message', (data) => {
        if (data.turn == currentPiece) {
            enable_cell_click_events();
            $('#message').html(data.message + ", make a move.");
        }
        else
            $('#message').html(data.message + ", waiting for opponent...");
    });
    socket.on('turnend_message', (data) => {
        update_state(data)
    })
    socket.on('gameover_message', (data) => {
        end_game(data)
    })
}

function make_move(index) {
    disable_cell_click_events();
    console.log(index)
    socket.emit('makemove', {player_id: player_id, room_id: room_id, index: index});
}

function update_state(data) {
    const index = data.index;
    $('#board').children().eq(index).text(data.turn);
    $('#board').children().eq(index).off('click');
}

function end_game(data) {
    const winner = data.winner
    if (winner == "")
        $('#message').html("Tie!");
    else if (winner == player_id)
        $('#message').html("You Win!");
    else
        $('#message').html("You Lose!");
    disable_cell_click_events();
    $('#leave-button').css('display', 'block');
}

function leave_room() {
    socket.disconnect();
    window.location.href = 'lobby.html';
}

function disable_cell_click_events() {
    $('.cell').each(function() {
        $(this).addClass('disabled');
    });
}

function enable_cell_click_events() {
    $('.cell').each(function() {
        $(this).removeClass('disabled');
    });
}

function findClosestCell(point) {
    var idx = 0, min_dist = Infinity;
    for (var i = 0; i < 9; i++)
    {
        var distance = BABYLON.Vector3.Distance(cells[i].position, point);
        if (distance < min_dist)
        {
            min_dist = distance;
            idx = i;
        }
    }
    return {
        index: idx,
        occupied: cells[idx].occupied
    };
}

function placePiece(position) {
    var circle = circleTask.loadedMeshes[0].getChildren()[0].createInstance();
    circle.position = position;
    circle.scaling.x *= 0.6;
    circle.scaling.y *= 0.3;
    circle.scaling.z *= 0.6;
    circle.setEnabled(true);
    var cross = crossTask.loadedMeshes[0].getChildren()[0].createInstance();
    cross.position = position;
    cross.scaling.x *= 0.8;
    cross.scaling.y *= 0.8;
    cross.scaling.z *= 0.3;
    cross.rotationQuaternion = null;
    cross.rotation.x = BABYLON.Tools.ToRadians(90);
    cross.rotation.z = BABYLON.Tools.ToRadians(45);
    pieces.push(circle);
    pieces.push(cross);
}

function createScene(canvas, engine) {
    // Creates a basic Babylon Scene object
    var scene = new BABYLON.Scene(engine);
    scene.environmentTexture = BABYLON.CubeTexture.CreateFromPrefilteredData("https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/mvp/front-end/models/textures/environment.env", scene);
    const skydome = BABYLON.MeshBuilder.CreateBox("sky", { size: 1000, sideOrientation: BABYLON.Mesh.BACKSIDE }, scene);
    skydome.position.y = 500;
    skydome.isPickable = false;
    skydome.receiveShadows = true;
    const sky = new BABYLON.BackgroundMaterial("skyMaterial", scene);
    sky.reflectionTexture = scene.environmentTexture.clone();
    sky.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
    sky.enableGroundProjection = true;
    sky.projectedGroundRadius = 20;
    sky.projectedGroundHeight = 3;
    skydome.material = sky;
    // Creates and positions a free camera
    var camera = new BABYLON.ArcRotateCamera("camera1", 0, 0, 10, new BABYLON.Vector3(0, 0, 0), scene);
    // camera.lowerAlphaLimit = 0
    // camera.upperAlphaLimit = 0
    camera.lowerBetaLimit = BABYLON.Tools.ToRadians(0)
    camera.upperBetaLimit = BABYLON.Tools.ToRadians(80)
    camera.lowerRadiusLimit = 8
    camera.upperRadiusLimit = 15
    
    // Targets the camera to scene origin
    camera.setTarget(BABYLON.Vector3.Zero());
    // This attaches the camera to the canvas
    camera.attachControl(canvas, false, false);
    
    var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");

    var text1 = new BABYLON.GUI.TextBlock();
    text1.text = "Display room status";
    text1.color = "white";
    text1.fontSize = 24;
    advancedTexture.addControl(text1);
    var button = BABYLON.GUI.Button.CreateSimpleButton("but", "Click Me");
    button.width = 0.2;
    button.height = "40px";
    button.color = "white";
    button.background = "green";
    advancedTexture.addControl(button);

    var assetsManager = new BABYLON.AssetsManager(scene);
    checkerboardTask = assetsManager.addMeshTask("checkboard", "", "https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/mvp/front-end/models/", "checkerboard.glb");
    checkerboardTask.onSuccess = function (task) {
        var checkerboard = task.loadedMeshes[0];
        checkerboard.position = new BABYLON.Vector3(0, 0, 0);
        checkerboard.scaling.x = 0.8;
        checkerboard.scaling.z = 0.8;
        const boundingBox = checkerboard.getChildren()[0].getBoundingInfo().boundingBox;
        // TODO adjust boundingbox values
        const cellSize = Math.max(boundingBox.maximumWorld.x - boundingBox.minimumWorld.x, boundingBox.maximumWorld.z - boundingBox.minimumWorld.z) / 3.0 * 0.8;
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
    }
    circleTask = assetsManager.addMeshTask("circle", "", "https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/mvp/front-end/models/", "circle.glb");
    circleTask.onSuccess = function (task) {
        task.loadedMeshes[0].setEnabled(false);
    }
    crossTask = assetsManager.addMeshTask("cross", "", "https://raw.githubusercontent.com/yale-cpsc-419-fa23/project-project-group-18/mvp/front-end/models/", "cross.glb");
    crossTask.onSuccess = function (task) {
        task.loadedMeshes[0].setEnabled(false);
    }
    assetsManager.onFinish = function (tasks) {
        canvas.addEventListener("click", function (event) {
            var pickResult = scene.pick(scene.pointerX, scene.pointerY);
            if (pickResult.hit && pickResult.pickedMesh && pickResult.pickedMesh.name === "立方体") {
                const closestCell = findClosestCell(pickResult.pickedPoint);
                if (!closestCell.occupied) {
                    placePiece(cells[closestCell.index].position);
                    cells[closestCell.index].occupied = true;
                }
            }
        });
        engine.runRenderLoop(function () {
            scene.render();
        });
        window.addEventListener("resize", function () {
            engine.resize();
        });
    };
    assetsManager.load();
    return scene;
};

function initialize() {
    const canvas = document.getElementById('renderCanvas');
    const engine = new BABYLON.Engine(canvas, true); // Generate the BABYLON 3D engine
    const scene = createScene(canvas, engine);
    $("#leave-button").on('click', leave_room);
    player_id = get_cookie("player_id");
    room_id = get_cookie("room_id");
    $('#room_id').html("Room ID: " + room_id);
    socket = io.connect(SERVER_ADDRESS.IP + ':' + SERVER_ADDRESS.PORT);
    socket.emit('joinroom', {player_id: player_id, room_id: room_id});
    socket.on('joinroom_message', (data) => {
        if (data.is_success == true)
            $('#message').html("Waiting for players to join...");
    });
    socket.on('gamestart_message', (data) => {
        $('#message').html(data.message);
        currentPiece = data.piece_map[player_id];
        opponentPiece = currentPiece == 'X' ? 'O' : 'X';
        run();
    });
}

initialize();