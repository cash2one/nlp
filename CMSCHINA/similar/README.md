SIMILAR
--------------

synonym 与 nearsynonym 都增加一个mode 参数，auto 即返回一个list。
'split' in mode: 返回一个dict, 表示最后结果的多个源头

synonym 时 mode 可以为'auto'(默认), 'auto_split'(默认分源), 'extended_split'(拓展分源), 'only_extended'(仅拓展分源),etc
nearsynonym 时 mode 可以为'auto'(默认),'auto_split'(默认分源),'wiki+tyccl+split'(维基百科+哈工大词林+分源),etc

前端需要增加一个mode参数(可以弄成下拉+自定义输入)，默认为auto, 并对返回是list/dict 分开处理。

