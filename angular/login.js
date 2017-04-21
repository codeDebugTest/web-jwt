'use strict';

angular.module('myApp.login', ['ngRoute'])
    .controller('loginCtrl', function ($scope, $location, loginInfo, authService, messageBox) {
        $scope.user = {
            login_name: "",
            password: ""
        };

        $scope.loginServer = function () {
            authService.login($scope.user.login_name, $scope.user.password).then(function success(data) {
                if (data.message != 'success') {
                    messageBox.error(data.message);
                } else {
                    loginInfo.super = data.super;
                    $location.path('/loading');
                }
            }, function failed() {
            });
        };

        $scope.$on('$destroy', function() {
          $scope = null;
        });
    });
