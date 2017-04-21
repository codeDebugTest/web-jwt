'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
        'ngRoute',
        'ngResource',
        'myApp.login',
        'myApp.loading'
    ])
    .config(['$routeProvider', '$httpProvider', function ($routeProvider, $httpProvider) {
        $httpProvider.interceptors.push('httpInterceptor');

        $routeProvider.when("/", {
            controller: 'loginCtrl',
            templateUrl: 'login/login.html'
        }).when('/loading', {
            controller: 'loadingAppCtrl',
            templateUrl: 'loading/loading.html'
        }).otherwise({
            redirectTo: '/'
        });
    }])
    .controller('appCtrl', function ($scope, $location) {
        $location.path('/login');
    });
