var express = require('express');
var router = express.Router();
var socket = require('../service/socket')
var serial = require('../service/serial')

/* GET users listing. */
router.get('/', function (req, res, next) {
  serial.on('data', function (data) {
    console.log(data)
    socket.sendData(data.toString().split('\t'))
  });

  res.json({
    msg: "This is socket path.. There is nothing to do here.."
  })
});

module.exports = router;