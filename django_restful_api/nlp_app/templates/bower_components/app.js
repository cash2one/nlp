'use strict';

/**
 * @ngdoc overview
 * @name demoApp
 * @description
 * # demoApp
 *
 * Main module of the application.
 */
angular
    .module('demoApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'ngTable',
        'highcharts-ng',
        'angular-jqcloud',
        'ngDialog'
    ])
    .value('menus', {
        main: {
            name: '首页',
            sonMenus: []
        },
        textanalysis: {
            name: '文本分析',
            sonMenus: {
                library: {name: '分词/词库', alias: '分词、新词和词库'},
                emotion: {name: '情感口碑', alias: '情感口碑'},
                translate: {name: '简繁、汉拼转换', alias: '简繁、汉拼转换'},
                classify: {name: '自定义分类', alias: '自定义分类、标签'},
                summary: {name: '词云摘要', alias: '词云、摘要'},
                correction: {name: '纠错补全', alias: '纠错、补全'},
                clustering: {name: '话题聚类', alias: '话题聚类'},
                extract: {name: '信息抽取', alias: '信息抽取'},
                mutilang: {name: '多语言', alias: '多语言'},
                distinct: {name: '文本去重', alias: '文本去重'}
            }


        },
        videoimage: {
            name: '视频图像',
            sonMenus: {
                celebrity: {name: '名人识别'},
                sentiments: {name: '情绪识别'},
                text: {name: '文字提取'},
                sexage: {name: '性别/年龄/种族场景'}
            }
        },
        audiofrequency: {
            name: '音频',
            sonMenus: {
                voice: {name: '语音识别'},
                voiceprint: {name: '声纹识别'},
                soundeffect: {name: '声音效果'},
            }
        },
    })
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl',
                controllerAs: 'main'
            })
            .when('/textanalysis', {
                templateUrl: 'views/textanalysis.html',
                controller: 'TextanalysisCtrl',
                controllerAs: 'textanalysis'
            })
            .when('/classify', {
                templateUrl: 'views/textanalysis.html',
                controller: 'TextanalysisCtrl',
                controllerAs: 'textanalysis'
            })
            .when('/videoimage', {
                templateUrl: 'views/videoimage.html',
                controller: 'VideoimageCtrl',
                controllerAs: 'videoimage'
            })
            .when('/audiofrequency', {
                templateUrl: 'views/audiofrequency.html',
                controller: 'AudiofrequencyCtrl',
                controllerAs: 'audiofrequency'
            })
            .when('/emotion', {
                templateUrl: 'views/emotion.html',
                controller: 'EmotionCtrl',
                controllerAs: 'emotion'
            })
            .when('/summary', {
                templateUrl: 'views/summary.html',
                controller: 'SummaryCtrl',
                controllerAs: 'summary'
            })
            .when('/mutilang', {
                templateUrl: 'views/mutilang.html',
                controller: 'MutilangCtrl',
                controllerAs: 'mutilang'
            })
            .when('/library', {
                templateUrl: 'views/library.html',
                controller: 'LibraryCtrl',
                controllerAs: 'library'
            })
            .when('/correction', {
                templateUrl: 'views/correction.html',
                controller: 'CorrectionCtrl',
                controllerAs: 'correction'
            })
            .when('/clustering', {
                templateUrl: 'views/clustering.html',
                controller: 'ClusteringCtrl',
                controllerAs: 'clustering'
            })
            .when('/extract', {
                templateUrl: 'views/extract.html',
                controller: 'ExtractCtrl',
                controllerAs: 'extract'
            })
            .when('/translate', {
                templateUrl: 'views/translate.html',
                controller: 'TranslateCtrl',
                controllerAs: 'translate'
            })
            .when('/distinct', {
                templateUrl: 'views/distinct.html',
                controller: 'DistinctCtrl',
                controllerAs: 'distinct'
            })
            .otherwise({
                redirectTo: '/'
            });
    })
    .directive("submitBtn", function () {
        return {
            restrict: "E",        // 指令是一个元素
            scope: {              // 设置指令对于的scope
                text: "@",          // name 值传递
                flag: "=",        // amount 引用传递
                click: '&click',
            },
            template: "<a href='javascript:;' ng-hide='flag' style='background-color: #ff7043;'' ng-click='click()'>" +
            "  {{text}}" +
            "</a>" +
            "<a ng-show='flag' style='background-color:lightgray;'>" +
            " <img src='images/loading.gif' style='height: 20px;'>" +
            "</a>",
            // replace: true,        // 使用模板替换原始标记
            // transclude: false,    // 不复制原始HTML内容
        }
    });
