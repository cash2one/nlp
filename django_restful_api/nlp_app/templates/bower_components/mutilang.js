'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:MutilangCtrl
 * @description
 * # MutilangCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('MutilangCtrl', ['$scope', '$http', function ($scope, $http) {
//    $scope.cates = [];
        $scope.formData = {
            a: 'mutilang',
            inputText: ''
        }
        $scope.results = [];
        $scope.myCate = '游戏';
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
                        $scope.flag1 = false;
                    });
            }
        };
        $scope.getResult = function () {
            var count = 4;
            var data = {
                text: $scope.inputText
            };
            if ($scope.inputText != '') {
//        $scope.first = true;
                $scope.flag = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/lang',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.outputText = data;
                    count--;
                    if (!count) {
                        $scope.first = true;
                        $scope.flag = false;
                    }
                })
                    .error(function (data) {
                        $scope.outputText = '';
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                    });
                data = {
                    text: $scope.inputText,
                    phrase: 'True',
                    nums: '10'
                };
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/keywords2',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                    timeout: 120000
                }).success(function (data) {
                    $scope.results = data;
                    count--;
                    if (!count) {
                        $scope.first = true;
                        $scope.flag = false;
                    }
                })
                    .error(function (data) {
                        $scope.results = [];
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                    });
                data = {
                    text: $scope.inputText,
                    type: 'common'
                }
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/classify',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                    timeout: 120000
                }).success(function (data) {
                    if (data.length) {
                        console.log(data);
                        $scope.cates = [];
                        for (var i = 0; i < data.length; i++) {
                            $scope.cates.push(data[i][0]);
                        }
                        $scope.myCate = data[0][0];
                    }
                    count--;
                    if (!count) {
                        $scope.first = true;
                        $scope.flag = false;
                    }
                })
                    .error(function (data) {
                        $scope.results = [];
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                    });
                data = {
                    text: $scope.inputText,
                    type: 'senti'
                }
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/classify',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                    timeout: 120000
                }).success(function (data) {
//              var positive_prob = parseFloat(data['正面']);
                    $scope.chartConfig.series[0].data = [{
                        name: data[0][0],
                        y: parseFloat(data[0][1])
                    }, {name: data[1][0], y: parseFloat(data[1][1])}];
                    count--;
                    if (!count) {
                        $scope.first = true;
                        $scope.flag = false;
                    }
                })
                    .error(function (data) {
                        $scope.results = [];
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                    });
            }

        }
        $scope.chartConfig = {
            options: {
                chart: {
                    type: 'pie'
                }
            },
            title: {
                text: ''
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                name: '权重',
                colorByPoint: true,
                data: []
            }],
            loading: false
        }

    }]);
