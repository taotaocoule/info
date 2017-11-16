var express = require('express');
var sqlite = require('sqlite3');
var bodyParser = require('body-parser');

var app = express();
var db=new sqlite.Database('database.db');

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', function (req, res) {
  res.sendFile(__dirname+"/public/html/index.html");
});

app.get('/wechat',function(req,res){
	db.all('select * from wechat',function(error,data){
		res.send(data);
	});
});

app.post('/login',function(req,res){
  res.send(req.body);
});

app.listen(3000,function(){
  console.log('Info starting');
});