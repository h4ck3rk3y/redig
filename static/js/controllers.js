'use strict';

/* Controllers */

function AddController($scope, AddTopic, $window)
{
	$scope.add = function(topic)
	{
		AddTopic.post({topic: topic}, function(data)
		{
			$window.location = '/topic/' + data.id;
		})
	}
}


function TopicController($scope, $routeParams, SingleTopic){
	var topicResults = SingleTopic.get({topic_id: $routeParams.topic_id}, functions(data){
		$scope.topic = data;
	});
}


function HomeController($scope, Topic, Upvote, Downvote, $timeout)
{
	var topicResults = Topic.get({}, functions(data){
		$scope.topics = data.topics;
	});

	$scope.upvote = function(topic) {
		Upvote.get({topic_id: topic}, function(data) {
			var topicResults = Topic.get({}, functions(data){
				$scope.topics = data.topics;
			});
		});
	}

	$scope.downvote = function(topic) {
		Downvote.get({topic_id: topic}, function(data) {
			var topicResults = Topic.get({}, functions(data){
				$scope.topics = data.topics;
			});
		});
	}


	function tick() {
		var topicResults = Topic.get({}, functions(data){
			$scope.topics = data.topics;
		});
		var timer = $timeout(tick, 3000);
	}

	tick();

	$scope.$on("destroy", function())
	{
		if(timer) {
			$timeout.cancel(timer);
		}
	}
}

function AllTopicsController($scope, $routeParams, $timeout, AllTopics, )
{
	var topicResults = AllTopics.get({page: $routeParams.page}, function(data) {
        $scope.data = data;
    });

	$scope.upvote = function(topic) {
		$scope.topics[topic].score+=1;
		Upvote.get({topic_id: topic}, function(data) {
			var topicResults = AllTopics.get({page: $routeParams.page}, functions(data){
				$scope.topics = data.topics;
			});
		});
	}

	$scope.downvote = function(topic) {
		$scope.topics[topic].score+=1;
		Downvote.get({topic_id: topic}, function(data) {
			var topicResults = AllTopics.get({page: $routeParams.page}, functions(data){
				$scope.topics = data.topics;
			});
		});
	}
}

