'use strict';

angular.module('AngularFlask', ['angularFlaskServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/list.html',
			controller: HomeController
		})
		.when('/add',{
			templateUrl: 'static/partials/add.html',
			controller: AddController
		})
		.when('/all/:page', {
			templateUrl: '/static/partials/all.html',
			controller: AllTopicsController
		})
		.when('/topic/:topic_id', {
			templateUrl: '/static/partials/topic.html',
			controller: TopicController
		})
		.when('/about', {
			templateUrl: '/static/partials/about.html',
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
	.filter('clean_date', function() {
	return function(input) {
		if(input != undefined)
			return input.replace('GMT', '');
		else
			return '';
	}
});