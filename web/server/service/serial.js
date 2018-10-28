var serial = {};
var SerialPort = require('serialport');
var Readline = SerialPort.parsers.Readline;
var port = null
connectPort()
const parser = port.pipe(new Readline());

parser.on('error', function (err) {
    console.log(`ERROR Serial port: ${err}`);
    setTimeout(function () {
        console.log('RECONNECTING...');
        connectPort()
    }, 2000);
});
parser.on('close', function (err) {
    console.log(`CLOSED Serial port: ${err}`);
    setTimeout(function () {
        console.log('RECONNECTING...');
        connectPort()
    }, 2000);
});

function connectPort() {
    port = new SerialPort('/COM9', {
        baudRate: 57600,
        dataBits: 8,
        parity: 'none',
        stopBits: 1
    }, (err) => {
        console.log("CAN'T CONNECT SERIALPORT:", err)
    });
}

module.exports = parser;