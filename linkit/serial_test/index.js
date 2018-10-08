#!/usr/bin/env node
//---------------------------------------------------------------
var SerialPort = require("serialport").SerialPort;
var Readline = SerialPort.parsers.Readline;
var port = new SerialPort("/dev/ttyS0", {
  baudRate: 57600,
  dataBits: 8,
  parity: "none",
  stopBits: 1
});
const parser = port.pipe(new Readline());

parser.on("error", function(err) {
  console.log("Serial port: " + err);
});

parser.on("data", function(data) {
  data = data.toString();
  console.log(data);
});

//---------------------------------------------------------------
var url = require("url");
var http = require("http");
var fs = require("fs");

var page = fs.readFileSync("page.html").toString(); // read file

http
  .createServer(
    function(req, resp) {
      var params = url.parse(req.url, true).query;
      resp.writeHead(200, { "content-type": "text/html" });
      resp.write(page);
      //resp.write('<br>URL: ' + req.url );
      //for (var key in params) {
      //    resp.write('<br> ' + key + ' : ' + params[key] );
      //}
      resp.end();

      if (params["led"] != null) {
        var state = params["led"];
        if (state == "1" || state == "on") {
          ser.write("led 1\n"); // send cmd string to Arduino
        } else if (state == "0" || state == "off") {
          ser.write("led 0\n"); // send cmd string to Arduino
        }
      }
    }.bind(this)
  )
  .listen(8080);

console.log("Listening on port 8080 ...");
//----------------------------------------------------------
