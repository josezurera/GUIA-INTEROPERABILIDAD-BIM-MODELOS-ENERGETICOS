require 'openstudio'

MODEL_DIR = File.expand_path(__dir__)
MODEL_PATH = File.join(MODEL_DIR, 'model.osm')

model = OpenStudio::Model::Model.new
model.getBuilding.setName('OS-MIN-001')
model.getBuilding.setNorthAxis(0.0)
model.getYearDescription.setCalendarYear(2024)
model.getSite.setName('Madrid-Barajas Reference')
model.getSite.setLatitude(40.47)
model.getSite.setLongitude(-3.56)
model.getSite.setTimeZone(1.0)
model.getSite.setElevation(609.0)

summer_day = OpenStudio::Model::DesignDay.new(model)
summer_day.setName('MADRID-SUMMER-REFERENCE')
summer_day.setMonth(7)
summer_day.setDayOfMonth(21)
summer_day.setDayType('SummerDesignDay')
summer_day.setMaximumDryBulbTemperature(36.0)
summer_day.setDailyDryBulbTemperatureRange(12.0)
summer_day.setHumidityConditionType('Wetbulb')
summer_day.setWetBulbOrDewPointAtMaximumDryBulb(20.0)
summer_day.setBarometricPressure(101_325.0)
summer_day.setWindSpeed(3.0)
summer_day.setWindDirection(180.0)
summer_day.setRainIndicator(false)
summer_day.setSnowIndicator(false)
summer_day.setSolarModelIndicator('ASHRAEClearSky')
summer_day.setSkyClearness(1.0)

winter_day = OpenStudio::Model::DesignDay.new(model)
winter_day.setName('MADRID-WINTER-REFERENCE')
winter_day.setMonth(1)
winter_day.setDayOfMonth(21)
winter_day.setDayType('WinterDesignDay')
winter_day.setMaximumDryBulbTemperature(-3.0)
winter_day.setDailyDryBulbTemperatureRange(0.0)
winter_day.setHumidityConditionType('Wetbulb')
winter_day.setWetBulbOrDewPointAtMaximumDryBulb(-3.0)
winter_day.setBarometricPressure(101_325.0)
winter_day.setWindSpeed(4.0)
winter_day.setWindDirection(0.0)
winter_day.setRainIndicator(false)
winter_day.setSnowIndicator(false)
winter_day.setSolarModelIndicator('ASHRAEClearSky')
winter_day.setSkyClearness(0.0)

opaque_material = OpenStudio::Model::MasslessOpaqueMaterial.new(model)
opaque_material.setName('MAT-OPAQUE-REFERENCE')
opaque_material.setRoughness('MediumSmooth')
opaque_material.setThermalResistance(2.0)

opaque_construction = OpenStudio::Model::Construction.new(model)
opaque_construction.setName('CON-OPAQUE-REFERENCE')
opaque_layers = OpenStudio::Model::MaterialVector.new
opaque_layers << opaque_material
opaque_construction.setLayers(opaque_layers)

glazing_material = OpenStudio::Model::SimpleGlazing.new(model)
glazing_material.setName('MAT-GLAZING-REFERENCE')
glazing_material.setUFactor(2.0)
glazing_material.setSolarHeatGainCoefficient(0.60)
glazing_material.setVisibleTransmittance(0.70)

glazing_construction = OpenStudio::Model::Construction.new(model)
glazing_construction.setName('CON-GLAZING-REFERENCE')
glazing_layers = OpenStudio::Model::MaterialVector.new
glazing_layers << glazing_material
glazing_construction.setLayers(glazing_layers)

occupancy_schedule = OpenStudio::Model::ScheduleRuleset.new(model)
occupancy_schedule.setName('SCH-OCCUPANCY-DAILY')
occupancy_day = occupancy_schedule.defaultDaySchedule
occupancy_day.addValue(OpenStudio::Time.new(0, 8, 0, 0), 0.0)
occupancy_day.addValue(OpenStudio::Time.new(0, 18, 0, 0), 1.0)
occupancy_day.addValue(OpenStudio::Time.new(0, 24, 0, 0), 0.0)

heating_schedule = OpenStudio::Model::ScheduleConstant.new(model)
heating_schedule.setName('SCH-HEATING-SETPOINT')
heating_schedule.setValue(20.0)

cooling_schedule = OpenStudio::Model::ScheduleConstant.new(model)
cooling_schedule.setName('SCH-COOLING-SETPOINT')
cooling_schedule.setValue(26.0)

activity_schedule = OpenStudio::Model::ScheduleConstant.new(model)
activity_schedule.setName('SCH-ACTIVITY-120-W-PERSON')
activity_schedule.setValue(120.0)

people_definition = OpenStudio::Model::PeopleDefinition.new(model)
people_definition.setName('LOAD-PEOPLE-0.10-PER-M2')
people_definition.setPeopleperSpaceFloorArea(0.10)

lights_definition = OpenStudio::Model::LightsDefinition.new(model)
lights_definition.setName('LOAD-LIGHTS-8-W-M2')
lights_definition.setWattsperSpaceFloorArea(8.0)

equipment_definition = OpenStudio::Model::ElectricEquipmentDefinition.new(model)
equipment_definition.setName('LOAD-EQUIPMENT-10-W-M2')
equipment_definition.setWattsperSpaceFloorArea(10.0)

story = OpenStudio::Model::BuildingStory.new(model)
story.setName('LEVEL-00')
story.setNominalZCoordinate(0.0)
story.setNominalFloortoFloorHeight(3.0)

def create_space(model, story, name, x0, x1)
  points = OpenStudio::Point3dVector.new
  points << OpenStudio::Point3d.new(x0, 0.0, 0.0)
  points << OpenStudio::Point3d.new(x0, 8.0, 0.0)
  points << OpenStudio::Point3d.new(x1, 8.0, 0.0)
  points << OpenStudio::Point3d.new(x1, 0.0, 0.0)

  optional_space = OpenStudio::Model::Space.fromFloorPrint(points, 3.0, model)
  raise "No se pudo crear #{name}" if optional_space.empty?

  space = optional_space.get
  space.setName(name)
  space.setBuildingStory(story)

  zone = OpenStudio::Model::ThermalZone.new(model)
  zone.setName(name.sub('SPACE', 'TZ'))
  zone.setUseIdealAirLoads(true)
  space.setThermalZone(zone)
  space
end

space_a = create_space(model, story, 'SPACE-A', 0.0, 5.0)
space_b = create_space(model, story, 'SPACE-B', 5.0, 10.0)
spaces = OpenStudio::Model::SpaceVector.new
spaces << space_a
spaces << space_b

OpenStudio::Model.intersectSurfaces(spaces)
OpenStudio::Model.matchSurfaces(spaces)

model.getSurfaces.each { |surface| surface.setConstruction(opaque_construction) }

[space_a, space_b].each do |space|
  south_wall = space.surfaces.find do |surface|
    surface.surfaceType == 'Wall' &&
      surface.vertices.all? { |vertex| vertex.y.abs < 1.0e-6 }
  end
  raise "No se encontró el muro sur de #{space.nameString}" unless south_wall

  optional_window = south_wall.setWindowToWallRatio(0.20, 0.75, true)
  raise "No se pudo crear la ventana de #{space.nameString}" if optional_window.empty?

  suffix = space.nameString.end_with?('A') ? 'A' : 'B'
  optional_window.get.setName("WIN-#{suffix}-S")
  optional_window.get.setConstruction(glazing_construction)

  people = OpenStudio::Model::People.new(people_definition)
  people.setName("PEOPLE-#{suffix}")
  people.setSpace(space)
  people.setNumberofPeopleSchedule(occupancy_schedule)
  people.setActivityLevelSchedule(activity_schedule)

  lights = OpenStudio::Model::Lights.new(lights_definition)
  lights.setName("LIGHTS-#{suffix}")
  lights.setSpace(space)
  lights.setSchedule(occupancy_schedule)

  equipment = OpenStudio::Model::ElectricEquipment.new(equipment_definition)
  equipment.setName("EQUIPMENT-#{suffix}")
  equipment.setSpace(space)
  equipment.setSchedule(occupancy_schedule)

  infiltration = OpenStudio::Model::SpaceInfiltrationDesignFlowRate.new(model)
  infiltration.setName("INFILTRATION-#{suffix}-0.30-ACH")
  infiltration.setSpace(space)
  infiltration.setSchedule(model.alwaysOnDiscreteSchedule)
  infiltration.setAirChangesperHour(0.30)

  outdoor_air = OpenStudio::Model::DesignSpecificationOutdoorAir.new(model)
  outdoor_air.setName("OUTDOOR-AIR-#{suffix}-10-L-S-PERSON")
  outdoor_air.setOutdoorAirMethod('Sum')
  outdoor_air.setOutdoorAirFlowperPerson(0.010)
  space.setDesignSpecificationOutdoorAir(outdoor_air)

  thermostat = OpenStudio::Model::ThermostatSetpointDualSetpoint.new(model)
  thermostat.setName("THERMOSTAT-#{suffix}-20-26-C")
  thermostat.setHeatingSetpointTemperatureSchedule(heating_schedule)
  thermostat.setCoolingSetpointTemperatureSchedule(cooling_schedule)
  space.thermalZone.get.setThermostatSetpointDualSetpoint(thermostat)
end

model.getSimulationControl.setRunSimulationforSizingPeriods(true)
model.getSimulationControl.setRunSimulationforWeatherFileRunPeriods(false)

unless model.save(OpenStudio::Path.new(MODEL_PATH), true)
  raise "No se pudo guardar #{MODEL_PATH}"
end

# OpenStudio añade líneas vacías al final; se normaliza el cierre del archivo de referencia.
File.write(MODEL_PATH, File.read(MODEL_PATH).rstrip + "\n")

puts "Modelo guardado: #{MODEL_PATH}"
puts "Espacios: #{model.getSpaces.size}"
puts "Zonas térmicas: #{model.getThermalZones.size}"
puts "Superficies: #{model.getSurfaces.size}"
puts "Huecos: #{model.getSubSurfaces.size}"
