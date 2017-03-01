'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:EmotionCtrl
 * @description
 * # EmotionCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('EmotionCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.formData = {
            a: 'emotion',
            inputText: ''
        }
        $scope.results = [];
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
            var count = 2;
            $scope.chartConfig.series[0].data = [];
            var data1 = {
                text: $scope.inputText,
                type: "senti"
            };
            var data2 = {
                q: $scope.inputText,
            };
            console.log(data1);
            if ($scope.inputText != '') {
                $scope.flag = true;
                console.log('emotion http started!')
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/emotion',
                    //url: 'http://172.18.1.146:11004/emotion',
                    data: $.param(data1),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    var positive_prob = 0
                    var senti1_name = data[0][0]
                    var senti1_value = parseFloat(data[0][1])
                    var senti2_value = parseFloat(data[1][1])
                    if (senti1_name == '正面') {
                        positive_prob = senti1_value
                    }
                    else {
                        positive_prob = senti2_value
                    }

//                    var positive_prob = parseFloat(data['positive_prob']);
                    $scope.chartConfig.series[0].data = [{name: '积极', y: positive_prob}, {
                        name: '消极',
                        y: 1 - positive_prob
                    }];
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
                    });

                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/reputation',
                    //url: 'http://172.18.1.146:11003/reputation',
                    data: $.param(data2),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    for (var i = 0; i < data.length; i++) {
                        if (data[i].subsentence.length > 10) {
                            data[i].subsentence = data[i].subsentence.slice(0, 10);
                        }
                        data[i].subsentence = data[i].subsentence.join("<br/>");
                    }
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
            }
//            angular.forEach(data, function(tdata, key) {
//                var rand = Math.floor(Math.random() * 20);
//                data[key]['weight'] = rand;
//            });
//            $scope.results = data;
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
