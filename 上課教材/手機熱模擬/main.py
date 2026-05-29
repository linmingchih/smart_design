from ansys.aedt.core import Icepak


# =========================
# 1. Basic settings
# =========================
AEDT_VERSION = "2026.1"
CAD_FILE = r"C:\demo\phone.step"


# =========================
# 2. Custom materials
# =========================
icepak = Icepak(version=AEDT_VERSION)

polycarbonate = icepak.materials.add_material("polycarbonate")
polycarbonate.thermal_conductivity = 0.19


# =========================
# 3. Material rules
# =========================
# Format:
# "material name": ([keywords used to match object names], "surface material")
material_rules = {
    "copper": (["Pin", "terminal", "FlexConnector", "Rectangle", "Circle"], "Steel-oxidised-surface"),
    "silicon": (["Pkg", "RFPkg"], "Steel-oxidised-surface"),
    "glass": (["screen", "TouchScreen", "Lens", "LLens"], "Steel-oxidised-surface"),
    "FR4_epoxy": (["MainBoard", "ButtonPCB"], "Steel-oxidised-surface"),
    "aluminum": (["Case", "Cover", "RFHousingShld", "Bottom", "Back"], "Steel-oxidised-surface"),
    "polycarbonate": (["Button", "Btn", "Menu", "Home", "On", "OFF", "Speaker", "Sim", "SIMbase"], "Steel-oxidised-surface"),
}


# =========================
# 4. Import CAD
# =========================
icepak.import_3d_cad(CAD_FILE)


# =========================
# 5. Assign materials by object name
# =========================
for obj in icepak.modeler.objects.values():
    if obj.name.lower() == "region":
        icepak.assign_openings(obj.faces)
        continue

    if not obj.is_3d:
        continue

    assigned = False

    for material_name, (keywords, surface_material_name) in material_rules.items():
        if any(keyword.lower() in obj.name.lower() for keyword in keywords):
            obj.material_name = material_name
            obj.surface_material_name = surface_material_name
            print(f"Assigned {obj.name} -> Vol: {material_name} | Surf: {surface_material_name}")
            assigned = True
            break

    if not assigned:
        obj.is_model = False
        print(f"[Skipped] No matching rule found for object: {obj.name}")


# =========================
# 6. Assign priorities based on material
#    Order: low priority -> high priority
# =========================
material_priority_order = [
    "polycarbonate",
    "glass",
    "FR4_epoxy",
    "silicon",
    "aluminum",
    "copper",
]

priority_assignment = []

for material_name in material_priority_order:
    object_names = [
        obj.name
        for obj in icepak.modeler.objects.values()
        if obj.name.lower() != "region" and obj.is_model and obj.material_name == material_name
    ]

    if object_names:
        priority_assignment.append(object_names)

if priority_assignment:
    icepak.mesh.assign_priorities(priority_assignment)
    print(f"Assigned priorities from low to high: {priority_assignment}")
else:
    print("[Warning] No material-based priority groups were created.")


# =========================
# 7. Package power settings
# =========================
pkg_power_map = {
    "Pkg1": "1.5W",
    "Pkg2": "2.0W",
    "Pkg3": "0.8W",
    "Pkg4": "1.2W",
    "Pkg5": "3.5W",
}

monitors = []

for pkg_name, power_value in pkg_power_map.items():
    if pkg_name in icepak.modeler.object_names:
        print(f"Assigning power source: {pkg_name} -> {power_value}")

        icepak.assign_source(
            assignment=pkg_name,
            thermal_condition="Total Power",
            assignment_value=power_value,
        )

        monitor_name = f"temp_{pkg_name}"
        monitors.append(monitor_name)
        icepak.assign_point_monitor_in_object(pkg_name, monitor_name=monitor_name)
    else:
        print(f"[Warning] Package object '{pkg_name}' not found in the modeler.")


# =========================
# 8. Create setup and mesh
# =========================
setup = icepak.create_setup()
setup.props["Include Gravity"] = True
setup.props["Radiation Model"] = "Discrete Ordinates Model"

icepak.modeler.change_region_padding(
    ["50mm", "50mm", "50mm", "50mm", "100mm", "100mm"],
    ["Absolute Offset"] * 6,
    ["+X", "-X", "+Y", "-Y", "+Z", "-Z"],
)

mesh_region = icepak.mesh.assign_mesh_region(level=3)
mesh_region.manual_settings = True
mesh_region.settings["MaxLevels"] = 2
mesh_region.settings["BufferLayers"] = 3
mesh_region.settings["EnforeMLMType"] = "2D"
mesh_region.settings["MaxElementSizeX"] = "5mm"
mesh_region.settings["MaxElementSizeY"] = "5mm"
mesh_region.settings["MaxElementSizeZ"] = "5mm"
mesh_region.update()


# =========================
# 9. Solve
# =========================
icepak.analyze(cores=4, tasks=4)


# =========================
# 10. Read monitor results
# =========================
result = {}

for monitor_name in monitors:
    data = icepak.post.get_solution_data(f"{monitor_name}.Temperature")
    result[monitor_name] = float(data.data_real()[0])

print(result)