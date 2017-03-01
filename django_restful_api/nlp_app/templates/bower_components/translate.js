'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:CorrectionCtrl
 * @description
 * # CorrectionCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('TranslateCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.tradition2simple = true;
        $scope.han2pin = true;
        $scope.getCrawlerResult1 = function () {
            $scope.flag3 = true
            var data = {
                url: $scope.formData.inputUrl1
            };
            if ($scope.formData.inputUrl1 != '') {
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/crawler',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.inputText = data;
                    $scope.flag3 = false;
                })
                    .error(function (data) {
                        $scope.inputText = '';
                        $scope.flag3 = false;
                    });
            }
        };
        $scope.getCrawlerResult2 = function () {
            $scope.flag4 = true
            var data = {
                url: $scope.formData.inputUrl2
            };
            if ($scope.formData.inputUrl2 != '') {
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/crawler',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.inputText1 = data;
                    $scope.flag4 = false;
                })
                    .error(function (data) {
                        $scope.inputText1 = '';
                        $scope.flag4 = false;

                    });
            }
        };
        $scope.getResult = function () {
            var data = {
                style: $scope.tradition2simple ? 'tradition2simple' : 'simple2tradition',
                q: $scope.inputText
            };
            if ($scope.inputText != '') {
                $scope.flag = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/simple2tradition',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.outputText = data;
                    $scope.flag = false;
                })
                    .error(function (data) {
                        $scope.outputText = data;
                        $scope.flag = false;
                    });
            }
        };
        $scope.getHpResult = function () {
            if ($scope.inputText != '') {
                var data = {
                    style: $scope.han2pin ? 'han2pin' : 'han2pin',
                    q: $scope.inputText1
                };
                $scope.flag1 = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/py',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.outputText1 = data.join(" ");
                    $scope.flag1 = false;
                })
                    .error(function (data) {
                        $scope.outputText1 = [];
                        $scope.flag1 = false;
                    });
            }
        };
    }]);
