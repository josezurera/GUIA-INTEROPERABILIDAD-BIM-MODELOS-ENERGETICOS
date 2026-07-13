import importlib.util
import json
import unittest
from pathlib import Path

import ifcopenshell.api
import numpy as np


SCRIPT = Path(__file__).parents[1] / "scripts" / "validar_ids.py"
SPEC = importlib.util.spec_from_file_location("validar_ids", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


def two_box_spaces(second_offset_x: float):
    model = ifcopenshell.api.run("project.create_file", version="IFC4")
    ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject")
    ifcopenshell.api.run("unit.assign_unit", model)
    context = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run(
        "context.add_context",
        model,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=context,
    )
    for name, offset_x in (("A", 0.0), ("B", second_offset_x)):
        space = ifcopenshell.api.run(
            "root.create_entity", model, ifc_class="IfcSpace", name=name
        )
        representation = ifcopenshell.api.run(
            "geometry.add_wall_representation",
            model,
            context=body,
            length=5.0,
            height=3.0,
            thickness=4.0,
        )
        ifcopenshell.api.run(
            "geometry.assign_representation",
            model,
            product=space,
            representation=representation,
        )
        matrix = np.eye(4)
        matrix[0, 3] = offset_x
        ifcopenshell.api.run(
            "geometry.edit_object_placement", model, product=space, matrix=matrix
        )
    return model


class SpaceIntersectionTests(unittest.TestCase):
    def test_overlapping_spaces_fail(self):
        result = VALIDATOR.space_intersection_diagnostics(two_box_spaces(4.0), 0.002)
        self.assertEqual(result["result"], "FAIL")
        self.assertEqual(result["incident_count"], 1)
        self.assertEqual(
            result["incidents"][0]["bbox_overlap_dimensions_m"], [1.0, 4.0, 3.0]
        )

    def test_touching_spaces_pass(self):
        result = VALIDATOR.space_intersection_diagnostics(two_box_spaces(5.0), 0.002)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["incident_count"], 0)

    def test_small_overlap_within_tolerance_passes(self):
        result = VALIDATOR.space_intersection_diagnostics(two_box_spaces(4.999), 0.002)
        self.assertEqual(result["result"], "PASS")

    def test_missing_space_geometry_is_not_evaluable(self):
        model = two_box_spaces(5.0)
        model.by_type("IfcSpace")[1].Representation = None
        result = VALIDATOR.space_intersection_diagnostics(model, 0.002)
        self.assertEqual(result["result"], "NOT_EVALUABLE")
        self.assertEqual(result["geometry_error_count"], 1)


class JsonDiagnosticsTests(unittest.TestCase):
    def test_ifc_entity_is_converted_to_stable_reference(self):
        model = ifcopenshell.api.run("project.create_file", version="IFC4")
        project = ifcopenshell.api.run(
            "root.create_entity", model, ifc_class="IfcProject", name="Ensayo"
        )
        result = VALIDATOR.json_safe({"instance": project})

        json.dumps(result)
        self.assertEqual(result["instance"]["ifc_class"], "IfcProject")
        self.assertEqual(result["instance"]["global_id"], project.GlobalId)


if __name__ == "__main__":
    unittest.main()
