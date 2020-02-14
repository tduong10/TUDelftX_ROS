
"use strict";

let ConveyorBeltControl = require('./ConveyorBeltControl.js')
let AGVControl = require('./AGVControl.js')
let GetMaterialLocations = require('./GetMaterialLocations.js')
let SubmitTray = require('./SubmitTray.js')
let VacuumGripperControl = require('./VacuumGripperControl.js')
let PopulationControl = require('./PopulationControl.js')

module.exports = {
  ConveyorBeltControl: ConveyorBeltControl,
  AGVControl: AGVControl,
  GetMaterialLocations: GetMaterialLocations,
  SubmitTray: SubmitTray,
  VacuumGripperControl: VacuumGripperControl,
  PopulationControl: PopulationControl,
};
