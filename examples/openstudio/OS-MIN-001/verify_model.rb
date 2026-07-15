require 'openstudio'

MODEL_PATH = OpenStudio::Path.new(File.join(__dir__, 'model.osm'))
TOLERANCE = 0.01

translator = OpenStudio::OSVersion::VersionTranslator.new
optional_model = translator.loadModel(MODEL_PATH)
raise 'No se pudo cargar model.osm' if optional_model.empty?

model = optional_model.get
spaces = model.getSpaces
surfaces = model.getSurfaces
windows = model.getSubSurfaces.select { |surface| surface.subSurfaceType == 'FixedWindow' }

values = {
  spaces: spaces.size,
  thermal_zones: model.getThermalZones.size,
  floor_area_m2: surfaces.select { |surface| surface.surfaceType == 'Floor' }.sum(&:grossArea),
  roof_area_m2: surfaces.select { |surface| surface.surfaceType == 'RoofCeiling' }.sum(&:grossArea),
  exterior_wall_area_m2: surfaces.select { |surface| surface.surfaceType == 'Wall' && surface.outsideBoundaryCondition == 'Outdoors' }.sum(&:grossArea),
  interior_partition_m2: surfaces.select { |surface| surface.surfaceType == 'Wall' && surface.outsideBoundaryCondition == 'Surface' }.sum(&:grossArea) / 2.0,
  volume_m3: spaces.sum(&:volume),
  windows: windows.size,
  window_area_m2: windows.sum(&:grossArea)
}

expected = {
  spaces: 2,
  thermal_zones: 2,
  floor_area_m2: 80.0,
  roof_area_m2: 80.0,
  exterior_wall_area_m2: 108.0,
  interior_partition_m2: 24.0,
  volume_m3: 240.0,
  windows: 2,
  window_area_m2: 6.0
}

expected.each do |key, target|
  actual = values.fetch(key)
  valid = target.is_a?(Integer) ? actual == target : (actual - target).abs <= TOLERANCE
  raise "#{key}: esperado #{target}, obtenido #{actual}" unless valid
  puts "OK #{key}=#{actual.round(3)}"
end

energy_objects = {
  people: model.getPeoples.size,
  lights: model.getLightss.size,
  electric_equipment: model.getElectricEquipments.size,
  infiltration: model.getSpaceInfiltrationDesignFlowRates.size,
  outdoor_air: model.getDesignSpecificationOutdoorAirs.size,
  thermostats: model.getThermostatSetpointDualSetpoints.size
}
energy_objects.each do |name, actual|
  raise "#{name}: esperado 2, obtenido #{actual}" unless actual == 2
  puts "OK #{name}=#{actual}"
end

puts 'Verificación geométrica superada.'
