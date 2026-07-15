require 'json'
require 'openstudio'

abort 'Uso: openstudio compare_models.rb referencia.osm candidato.osm [informe.json]' if ARGV.size < 2

reference_path = File.expand_path(ARGV[0], Dir.pwd)
candidate_path = File.expand_path(ARGV[1], Dir.pwd)
report_path = ARGV[2] && File.expand_path(ARGV[2], Dir.pwd)
tolerance = 0.000001

def load_model(path)
  translator = OpenStudio::OSVersion::VersionTranslator.new
  optional_model = translator.loadModel(OpenStudio::Path.new(path))
  raise "No se pudo cargar #{path}" if optional_model.empty?

  optional_model.get
end

def rounded(value)
  value.round(6)
end

def canonical_vertices(points)
  vertices = points.map { |vertex| [rounded(vertex.x), rounded(vertex.y), rounded(vertex.z)] }
  start_index = vertices.each_index.min_by { |index| vertices[index] }
  vertices.rotate(start_index)
end

def snapshot(model)
  surfaces = model.getSurfaces.sort_by(&:nameString).map do |surface|
    {
      name: surface.nameString,
      type: surface.surfaceType,
      boundary: surface.outsideBoundaryCondition,
      area_m2: rounded(surface.grossArea),
      space: surface.space.empty? ? nil : surface.space.get.nameString,
      adjacent: surface.adjacentSurface.empty? ? nil : surface.adjacentSurface.get.nameString,
      vertices_m: canonical_vertices(surface.vertices)
    }
  end

  subsurfaces = model.getSubSurfaces.sort_by(&:nameString).map do |surface|
    {
      name: surface.nameString,
      type: surface.subSurfaceType,
      area_m2: rounded(surface.grossArea),
      parent_surface: surface.surface.empty? ? nil : surface.surface.get.nameString,
      vertices_m: canonical_vertices(surface.vertices)
    }
  end

  spaces = model.getSpaces.sort_by(&:nameString).map do |space|
    {
      name: space.nameString,
      floor_area_m2: rounded(space.floorArea),
      volume_m3: rounded(space.volume),
      thermal_zone: space.thermalZone.empty? ? nil : space.thermalZone.get.nameString
    }
  end

  object_counts = model.getModelObjects.each_with_object(Hash.new(0)) do |object, counts|
    counts[object.iddObjectType.valueName] += 1
  end.sort.to_h

  {
    object_counts: object_counts,
    spaces: spaces,
    thermal_zones: model.getThermalZones.map(&:nameString).sort,
    surfaces: surfaces,
    subsurfaces: subsurfaces,
    energy_objects: {
      people: model.getPeoples.size,
      lights: model.getLightss.size,
      electric_equipment: model.getElectricEquipments.size,
      infiltration: model.getSpaceInfiltrationDesignFlowRates.size,
      outdoor_air: model.getDesignSpecificationOutdoorAirs.size,
      thermostats: model.getThermostatSetpointDualSetpoints.size,
      ideal_loads: model.getZoneHVACIdealLoadsAirSystems.size
    }
  }
end

reference = snapshot(load_model(reference_path))
candidate = snapshot(load_model(candidate_path))

allowed_additions = {
  'OS_Facility' => 1,
  'OS_Rendering_Color' => 5
}

all_types = (reference[:object_counts].keys + candidate[:object_counts].keys).uniq.sort
type_differences = all_types.filter_map do |type|
  reference_count = reference[:object_counts].fetch(type, 0)
  candidate_count = candidate[:object_counts].fetch(type, 0)
  next if reference_count == candidate_count

  {
    type: type,
    reference: reference_count,
    candidate: candidate_count,
    delta: candidate_count - reference_count,
    allowed: allowed_additions[type] == candidate_count - reference_count
  }
end

semantic_sections = %i[spaces thermal_zones surfaces subsurfaces energy_objects]
semantic_differences = semantic_sections.reject { |section| reference[section] == candidate[section] }
unexpected_type_differences = type_differences.reject { |difference| difference[:allowed] }

report = {
  schema: 'bem-openstudio-model-comparison/1.0',
  reference: reference_path,
  candidate: candidate_path,
  tolerance_m: tolerance,
  result: semantic_differences.empty? && unexpected_type_differences.empty? ? 'pass' : 'fail',
  semantic_sections_equal: semantic_sections.to_h { |section| [section, !semantic_differences.include?(section)] },
  type_differences: type_differences,
  unexpected_type_differences: unexpected_type_differences,
  semantic_differences: semantic_differences,
  difference_details: semantic_differences.to_h do |section|
    [section, { reference: reference[section], candidate: candidate[section] }]
  end
}

json = JSON.pretty_generate(report)
puts json
File.write(report_path, "#{json}\n") if report_path
exit(report[:result] == 'pass' ? 0 : 1)
