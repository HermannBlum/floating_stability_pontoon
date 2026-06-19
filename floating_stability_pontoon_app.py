import pandas as pd
from toolbox.dataclasses import GeneralParameters, Pontoon, Results

from toolbox.functions import calculate_force, calculate_center_of_gravity, calculate_metacentric_height_roll

pd.set_option('display.float_format', lambda x: f'{x:.2f}')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)          # show all columns
pd.set_option('display.expand_frame_repr', False)   # do not split over multiple columns
pd.set_option('display.width', 0)                   # use full console width
pd.set_option('display.max_colwidth', None)         # do not split column values

file = "template/pontoon_template.csv"

massforce_centroid = pd.read_csv(file, sep=None, engine="python")
massforce_centroid["force_total_kN"] = massforce_centroid.apply(calculate_force, axis=1)

errors = []

for _, row in massforce_centroid.iterrows():
    if row["load_type"] == "point" and pd.isna(row["force_kN"]):
        errors.append(f"{row['name']}: mist force_kN")

    if row["load_type"] == "area":
        if pd.isna(row["load_kNm2"]) or pd.isna(row["width_m"]) or pd.isna(row["length_m"]):
            errors.append(f"{row['name']}: mist area input")

print(massforce_centroid.fillna("-"))

total_force, x_cg, y_cg, z_cg = calculate_center_of_gravity(massforce_centroid)

gen = GeneralParameters(
    gravity=9.81,
    water_density=1.012,
    requirement_gm=1.00,
    requirement_roll=2.50,
    requirement_pitch=1.00)

massforce_centroid_name_id = massforce_centroid.set_index("name")

pon = Pontoon(
    name="The William Gall",
    type="barge",
    pontoon_weight= massforce_centroid_name_id.loc["pontoon", "force_kN"],
    block_factor=1.0,
    length=15.50,
    width=5.20,
    height=0.75)

res = Results(
    x_coordinate_mass_centroid=x_cg,
    y_coordinate_mass_centroid=y_cg,
    z_coordinate_mass_centroid=z_cg,
    total_force=total_force,
    total_weight=total_force / gen.gravity,
    moulded_depth = (total_force / gen.gravity) / (pon.block_factor * pon.length * pon.width * gen.water_density),
    displaced_volume= (total_force / gen.gravity) / gen.water_density)

## K is the point at the bottom of the element on the z-axis
## Point B is the centre of buoyancy (drukpunt) for caissons and pontoons it is halfway between the water line and the bottom of the element.
## G is the centre of gravity (zwaartepunt) of the element G( x_cg, y_cg, z_cg)
## M is the meta_centre, the point of intersection of the z-axis with the action line of the buoyancy force in tilted position.
## the larger M, the larger the lever a and thus the capability of the element to restore the upright position

mc_height_roll = calculate_metacentric_height_roll(gen, pon, res)

print()
print(mc_height_roll)
