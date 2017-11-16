var app=angular.module('info',[]);

app.controller('wechat',function($scope,$http){
	$http.get('/wechat').then(function(response){
		$scope.wechatData=response.data;
	});
});