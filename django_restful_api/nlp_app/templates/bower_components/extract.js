'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:ExtractCtrl
 * @description
 * # ExtractCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('ExtractCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.results = {
            'entity': [],
            'relation': [],
            'events': [],
        }
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
                    $scope.formData.inputText = data;
                    $scope.flag1 = false;
                })
                    .error(function (data) {
                        $scope.formData.inputText = '';
                        $scope.flag1 = false;
                    });
            }
        };
        $scope.getResult = function () {
            $scope.flag = true;
            $scope.first = true;
            var data = {
                q: $scope.formData.inputText
            };
            if ($scope.formData.inputText != '') {
                $http({
                    method: 'POST',
                    url: 'http://ai.baifendian.com/eventextract',
                    data: $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                }).success(function (data) {
                    $scope.results = data;
                    $scope.flag = false;
                })
                    .error(function (data) {
                        $scope.results = data;
                        $scope.flag = false;
                    });
            }
//  	  $scope.results = {
////  		'entity': [
////  			{'name': '王石', 'type': '人物'},
////  			{'name': '万科', 'type': '公司'},
////  			{'name': '王健林', 'type': '人物'},
////  			{'name': '万达', 'type': '公司'},
////  			{'name': '张继科', 'type': '人物'},
////  		],
////  		'relation': [
////  			{'name': '钜盛华', 'name1': '宝能', 'type': '子公司'},
////  			{'name': '华润', 'name1': '万科', 'type': '股东'},
////  			{'name': '钜盛华', 'name1': '宝能', 'type': '子公司'},
////  			{'name': '华润', 'name1': '万科', 'type': '股东'},
////  			{'name': '钜盛华', 'name1': '宝能', 'type': '子公司'}
////  		],
//  		'events': [
//  			{'事件': '霍顿讽刺孙杨', '地点': '里约', '实施者': '霍顿', '受害者': '孙杨', '类型': '体育','状态': '霍顿', '原因': '体育', '结果': '体育', '金钱': '0', '备注': '无'},
//  			{'name': '张梦雪首金', 'date': '2016-08-06', 'place': '里约', 'executor': '张梦雪', 'patient': '张梦雪', 'type': '体育','status': '张梦雪', 'reason': '体育', 'result': '体育', 'money': '0', 'casualties': '无'},
//  			{'name': '伏明霞五冠', 'date': '2016-08-06', 'place': '里约', 'executor': '伏明霞', 'patient': '伏明霞', 'type': '体育','status': '伏明霞', 'reason': '体育', 'result': '体育', 'money': '0', 'casualties': '无'},
//  			{'name': '傅园慧段子手', 'date': '2016-08-06', 'place': '里约', 'executor': '傅园慧', 'patient': '傅园慧', 'type': '体育','status': '傅园慧', 'reason': '体育', 'result': '体育', 'money': '0', 'casualties': '无'},
//  			{'name': '王思聪', 'date': '2016-08-06', 'place': '北京', 'executor': '王思聪', 'patient': '王思聪', 'type': '体育','status': '王思聪', 'reason': '体育', 'result': '体育', 'money': '0', 'casualties': '无'}
//  		],
//  		'ths':['事件','日期','地点','实施者','受害者','类型','状态', '原因', '结果', '金钱', '备注'],
//  	  }
        }

    }]);
