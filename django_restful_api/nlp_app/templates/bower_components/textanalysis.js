(function () {
    'use strict';
    /**
     * @ngdoc function
     * @name demoApp.controller:TextanalysisCtrl
     * @description
     * # TextanalysisCtrl
     * Controller of the demoApp
     */
    angular.module('demoApp')
        .controller('TextanalysisCtrl', ["$scope", "$http", "ngTableParams", "ngDialog", function ($scope, $http, ngTableParams, ngDialog) {
            var defaultCates = ['汽车', '体育', '娱乐', '美食', '时尚', '科技', '军事', '母婴/育儿', '医疗/健康', '教育/培训', 'IT/数码'];
            $scope.colors = ["#ffcccb", "#67ccaa", "#ff9899", "#ffcb99", "#4dd9e6", "#8e8b8b", "#9acccd", "#ccc", "#67a6d9", "#f48363", "#d07f7f", "#99cc67", "#cee887", "#986699", "#488fce", "#8ea4de", "#c7aee7", "#c9aaca", "#8bc3f5"];
            $scope.types = [];
            var ngTableSimpleList = [];
            angular.forEach(defaultCates, function (cate) {
                ngTableSimpleList.push({
                    cate: cate,
//	        desc: "这是" + cate + "的描述"
                    desc: ""
                });
            });
            var originalData = angular.copy(ngTableSimpleList);
            $scope.tableParams = new ngTableParams({}, {
                dataset: angular.copy(ngTableSimpleList)
            });

            $scope.deleteCount = 0;
            $scope.add = add;
            $scope.addall = addall;
            $scope.edit = edit;
            $scope.cancelChanges = cancelChanges;
            $scope.del = del;
            $scope.hasChanges = hasChanges;
            $scope.saveChanges = saveChanges;

            function add() {
                $scope.isEditing = true;
                $scope.isAdding = true;
                $scope.tableParams.settings().dataset.unshift({
                    cate: null,
                    desc: null
                });
                // we need to ensure the user sees the new row we've just added.
                // it seems a poor but reliable choice to remove sorting and move them to the first page
                // where we know that our new item was added to
                $scope.tableParams.sorting({});
                $scope.tableParams.page(1);
                $scope.tableParams.reload();
            }

            function addall() {
                ngDialog.open({
                    template: 'dialogId',
                    controller: ['$scope', function ($scope) {
                        $scope.$$prevSibling.tableParams.settings().dataset = [];
                        $scope.$$prevSibling.tableParams.sorting({});
                        $scope.$$prevSibling.tableParams.page(1);
                        $scope.$$prevSibling.tableParams.reload();
                        $scope.saveAllChanges = function () {
                            if ('' != $scope.inputValue) {
                                angular.forEach($scope.inputValue.split('\n'), function (inputCate) {
                                    var split_cate = inputCate.split('|');
                                    $scope.$$prevSibling.tableParams.settings().dataset.unshift({
                                        cate: split_cate[0],
                                        desc: split_cate[1]
                                    });
                                });
                                $scope.$$prevSibling.tableParams.sorting({});
                                $scope.$$prevSibling.tableParams.page(1);
                                $scope.$$prevSibling.tableParams.reload();
                            }
                            ngDialog.closeAll();
                            saveChanges();
                        }
                    }]
                });
            }

            function edit() {
                $scope.isEditing = true;
                $scope.tableParams.sorting({});
                $scope.tableParams.page(1);
                $scope.tableParams.reload();
            }

            function cancelChanges() {
                resetTableStatus();
                var currentPage = $scope.tableParams.page();
                $scope.tableParams.settings({
                    dataset: angular.copy(originalData)
                });
                // keep the user on the current page when we can
                if (!$scope.isAdding) {
                    $scope.tableParams.page(currentPage);
                }
            }

            function del(row) {
                _.remove($scope.tableParams.settings().dataset, function (item) {
                    return row === item;
                });
                $scope.deleteCount++;
                $scope.tableTracker.untrack(row);
                $scope.tableParams.reload().then(function (data) {
                    if (data.length === 0 && $scope.tableParams.total() > 0) {
                        $scope.tableParams.page($scope.tableParams.page() - 1);
                        $scope.tableParams.reload();
                    }
                });
                originalData = angular.copy($scope.tableParams.settings().dataset);
            }

            function hasChanges() {
                return $scope.tableForm.$dirty || $scope.deleteCount > 0;
            }

            function resetTableStatus() {
                $scope.isEditing = false;
                $scope.isAdding = false;
                $scope.deleteCount = 0;
                $scope.tableTracker.reset();
                $scope.tableForm.$setPristine();
            }

            function saveChanges() {
                resetTableStatus();
                var currentPage = $scope.tableParams.page();
                originalData = angular.copy($scope.tableParams.settings().dataset);
            }

            $scope.formData = {
                a: 'classify',
                inputText: '',
                cates: ''
            }
            $scope.results = [];

            function jsonToParam(data) {
                return Object.keys(data).map(function (k) {
                    if (_.isArray(data[k])) {
                        var keyE = encodeURIComponent(k + '[]');
                        return data[k].map(function (subData) {
                            return keyE + '=' + encodeURIComponent(subData);
                        }).join('&');
                    } else {
                        return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]);
                    }
                }).join('&');
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
                if (0 != originalData.length && '' != $scope.formData.inputText) {
                    var count = 2;
                    var cates = [], i = 0;
                    $scope.types = [];
                    $scope.flag = true;
                    angular.forEach(originalData, function (data) {
                        if (data.desc) {
                            cates[i] = data.cate + "|" + data.desc.split(" ").join("|")
                            i++;
                        } else {
                            cates[i] = data.cate;
                            i++;
                        }
                    });
                    $scope.formData.cates = cates.join(',');
                    var data = {
                        classwords: $scope.formData.cates,
                        q: $scope.formData.inputText
                    }
                    $http({
                        method: 'POST',
                        url: 'http://ai.baifendian.com/gc',
                        //url:"http://172.18.1.146:20022/gc",
                        data: $.param(data),
                        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                    }).success(function (data) {
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                        $scope.results = data.task_gc_class_points;
                    })
                        .error(function (data) {
                            count--;
                            if (!count) {
                                $scope.first = true;
                                $scope.flag = false;
                            }
                            $scope.results = [];
                        });
                    var data = {
                        content: $scope.formData.inputText,
                        topn: '10',
                        title: ''
                    }
                    $http({
                        method: 'POST',
                        url: 'http://ai.baifendian.com/keywords',
                        data: $.param(data),
                        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                    }).success(function (data) {
                        count--;
                        if (!count) {
                            $scope.first = true;
                            $scope.flag = false;
                        }
                        for (var x in data) {
                            $scope.types.push(x);
                        }
                        $scope.tag_results = $scope.types;
                    })
                        .error(function (data) {
                            count--;
                            if (!count) {
                                $scope.first = true;
                                $scope.flag = false;
                            }
                            $scope.tag_results = [];
                        });
                }
            };
            $scope.getColor = function (type) {
                var len = $scope.colors.length;
                return $scope.colors[$scope.types.indexOf(type) % len];
            };
        }]);
})();

(function () {
    "use strict";

    angular.module("demoApp").run(configureDefaults);
    configureDefaults.$inject = ["ngTableDefaults"];

    function configureDefaults(ngTableDefaults) {
        ngTableDefaults.params.count = 5;
        ngTableDefaults.settings.counts = [];
    }
})();

(function () {
    "use strict";

    angular.module("demoApp").directive("demoTrackedTable", demoTrackedTable);

    demoTrackedTable.$inject = [];

    function demoTrackedTable() {
        return {
            restrict: "A",
            priority: -1,
            require: "ngForm",
            controller: demoTrackedTableController
        };
    }

    demoTrackedTableController.$inject = ["$scope", "$parse", "$attrs", "$element"];

    function demoTrackedTableController($scope, $parse, $attrs, $element) {
        var self = this;
        var tableForm = $element.controller("form");
        var dirtyCellsByRow = [];
        var invalidCellsByRow = [];
        init();

        ////////

        function init() {
            var setter = $parse($attrs.demoTrackedTable).assign;
            setter($scope, self);
            $scope.$on("$destroy", function () {
                setter(null);
            });

            self.reset = reset;
            self.isCellDirty = isCellDirty;
            self.setCellDirty = setCellDirty;
            self.setCellInvalid = setCellInvalid;
            self.untrack = untrack;
            $scope.$parent.tableTracker = self;
        }

        function getCellsForRow(row, cellsByRow) {
            return _.find(cellsByRow, function (entry) {
                return entry.row === row;
            });
        }

        function isCellDirty(row, cell) {
            var rowCells = getCellsForRow(row, dirtyCellsByRow);
            return rowCells && rowCells.cells.indexOf(cell) !== -1;
        }

        function reset() {
            dirtyCellsByRow = [];
            invalidCellsByRow = [];
            setInvalid(false);
        }

        function setCellDirty(row, cell, isDirty) {
            setCellStatus(row, cell, isDirty, dirtyCellsByRow);
        }

        function setCellInvalid(row, cell, isInvalid) {
            setCellStatus(row, cell, isInvalid, invalidCellsByRow);
            setInvalid(invalidCellsByRow.length > 0);
        }

        function setCellStatus(row, cell, value, cellsByRow) {
            var rowCells = getCellsForRow(row, cellsByRow);
            if (!rowCells && !value) {
                return;
            }

            if (value) {
                if (!rowCells) {
                    rowCells = {
                        row: row,
                        cells: []
                    };
                    cellsByRow.push(rowCells);
                }
                if (rowCells.cells.indexOf(cell) === -1) {
                    rowCells.cells.push(cell);
                }
            } else {
                _.remove(rowCells.cells, function (item) {
                    return cell === item;
                });
                if (rowCells.cells.length === 0) {
                    _.remove(cellsByRow, function (item) {
                        return rowCells === item;
                    });
                }
            }
        }

        function setInvalid(isInvalid) {
            self.$invalid = isInvalid;
            self.$valid = !isInvalid;
        }

        function untrack(row) {
            _.remove(invalidCellsByRow, function (item) {
                return item.row === row;
            });
            _.remove(dirtyCellsByRow, function (item) {
                return item.row === row;
            });
            setInvalid(invalidCellsByRow.length > 0);
        }
    }
})();

(function () {
    "use strict";

    angular.module("demoApp").directive("demoTrackedTableRow", demoTrackedTableRow);

    demoTrackedTableRow.$inject = [];

    function demoTrackedTableRow() {
        return {
            restrict: "A",
            priority: -1,
            require: ["^demoTrackedTable", "ngForm"],
            controller: demoTrackedTableRowController
        };
    }

    demoTrackedTableRowController.$inject = ["$attrs", "$element", "$parse", "$scope"];

    function demoTrackedTableRowController($attrs, $element, $parse, $scope) {
        var self = this;
        var row = $parse($attrs.demoTrackedTableRow)($scope);
        var rowFormCtrl = $element.controller("form");
        var trackedTableCtrl = $element.controller("demoTrackedTable");

        self.isCellDirty = isCellDirty;
        self.setCellDirty = setCellDirty;
        self.setCellInvalid = setCellInvalid;

        function isCellDirty(cell) {
            return trackedTableCtrl.isCellDirty(row, cell);
        }

        function setCellDirty(cell, isDirty) {
            trackedTableCtrl.setCellDirty(row, cell, isDirty);
        }

        function setCellInvalid(cell, isInvalid) {
            trackedTableCtrl.setCellInvalid(row, cell, isInvalid)
        }
    }
})();

(function () {
    "use strict";

    angular.module("demoApp").directive("demoTrackedTableCell", demoTrackedTableCell);

    demoTrackedTableCell.$inject = [];

    function demoTrackedTableCell() {
        return {
            restrict: "A",
            priority: -1,
            scope: true,
            require: ["^demoTrackedTableRow", "ngForm"],
            controller: demoTrackedTableCellController
        };
    }

    demoTrackedTableCellController.$inject = ["$attrs", "$element", "$scope"];

    function demoTrackedTableCellController($attrs, $element, $scope) {
        var cellFormCtrl = $element.controller("form");
        var cellName = cellFormCtrl.$name;
        var trackedTableRowCtrl = $element.controller("demoTrackedTableRow");

        if (trackedTableRowCtrl.isCellDirty(cellName)) {
            cellFormCtrl.$setDirty();
        } else {
            cellFormCtrl.$setPristine();
        }
        // note: we don't have to force setting validaty as angular will run validations
        // when we page back to a row that contains invalid data

        $scope.$watch(function () {
            return cellFormCtrl.$dirty;
        }, function (newValue, oldValue) {
            if (newValue === oldValue) return;

            trackedTableRowCtrl.setCellDirty(cellName, newValue);
        });

        $scope.$watch(function () {
            return cellFormCtrl.$invalid;
        }, function (newValue, oldValue) {
            if (newValue === oldValue) return;

            trackedTableRowCtrl.setCellInvalid(cellName, newValue);
        });
    }
})();
