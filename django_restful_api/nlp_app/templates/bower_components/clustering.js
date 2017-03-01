'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:ClusteringCtrl
 * @description
 * # ClusteringCtrl
 * Controller of the demoApp
 */
// http://www.highcharts.com/demo/bubble/
angular.module('demoApp')
    .controller('ClusteringCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.results = [];
        $scope.colors = ["#ffcccb", "#67ccaa", "#ff9899", "#ffcb99", "#4dd9e6", "#8e8b8b", "#9acccd", "#ccc", "#67a6d9", "#f48363", "#d07f7f", "#99cc67", "#cee887", "#986699", "#488fce", "#8ea4de", "#c7aee7", "#c9aaca", "#8bc3f5"];
        $scope.types = [];
        $scope.getResult = function () {
            $scope.types = [];
            if ($scope.inputText != '') {
//            console.log($scope.inputText);
                var data = {
                    q: $scope.inputText.replace(/\n/g, "^^")
                };
//            console.log(data);
                $scope.flag = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/cluster/',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.results = data;
                    var charData = [];
                    $scope.cates = [];
                    angular.forEach(data, function (tdata, key) {
                        var rand = Math.floor(Math.random() * 20);
                        var cate = tdata[1].slice(0, 3);
//                    charData.push({ x: rand, y: rand + 10, z: tdata[0].length, num: key + 1, name: cate});
                        $scope.cates.push(cate);
                        for (var x in cate) {
                            $scope.types.push(cate[x]);
                        }
                    });

//                $scope.chartConfig.series[0].data = charData;
                    $scope.flag = false;
                    $scope.first = true;
                })
                    .error(function (data) {
                        $scope.results = [];
                        $scope.cates = [];
                        $scope.flag = false;
                        $scope.first = true;
                    });
            }
        };
        $scope.getColor = function (type) {
            var len = $scope.colors.length;
            return $scope.colors[$scope.types.indexOf(type) % len];
        };
//    $scope.chartConfig = {
//        options: {
//          chart: {
//              type: 'bubble',
//              plotBorderWidth: 1,
//              zoomType: 'xy'
//          }
//        },
//        legend: {
//            enabled: false
//        },
//        title: {
//            text: null
//        },
//        xAxis: {
//            gridLineWidth: 0,
//            title: {
//                text: null
//            },
//            labels: { enabled: false }
//        },
//        yAxis: {
//            gridLineWidth: 0,
//            startOnTick: false,
//            endOnTick: false,
//            title: {
//                text: null
//            },
//            labels: { enabled: false }
//        },
//        tooltip: {
//            useHTML: true,
//            headerFormat: '<table>',
//            pointFormat: '<tr><th colspan="2"><h3>{point.name}</h3></th></tr>' +
//                '<tr><th>文章数: </th><td>{point.num}g</td></tr>',
//            footerFormat: '</table>',
//            followPointer: true
//        },
//        plotOptions: {
//            series: {
//                dataLabels: {
//                    enabled: true,
//                    format: '{point.num}'
//                }
//            }
//        },
//        series: [{
//            data: []
//        }]
//    }

    }]);
