'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:LibraryCtrl
 * @description
 * # LibraryCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('LibraryCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.formData = {
            a: 'mutilang',
            inputText: ''
        }
        $scope.results = [];
        $scope.colors = ["#ffcccb", "#67ccaa", "#ff9899", "#ffcb99", "#4dd9e6", "#8e8b8b", "#9acccd", "#ccc", "#67a6d9", "#f48363", "#d07f7f", "#99cc67", "#cee887", "#986699", "#488fce", "#8ea4de", "#c7aee7", "#c9aaca", "#8bc3f5"];
        $scope.cates = ['会计', '动漫', '医院', '同义词', '大学课程', '明星', '汽车', '电影', '财经', '颜色', '公司名称', '医疗健康', '反义词', '地方', '学校', '歌曲', '游戏', '计算机', '音乐'];
        $scope.myCate = '';
        $scope.cateTotalCount = '';
        $scope.results = [];
        $scope.types = [];
        $scope.getCrawlerResult = function () {
            $scope.flag1 = true;
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
                    $scope.formData.inputText = data;
                    $scope.flag1 = false;
                })
                    .error(function (data) {
                        $scope.formData.inputText = [];
                        $scope.flag1 = false;
                    });
            }
        };
        $scope.getResult = function () {
            $scope.results = [];
            $scope.types = [];
//      $scope.cateTotalCount = Math.floor(Math.random() * 50000);
            var data = {
                style: 'seg_pos',
                q: $scope.formData.inputText
            };
            if ($scope.formData.inputText != '') {
                $scope.flag = true;
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/word_seg',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    angular.forEach(data, function (item, index) {
                        $scope.results.push({name: item[0], name1: item[1]});
                        if (-1 == $scope.types.indexOf(item[1]))
                            $scope.types.push(item[1]);
                    });
                    $scope.first = true;
                    $scope.flag = false;
                })
                    .error(function (data) {
                        $scope.results = [];
                        $scope.types = [];
                    });
            }

//      var idx = Math.floor(Math.random() * 10);
//      $scope.myCate = $scope.cates[idx];
        };
        $scope.getCate = function (cate) {
            $scope.flag2 = true;
            var data = {
                q: cate
            };
            $http({
                method: 'POST',
                url: 'http://ai.baifendian.com/ciku',
                data: $.param(data),
                headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            }).success(function (data) {
                $scope.cateTotalCount = data['count'];
                $scope.results1 = data['words'];
                $scope.flag2 = false;
            })
                .error(function (data) {
                    $scope.cateTotalCount = 0;
                    $scope.results1 = [];
                    $scope.flag2 = false;
                });
        };

        $scope.getColor = function (type) {
            if (type == "地名") return "#ffffff"
            else {
                var len = $scope.colors.length;
                return $scope.colors[$scope.types.indexOf(type) % len];
            }
        };

    }]);
