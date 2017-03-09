'use strict';

/* Controllers */

function AddController($scope, AddTopic, $window)
{
	$scope.add = function(topic)
	{
		AddTopic.post({topic: topic}, function(data)
		{
			$window.location = '/topic/' + data.id;
		});
	}
}


function TopicController($scope, $routeParams, SingleTopic, Upvote, Downvote)
{
	var topicResults = SingleTopic.get({topic_id: $routeParams.topic_id}, function(data){
		$scope.topics = data;
	});

	$scope.upvote = function(topic) {
		Upvote.get({topic_id: topic}, function(data) {
			var topicResults = Topic.get({}, function(data){
				$scope.topics = data;
			});
		});
	}

	$scope.downvote = function(topic) {
		Downvote.get({topic_id: topic}, function(data) {
			var topicResults = Topic.get({}, function(data){
				$scope.topics = data;
			});
		});
	}

}


function HomeController($scope, Topic, Upvote, Downvote, $timeout)
{
	var topicResults = Topic.get({}, function(data){
		$scope.topics = data;
	});

	$scope.upvote = function(topic) {
		Upvote.get({topic_id: topic}, function(data) {
			var topicResults = Topic.get({}, function(data){
				$scope.topics = data;
			});
		});
	}

	$scope.downvote = function(topic) {
		Downvote.get({topic_id: topic}, function(data) {
			var topicResults = Topic.get({}, function(data){
				$scope.topics = data;
			});
		});
	}


	function tick() {
		var topicResults = Topic.get({}, function(data){
			$scope.topics = data;
		});
		var timer = $timeout(tick, 3000);
	}

	tick();

	$scope.$on("destroy", function()
	{
		if(timer) {
			$timeout.cancel(timer);
		}
	});
}

function AllTopicsController($scope, $routeParams, $timeout, AllTopics, $window)
{
	var topicResults = AllTopics.get({page: $routeParams.page}, function(data) {
        $scope.topics = data;
    });

	$scope.upvote = function(topic) {
		$scope.topics[topic].score+=1;
		Upvote.get({topic_id: topic}, function(data) {
			var topicResults = AllTopics.get({page: $routeParams.page}, function(data){
				$scope.topics = data;
			});
		});
	}

	$scope.downvote = function(topic) {
		$scope.topics[topic].score+=1;
		Downvote.get({topic_id: topic}, function(data) {
			var topicResults = AllTopics.get({page: $routeParams.page}, function(data){
				$scope.topics = data;
			});
		});
	}

	$scope.next = function()
	{
		$window.location = '/all/' + (parseInt($routeParams.page) + 1);
	}

	$scope.previous = function()
	{	if($routeParams.page > 1)
			$window.location = '/all/' + (parseInt($routeParams.page) - 1);
	}

}

