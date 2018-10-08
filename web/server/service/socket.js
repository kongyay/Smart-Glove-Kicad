var socket_io = require('socket.io');
var io = socket_io();
var socketApi = {};

socketApi.io = io;

io.on('connection', function (socket) {
    console.log('A user connected');
});

socketApi.sendData = function (data) {
    io.sockets.emit('livedata', {
        msg: data
    });
};

module.exports = socketApi;