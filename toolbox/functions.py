

def calculate_force(row):
    if row["load_type"] == "point":
        base_force = row["force_kN"]
    elif row["load_type"] == "area":
        base_force = row["load_kNm2"] * row["width_m"] * row["length_m"]

    return base_force * row["factor"]

def calculate_center_of_gravity(massforce_centroid):
    total_force = massforce_centroid["force_total_kN"].sum()

    if total_force == 0:
        raise ValueError("Totale kracht is 0")

    x_cg = (massforce_centroid["x_m"] * massforce_centroid["force_total_kN"]).sum() / total_force
    y_cg = (massforce_centroid["y_m"] * massforce_centroid["force_total_kN"]).sum() / total_force
    z_cg = (massforce_centroid["z_m"] * massforce_centroid["force_total_kN"]).sum() / total_force

    return total_force, x_cg, y_cg, z_cg

def calculate_metacentric_height_roll(gen, pon, res):
    KB = res.moulded_depth / 2 ## for simple square element
    BM = pon.inertia_yy / res.displaced_volume ## for angels < 10 sin(angle) about equal to angle in radian
    KG = res.y_coordinate_mass_centroid
    mc_height_roll = KB + BM - KG
    return mc_height_roll