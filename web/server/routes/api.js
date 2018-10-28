var express = require('express');
var router = express.Router();


/* GET users listing. */
router.get('/', function (req, res, next) {


  res.json({
    msg: "This is socket path.. There is nothing to do here.."
  })
});

module.exports = router;