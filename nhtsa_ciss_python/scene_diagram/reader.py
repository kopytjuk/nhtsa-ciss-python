import xml.etree.ElementTree as ET
from typing import List

from .models import GosModel, Label, PolyCurve


class BlitzReader:
    """Parser for the blz files generated by Faro/ARAS Blitz software."""

    def __init__(self, file_path) -> None:
        self.tree = ET.parse(file_path)

    def read_metadata(self):
        root = self.get_tree_root()
        data_field = root.find("data")
        meta_attributes = data_field.attrib
        return meta_attributes

    def get_tree_root(self):
        return self.tree.getroot()

    def read_layer(self, name: str = "Default"):
        root = self.get_tree_root()
        layer = root.find(f'scene/layers/layer[@name="{name}"]')
        return layer

    def get_vehicles(
        self, layer_name: str = "Default", only_named: bool = False
    ) -> List[GosModel]:
        """Extracts available vehicles.

        Args:
            layer_name (str, optional): Layer name. Defaults to "Default".
            only_named (bool, optional): Ignores objects /wo name. Defaults to False.

        Returns:
            List[GosModel]: parsed road objects
        """

        layer = self.read_layer(layer_name)
        objects = layer.findall("items/item[@type='gosmodel']")

        gos_models = list()
        for object in objects:
            obj_attrs = object.attrib
            if only_named and not len(obj_attrs["name"]):
                continue
            gos_model = GosModel(
                obj_attrs["name"],
                int(obj_attrs["dmgIdx"]),
                float(obj_attrs["t"]),
                float(obj_attrs["pX"]),
                float(obj_attrs["pY"]),
                float(obj_attrs["sX"]),
                float(obj_attrs["sY"]),
                float(obj_attrs["bsX"]),
                float(obj_attrs["bsY"]),
            )
            gos_models.append(gos_model)
        return gos_models

    def get_labels(self, layer_name: str = "Default") -> List[Label]:
        """Extracts available labels with text.

        Args:
            layer_name (str, optional): Layer name. Defaults to "Default".
            only_named (bool, optional): Ignores objects /wo name. Defaults to False.

        Returns:
            List[Label]: parsed road objects
        """

        layer = self.read_layer(layer_name)
        elements = layer.findall("items/item[@type='label']")

        labels = list()
        for elem in elements:
            elem_attrs = elem.attrib
            textp = elem.find("text[@type='textp']")

            label = Label(
                float(elem_attrs["posX"]),
                float(elem_attrs["posY"]),
                float(elem_attrs["sX"]),
                float(elem_attrs["sY"]),
                float(elem_attrs["theta"]),
                textp.attrib["txt"],
            )
            labels.append(label)
        return labels

    def get_curves(self, layer_name: str = "Default") -> List[PolyCurve]:
        """Extracts available labels with text.

        Args:
            layer_name (str, optional): Layer name. Defaults to "Default".
            only_named (bool, optional): Ignores objects /wo name. Defaults to False.

        Returns:
            List[Label]: parsed road objects
        """

        layer = self.read_layer(layer_name)
        elements = layer.findall("items/item[@type='poly-curve']")

        curves = list()
        for elem in elements:
            elem_attrs = elem.attrib
            points = elem.findall("pnt")
            coords = list()
            for pt in points:
                pt_attrs = pt.attrib
                x = float(pt_attrs["X"])
                y = float(pt_attrs["Y"])
                coords.append((x, y))

            curve = PolyCurve.from_coords(coords, elem_attrs)
            curves.append(curve)

        return curves
