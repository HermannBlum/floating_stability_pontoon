from dataclasses import dataclass

@dataclass
class GeneralParameters:
    gravity: float
    water_density: float
    requirement_gm: float
    requirement_roll: float
    requirement_pitch: float

@dataclass
class Pontoon:
    name: str
    type: str
    pontoon_weight: float
    block_factor: float
    length: float
    width: float
    height: float

    @property
    def inertia_yy(self) -> float:
        """innertia_yy = 1/12 * length * width^3"""
        return 1/12 * self.length * pow(self.width, 3)

    @property
    def inertia_xx(self) -> float:
        """innertia_xx = 1/12 * length^3 * width"""
        return 1/12 * pow(self.length, 3) * self.width

@dataclass
class Results:
    x_coordinate_mass_centroid: float
    y_coordinate_mass_centroid: float
    z_coordinate_mass_centroid: float
    total_force: float
    total_weight: float
    moulded_depth: float
    displaced_volume: float
