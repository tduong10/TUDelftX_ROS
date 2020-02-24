
"use strict";

let GetMaterialLocations = require('./GetMaterialLocations.js')
let AGVControl = require('./AGVControl.js')
let VacuumGripperControl = require('./VacuumGripperControl.js')
let PopulationControl = require('./PopulationControl.js')
let ConveyorBeltControl = require('./ConveyorBeltControl.js')
let SubmitTray = require('./SubmitTray.js')

module.exports = {
  GetMaterialLocations: GetMaterialLocations,
  AGVControl: AGVControl,
  VacuumGripperControl: VacuumGripperControl,
  PopulationControl: PopulationControl,
  ConveyorBeltControl: ConveyorBeltControl,
  SubmitTray: SubmitTray,
};
