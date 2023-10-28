let board = Array(9).fill(null);
let currentPlayer = 'X';

var socket = io.connect('http://192.168.4.48:5001');

socket.on('message', function(data) {
    console.log(data);  // Log the data received from the server
});

window.makeMove = function(index) {

    console.log(JSON.stringify(JSON.stringify({ index, player: currentPlayer, room:'room1'})))
    socket.emit('join', {username: 'John', room: 'room1', index, player: currentPlayer});
    
    if (board[index] === null) {
            board[index] = currentPlayer;
            document.getElementById('board').children[index].innerText = currentPlayer;
            if (checkWinner()) {
                alert(currentPlayer + ' wins!');
            resetBoard();
        } else {
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        }
    }
}

function checkWinner() {
    const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    return winPatterns.some(pattern => pattern.every(index => board[index] === currentPlayer));
}

function resetBoard() {
    board = Array(9).fill(null);
    Array.from(document.getElementById('board').children).forEach(cell => cell.innerText = '');
}