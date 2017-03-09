'use strict';

angular.module('angularFlaskServices', ['ngResource'])
	.factory('AddTopic', function($resource){
		return $resource('/api/topics/', {}, {
			post: {
				method: 'POST',
			}
		})
	})
	.factory('SingleTopic', function($resource){
		return $resource('/api/topics/:topic_id', {}, {
			query : {
				method: 'GET',
				params: {'topic_id': ''}
			}
		})
	})
	.factory('Topic', function($resource){
		return $resource('/api/topics/top', {}, {
			query : {
				method: 'GET',
			}
		})
	})
	.factory('Upvote', function($resource){
		return $resource('/api/topics/upvote/:topic_id', {}, {
			query : {
				method: 'GET',
				params: {'topic_id': ''}
			}
		})
	})
	.factory('Downvote', function($resource){
		return $resource('/api/topics/downvote/:topic_id', {}, {
			query : {
				method: 'GET',
				params: {'topic_id': ''}
			}
		})
	})
	.factory('AllTopics', function($resource){
		return $resource('/api/topics/all/:page', {}, {
			query : {
				method: 'GET',
				params: {'page': ''}
			}
		})
	})
;



