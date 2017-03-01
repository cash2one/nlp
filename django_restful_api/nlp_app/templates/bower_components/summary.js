'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:SummaryCtrl
 * @description
 * # SummaryCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('SummaryCtrl', ['$scope', '$http', function ($scope, $http) {

        $scope.inputText = ''
        $scope.results = [];
        $scope.textSummary = '';
        $scope.wordcloud = '';
//        $scope.colors = ["#ffcccb", "#67ccaa", "#ff9899", "#ffcb99", "#4dd9e6", "#8e8b8b", "#9acccd", "#ccc", "#67a6d9", "#f48363", "#d07f7f", "#99cc67", "#cee887", "#986699", "#488fce", "#8ea4de", "#c7aee7", "#c9aaca", "#8bc3f5" ];
        $scope.types = [];
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
                    $scope.inputText = data;
                    $scope.flag1 = false;
                })
                    .error(function (data) {
                        $scope.inputText = '';
                        $scope.falg1 = false;
                    });
            }
        };
        $scope.getResult = function () {
            if ($scope.inputText != '') {
                var count = 2;
                $scope.flag = true;
                $scope.first = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/summary',
                    data: "q=" + $scope.inputText,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.textSummary = data.task_as;
                    count--;
                    if (!count) {
                        $scope.first = true;
                        $scope.flag = false;
                    }
                })
                    .error(function (data) {
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                        $scope.textSummary = [];
                    });
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/key',
                    data: "q=" + $scope.inputText,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    count--;
                    if (!count) {
                        $scope.first = true;
                        $scope.flag = false;
                    }
                    $scope.results = data.task_pd;
                    for (var i = $scope.results.length; i < 10; i++)
                        $scope.results.push(['', '']);
                    var words = [];
                    angular.forEach(data.task_pd, function (item, index) {
                        words.push({text: item[0], weight: item[1] * 100});
                    });
                    $scope.words = words;
                })
                    .error(function (data) {
                        $scope.results = [];
                        $scope.words = [];
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                    });
//                $http({
//                    method: 'POST',
//                    url: 'http://ai.baifendian.com:22225/topic_words',
//                    data: "q=" + $scope.inputText,
//                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
//                }).success(function(data) {
//                    count--;
//                    if(!count){
//                      $scope.first = true;
//                      $scope.flag = false;
//                    }
//                    $scope.topic_words = data;
//                    $scope.types = data;
//                })
//                .error(function(data) {
//                  $scope.topic_words = [];
//                  count--;
//                  if(!count){
//                    $scope.first = true;
//                    $scope.flag = false;
//                  }
//                });
            }
        }
//        $scope.getColor = function(type) {
//          var len = $scope.colors.length;
//          return $scope.colors[$scope.types.indexOf(type) % len];
//        };

    }]);
