var socket_io = require('socket.io');
var io = socket_io();
io.origins('*:*')
var socketApi = {};
var namespace = io.of('/web');
socketApi.io = io;
socketApi.namespace = namespace;

io.on('connection', function (socket) {
    console.log('A user connected');
});

socketApi.sendData = function (data) {
    namespace.emit('livedata', {
        msg: data
    });
};

module.exports = socketApi;