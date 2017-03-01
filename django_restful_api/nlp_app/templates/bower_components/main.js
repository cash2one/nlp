'use strict';

/**
 * @ngdoc function
 * @name demoApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the demoApp
 */
angular.module('demoApp')
    .controller('MainCtrl', ['$scope', 'menus', function ($scope, menus) {
        var icons = {
            textanalysis: {
                'classify': '06',
                'emotion': '08',
                'summary': '10',
                'mutilang': '03',
                'library': '22',
                'correction': '20',
                'clustering': '16',
                'extract': '18',
                'translate': '50',
                'distinct': '53'
            },
            videoimage: {'celebrity': '30', 'sentiments': '35', 'text': '33', 'sexage': '28'},
            audiofrequency: {'voice': '42', 'voiceprint': '45', 'soundeffect': '48'},
        };
        var dess = {
            audiofrequency: {
                'voice': '将语音转换为文本。该API 可以直接打开并识别来自麦克风的实时语音，可以通过实时流将语音传送到服务器，服务器再将部分识别结果传送回来',
                'voiceprint': '使用你的声音进行身份验证。此API可以使应用具备智能验证功能，用声音来核实用户身份。 想要了解它的工作原理，请从给定的短语列表中选取一段短语。',
                'soundeffect': '识别谁在讲话。此API可以用于识别未知讲话人的身份。在给定一组说话人的情况下，声纹辨识能够自动辨识出音频文件中的说话人的身份。'
            }
        };
        $scope.models = {};
        angular.forEach(menus, function (menu, key) {
            var _tmp_menu = menu.sonMenus;
            angular.forEach(_tmp_menu, function (_menu, _key) {
                var _merge = {'icon': icons[key][_key]};
                if (dess[key]) {
                    _merge.des = dess[key][_key];
                }
                _tmp_menu[_key] = angular.merge(_menu, _merge);
            });
            if (_tmp_menu.length !== 0) {
                $scope.models[key] = _tmp_menu;
            }
        });
    }]);
