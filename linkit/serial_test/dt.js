var DecisionTree = require('decision-tree');

var training_data = [
    {"flex1":320,"flex2":76,"flex3":226,"flex4":220,"flex5":234,"output":"little-finger-off"},
    {"flex1":301,"flex2":79,"flex3":236,"flex4":217,"flex5":221,"output":"little-finger-off"},
    {"flex1":298,"flex2":81,"flex3":250,"flex4":224,"flex5":222,"output":"little-finger-off"},
    {"flex1":297,"flex2":79,"flex3":246,"flex4":220,"flex5":226,"output":"little-finger-off"},
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":224,"output":"little-finger-off"}, //
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":601,"output":"little-finger-on"},
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":583,"output":"little-finger-on"},
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":623,"output":"little-finger-on"},
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":621,"output":"little-finger-on"},
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":591,"output":"little-finger-on"},
]                        
/*                             
var training_data = [
    {"color":"blue", "shape":"square", "liked":false},
    {"color":"red", "shape":"square", "liked":false},
    {"color":"blue", "shape":"circle", "liked":true},
    {"color":"red", "shape":"circle", "liked":true},
    {"color":"blue", "shape":"hexagon", "liked":false},
    {"color":"red", "shape":"hexagon", "liked":false},
    {"color":"yellow", "shape":"hexagon", "liked":true},
    {"color":"yellow", "shape":"circle", "liked":true}
];
*/
var test_data = [
    {"flex1":284,"flex2":81,"flex3":251,"flex4":226,"flex5":600,"output":"little-finger-on"},
    {"flex1":284,"flex2":75,"flex3":251,"flex4":226,"flex5":613,"output":"little-finger-on"},
    {"flex1":298,"flex2":79,"flex3":250,"flex4":224,"flex5":223,"output":"little-finger-off"},
    {"flex1":320,"flex2":76,"flex3":226,"flex4":220,"flex5":235,"output":"little-finger-off"},
];

var class_name = "output";

var features = ["flex1", "flex2", "flex3", "flex4", "flex5"];

var dt = new DecisionTree(training_data, class_name, features);

//console.log(predicted_class)

var accuracy = dt.evaluate(test_data);

console.log(accuracy)

var treeModel = dt.toJSON();

//console.log(treeModel)
