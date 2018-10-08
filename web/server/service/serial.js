var serial = {};
var SerialPort = require('serialport');
var Readline = SerialPort.parsers.Readline;
var port = new SerialPort('/COM3', {
    baudRate: 57600,
    dataBits: 8,
    parity: 'none',
    stopBits: 1
});
const parser = port.pipe(new Readline());

parser.on('error', function (err) {
    console.log(`Serial port: ${err}`);
});

module.exports = parser;