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
    .controller('DistinctCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.results = [];
        $scope.getResult = function () {
            if ($scope.inputText != '') {
//            console.log($scope.inputText);
                var data = {
                    q: $scope.inputText.replace(/\n/g, "^^")
                };
//            console.log(data);
                $scope.flag = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/different',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.results = data;
                    $scope.flag = false;
                    $scope.first = true;
//                var charData = [];
//                $scope.cates = [];
//                angular.forEach(data, function(tdata, key) {
//                    var rand = Math.floor(Math.random() * 20);
//                    var cate = tdata[1].slice(0,3).join(", ");
//                    charData.push({ x: rand, y: rand + 10, z: tdata[0].length, num: key + 1, name: cate});
//                    $scope.cates.push(cate);
                })
                    .error(function (data) {
                        $scope.results = [];
                        $scope.flag = false;
                        $scope.first = true;
                    });

//                $scope.chartConfig.series[0].data = charData;
//                $scope.flag = false;
//                $scope.first = true;
//            });
            }
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
