'use strict';
angular.module('myApp')
    .factory('authService', function($resource, apiAddress, $q) {
        var _login = (function () {
            return $resource(apiAddress + "/sumscope_login", {}, {
                post: {method: 'POST', params: {}, isArray: false}
            });
        })();
        var _refreshToken = (function () {
            return $resource(apiAddress + '/refresh_token', {}, {
                post: {method: 'POST', params: {}, isArray: false}
            })
        })();
        var _setAuthorizationData = function (data) {
            if (data.access_token) {
                sessionStorage.setItem('access_token', data.access_token);
            }
            if (data.refresh_token) {
                sessionStorage.setItem('refresh_token', data.refresh_token);
            }
        };
        return {
            login: function(name, password) {
                var deferred = $q.defer();
                _login.post({account_name: name, password: password}, function success (response) {
                    _setAuthorizationData(response);
                    deferred.resolve(response);
                }, function failed () {
                    deferred.reject();
                });

                return deferred.promise;
            },
            refreshToken: function() {
                var deferred = $q.defer();
                _refreshToken.post({}, function success(data) {
                    _setAuthorizationData(data);
                    deferred.resolve();
                }, function failed() {
                    deferred.reject()
                });
                return deferred.promise;
            },
            clear: function() {
                sessionStorage.removeItem('access_token');
                sessionStorage.removeItem('refresh_token');
            }
        }
    })
    .factory('httpInterceptor', function($q, $injector, $location) {
        var _httpRequest = function(config) {
            if (config.url.indexOf('refresh_token') != -1) {
                config.headers.Authorization = sessionStorage.getItem('refresh_token');
            } else {
                config.headers.Authorization = sessionStorage.getItem('access_token');
            }
            return config
        };
        var _responseError = function(rejection) {
            if (401 === rejection.status){
                var deferred = $q.defer();
                var authService = $injector.get('authService');
                authService.refreshToken().then(function success() {
                    // 消息重发
                    $injector.get("$http")(rejection.config).then(function(resp) {
                        deferred.resolve(resp);
                    },function() {
                        deferred.reject();
                    });
                }, function failed() {
                    deferred.reject();
                    $location.path('/login');
                });
                return deferred.promise;
            }
            return $q.reject(rejection);
        };

        return {
            request: _httpRequest,

            responseError: _responseError
        }
    });