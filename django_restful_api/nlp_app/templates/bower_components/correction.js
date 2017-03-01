'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:CorrectionCtrl
 * @description
 * # CorrectionCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('CorrectionCtrl', ['$scope', '$http', function ($scope, $http) {
        var resultList = ['自然语言处理网站', '自然语言处理照片', '自然语言处理', '自然语言编程', '自然语言处理结果', '自来水', '独自'];

        $scope.inputText = '';
        $scope.focusText = '';
        $scope.searchResult = [];
        $scope.getCrawlerResult = function () {
            $scope.flag1 = true
            var data = {
                url: $scope.formData.inputUrl
            };
            if ($scope.formData.inputUrl != '') {
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/crawler',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.errorText = data;
                    $scope.flag1 = false;
                })
                    .error(function (data) {
                        $scope.errorText = data;
                        $scope.flag1 = false;
                    });
            }
        };
        $scope.search = function () {
            $scope.searchResult = [];
            $scope.focusText = '';
            if ($scope.inputText != '') {
                var i = 0;
                angular.forEach(resultList, function (res) {
                    if (res.indexOf($scope.inputText) >= 0) {
                        $scope.searchResult[i] = res;
                        i++;
                    }
                });
                $scope.focusText = '自然语言处理';
            }
        }

        $scope.errorText = '';
        $scope.mybeText = '';
        $scope.getResult = function () {
            if ($scope.errorText != '') {
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/aec',
                    data: "q=" + $scope.errorText,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.first = true;
                    $scope.mybeText = data;
                })
                    .error(function (data) {
                        $scope.first = true;
                        $scope.mybeText = '';
                    });
            }
        }
    }]);
