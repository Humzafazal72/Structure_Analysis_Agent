import io
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

SupportMaterial = Literal[
    "DF-L", "SP", "SPF", "HF", 
    "concrete", "steel", 
    "LVL", "PSL", "LSL"
]

class UncertainAreas(BaseModel):
    area_name: str
    variables: List[str]

class LumberSpec(BaseModel):
    species: Literal["DF-L", "SP", "SPF", "HF"] | None
    grade: Literal["SS", "No.1", "No.2", "No.3", "Stud"] | None
    species_grade_note: str

# ------------------------- Global Project Data -----------------------
class ProjectData(BaseModel):
    address: str
    stories: int | None
    uncertain_areas: List[str] | None

class WindLoadData(BaseModel):
    wind_speed_mph: float | None
    exposure_category: Literal["B", "C", "D"] | None
    uncertain_areas: List[str] | None

class SeismicLoadData(BaseModel):
    seismic_design_category: str | None
    sds: float | None
    sd1: float | None
    design_base_shear_kips: float | None
    uncertain_areas: List[str] | None

 # --------------------------- Roof System ---------------------------
class RoofRafter(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str
    overhang_in: float | None
    overhang_note: str
    roof_pitch: str | None
    available_support_bearing_in: float | None
    available_support_bearing_note: str
    support_material: SupportMaterial | None
    spacing_in: float | None
    roof_dead_load_psf: float | None
    roof_live_load_psf: float | None
    roof_snow_load_psf: float | None
    repetitive_member: bool | None
    uncertain_areas: List[str] | None

class CeilingJoist(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str
    available_support_bearing_in: float | None
    available_support_bearing_note: str
    support_material: SupportMaterial | None
    spacing_in: float | None
    ceiling_dead_load_psf: float | None
    attic_live_load_psf: float | None
    attic_use: Literal["no_access", "limited_storage", "habitable"] | None
    repetitive_member: bool | None
    uncertain_areas: List[str] | None

class RidgeBeam(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str
    available_support_bearing_in: float | None
    available_support_bearing_note: str
    support_material: SupportMaterial | None
    tributary_width_ft: float | None
    tributary_width_note: str
    roof_dead_load_psf: float | None
    roof_live_load_psf: float | None
    roof_snow_load_psf: float | None
    uncertain_areas: List[str] | None

class HipValleyRafter(BaseModel):
    zone: str
    member_type: Literal["hip", "valley"]
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str
    roof_pitch: str | None
    available_support_bearing_in: float | None
    available_support_bearing_note: str
    support_material: SupportMaterial | None
    tributary_width_ft: float | None
    tributary_width_note: str
    roof_dead_load_psf: float | None
    roof_live_load_psf: float | None
    roof_snow_load_psf: float | None
    uncertain_areas: List[str] | None

class RoofDropBeam(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str
    roof_pitch: str | None
    available_support_bearing_in: float | None
    available_support_bearing_note: str
    support_material: SupportMaterial | None
    tributary_width_ft: float | None
    tributary_width_note: str
    roof_dead_load_psf: float | None
    roof_live_load_psf: float | None
    roof_snow_load_psf: float | None
    uncertain_areas: List[str] | None

class RoofFlushBeam(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str
    available_support_bearing_in: float | None
    available_support_bearing_note: str
    support_material: SupportMaterial | None
    hanger_bucket_seat_depth_in: float | None
    hanger_seat_depth_note: str
    hanger_carrier_material: str | None
    tributary_width_ft: float | None
    tributary_width_note: str
    roof_dead_load_psf: float | None
    roof_live_load_psf: float | None
    roof_snow_load_psf: float | None
    uncertain_areas: List[str] | None

class RoofSystemData(BaseModel):
    roof_rafters: List[RoofRafter]
    ceiling_joists: List[CeilingJoist]
    ridge_beams: List[RidgeBeam]
    hip_valley_rafters: List[HipValleyRafter]
    roof_drop_beams: List[RoofDropBeam]
    roof_flush_beams: List[RoofFlushBeam]


 # --------------------------- Floor System ---------------------------
class FloorJoist(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str | None
    cantilever_ft: float | None
    cantilever_note: str | None
    available_support_bearing_in: float | None
    available_support_bearing_note: str | None
    support_material: SupportMaterial | None
    spacing_in: float | None
    dead_load_psf: float | None
    dead_load_note: str | None
    floor_live_load_psf: float | None
    floor_live_load_note: str | None
    repetitive_member: bool | None
    uncertain_areas: List[str] | None

class FloorDropBeam(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str | None
    available_support_bearing_in: float | None
    available_support_bearing_note: str | None
    support_material: SupportMaterial | None
    tributary_width_ft: float | None
    tributary_width_note: str | None
    dead_load_psf: float | None
    dead_load_note: str | None
    floor_live_load_psf: float | None
    floor_live_load_note: str | None
    uncertain_areas: List[str] | None

class FloorFlushBeam(BaseModel):
    zone: str
    size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    clear_span_ft: float | None
    clear_span_note: str | None
    available_support_bearing_in: float | None
    available_support_bearing_note: str | None
    support_material: SupportMaterial | None
    hanger_bucket_seat_depth_in: float | None
    hanger_seat_depth_note: str | None
    hanger_carrier_material: str | None
    tributary_width_ft: float | None
    tributary_width_note: str | None
    dead_load_psf: float | None
    dead_load_note: str | None
    floor_live_load_psf: float | None
    floor_live_load_note: str | None
    uncertain_areas: List[str] | None

class FloorSystemData(BaseModel):
    floor_joists: List[FloorJoist]
    floor_drop_beams: List[FloorDropBeam]
    floor_flush_beams: List[FloorFlushBeam]
    

# ----------------------------- Footing -------------------------------
class FootingProjectInfo(BaseModel):
    concrete_fc_footings_psi: int | None
    concrete_fc_slab_psi: int | None
    rebar_grade: str
    soil_bearing_pressure_psf: float | None
    soil_bearing_note: str
    frost_line_depth_in: float | None
    frost_line_note: str
    soils_engineer_required: bool | None
    concrete_cover_to_soil_in: float | None
    uncertain_areas: List[str] | None

class ContinuousStripFooting(BaseModel):
    footing_mark: str
    existing_condition: bool
    new_load_applied: str
    location_description: str
    supported_element: str
    wall_type: Literal["exterior_bearing", "interior_bearing", "shear_wall", "non_bearing", "grade_beam"]
    width_in: float | None
    width_note: str
    depth_in: float | None
    depth_note: str
    length_ft: float | None
    length_note: str
    top_of_footing_below_grade_in: float | None
    bottom_of_footing_below_grade_in: float | None
    embedment_note: str
    frost_compliance: str
    longitudinal_rebar_size: int | None
    longitudinal_rebar_count: int | None
    transverse_rebar_size: int | None
    transverse_rebar_spacing_in: float | None
    rebar_orientation: str | None
    rebar_faces: str | None
    rebar_lap_length_in: float | None
    concrete_cover_in: float | None
    anchor_bolt_dia_in: float | None
    anchor_bolt_embedment_in: float | None
    anchor_bolt_spacing_in: float | None
    anchor_bolt_corner_spacing_in: float | None
    anchor_bolt_end_of_plate_max_in: float | None
    plate_washer_required: bool | None
    plate_washer_spec: str
    sill_plate_size: str
    sill_plate_treated: bool | None
    footing_note: str
    uncertain_areas: List[str] | None

class PadFooting(BaseModel):
    footing_mark: str
    existing_condition: bool
    new_load_applied: str
    location_description: str
    supported_element: str
    width_in: float | None
    length_in: float | None
    depth_in: float | None
    dimension_note: str
    top_of_footing_below_grade_in: float | None
    bottom_of_footing_below_grade_in: float | None
    embedment_note: str
    frost_compliance: str
    rebar_size: int | None
    rebar_spacing_in: float | None
    rebar_orientation: str | None
    rebar_faces: str | None
    rebar_lap_length_in: float | None
    concrete_cover_in: float | None
    post_base_model: str
    post_base_anchor_type: Literal["cast_in", "epoxy_set"] | None
    post_size: str
    footing_note: str
    uncertain_areas: List[str] | None

class GradeBeam(BaseModel):
    footing_mark: str
    existing_condition: bool
    new_load_applied: str
    location_description: str
    supported_element: str
    bearing_on: Literal["soil", "piers", "piles"] | None
    width_in: float | None
    depth_in: float | None
    length_ft: float | None
    dimension_note: str
    top_of_beam_below_grade_in: float | None
    bottom_of_beam_below_grade_in: float | None
    frost_compliance: str
    rebar_size: int | None
    rebar_count: int | None
    rebar_orientation: str | None
    rebar_faces: str | None
    rebar_lap_length_in: float | None
    concrete_cover_in: float | None
    footing_note: str
    uncertain_areas: List[str] | None

class SlabOnGrade(BaseModel):
    zone: str
    existing_condition: bool
    thickness_in: float | None
    thickness_note: str
    reinforcement_type: Literal["rebar", "wwf", "fiber", "none"] | None
    rebar_size: int | None
    rebar_spacing_in: float | None
    rebar_orientation: str | None
    wwf_designation: str | None
    vapor_barrier_mils: int | None
    sub_base_description: str
    sub_base_depth_in: float | None
    control_joint_spacing_ft: float | None
    monolithic_with_footing: bool | None
    slab_note: str
    uncertain_areas: List[str] | None

class HoldownAnchor(BaseModel):
    holdown_model: str
    anchor_rod: str
    embedment_in: float | None
    location: str
    supported_wall_mark: str
    installation_timing: str
    holdown_note: str
    uncertain_areas: List[str] | None

class FootingSystemData(BaseModel):
    project_info: FootingProjectInfo
    continuous_strip_footings: List[ContinuousStripFooting]
    pad_footings: List[PadFooting]
    grade_beams: List[GradeBeam]
    slab_on_grade: List[SlabOnGrade]
    holdown_anchors: List[HoldownAnchor]


# ----------------------------- Post -------------------------------
class StandalonePost(BaseModel):
    post_mark: str
    existing_condition: bool
    new_load_applied: str
    location_description: str
    post_type: Literal["solid", "built_up"] | None
    functional_type: Literal[
        "bearing", 
        "holdown", 
        "corner", 
        "intermediate_bearing", 
        "decorative"
    ] | None
    post_size: str
    number_of_plies: int | None
    species: str
    grade: str
    species_grade_note: str
    height_ft: float | None
    height_note: str
    unbraced_length_ft: float | None
    unbraced_length_note: str
    bracing_condition: str
    tributary_area_sf: float | None
    tributary_area_note: str
    point_load_lbs: float | None
    point_load_note: str
    roof_dead_load_psf: float | None
    roof_live_load_psf: float | None
    roof_snow_load_psf: float | None
    floor_dead_load_psf: float | None
    floor_live_load_psf: float | None
    base_connector_model: str
    base_bearing_surface: Literal[
        "concrete_footing", 
        "concrete_slab", 
        "wood_beam", 
        "steel_beam", 
        "grade"
    ] | None
    base_anchor_type: Literal["cast_in", "epoxy_set", "bolt_through"] | None
    base_anchor_fastener: str
    top_connector_model: str
    top_bearing_condition: str
    holdown_model: str
    holdown_anchor_rod: str
    holdown_note: str
    post_note: str
    uncertain_areas: List[str] | None

class PostData(BaseModel):
    standalone_posts: List[StandalonePost]


# ------------------------- ShearWall ---------------------------
class BracedWallLine(BaseModel):
    bwl_id: str
    direction: Literal["X", "Y"] | None
    story_level: str
    bwl_total_length_ft: float | None
    total_braced_length_ft: float | None
    braced_panel_ids: List[str]
    bwl_spacing_to_adjacent_ft: float | None
    drag_strut_member: str | None
    drag_strut_connector: str | None
    bwl_note: str
    uncertain_areas: List[str] | None

class ShearWall(BaseModel):
    sw_mark: str
    bwl_id: str
    story_level: str
    system_type: str
    framing_species: str | None
    pier_length_ft: float | None
    wall_height_ft: float | None
    aspect_ratio: float | None
    sheathing_type: str
    sheathing_thickness_in: float | None
    sheathing_faces: str
    blocking: str
    edge_nail_spacing_in: float | None
    field_nail_spacing_in: float | None
    boundary_nail_spacing_in: float | None
    nail_size: str
    requires_3x_framing: bool
    stud_size: str
    stud_spacing_in: float | None
    holdown_model: str
    holdown_anchor_rod: str
    holdown_force_lbs: float | None
    support_connector: str
    anchor_bolt_dia_in: float | None
    anchor_bolt_spacing_in: float | None
    sill_plate_transfer: str
    top_plate_transfer: str
    tabulated_unit_shear_plf: float | None
    sw_note: str
    uncertain_areas: List[str] | None


class NailingZone(BaseModel):
    zone_label: str
    nail_spacing_in: float | None
    area_description: str
    uncertain_areas: List[str]

class Diaphragm(BaseModel):
    level: str
    diaphragm_type: str
    sheathing_type: str
    sheathing_thickness_in: float | None
    nailing_zones: List[NailingZone]
    chord_member: str | None
    collector_lines: List[str]
    diaphragm_note: str
    uncertain_areas: List[str] | None

class ShearWallData(BaseModel):
    braced_wall_lines: List[BracedWallLine]
    shear_walls: List[ShearWall]
    diaphragms: List[Diaphragm]


# ------------------------- Wall System ---------------------------
class StudWall(BaseModel):
    zone: str
    wall_type: Literal["exterior_bearing", "interior_bearing", "non_bearing_partition", "shear_wall"]
    stud_size: str
    number_of_plies: int
    lumber_spec: LumberSpec | None
    stud_height_ft: float | None
    stud_height_note: str
    spacing_in: float | None
    wall_length_ft: float | None
    wall_length_note: str
    top_plate: Literal["single", "double"] | None
    top_plate_size: str | None
    bottom_plate_size: str | None
    bottom_plate_treated: bool | None
    sheathing_type: str | None
    sheathing_thickness_in: float | None
    braced_wall_panel: bool | None
    holdown_connector: str | None
    support_material: SupportMaterial | None
    axial_load_lbs: float | None
    axial_load_note: str | None
    tributary_width_ft: float | None
    wall_dead_load_psf: float | None
    repetitive_member: bool | None
    stud_note: str
    uncertain_areas: List[str] | None

class Header(BaseModel):
    zone: str
    opening_type: Literal["window", "door", "sliding_door", "garage_door", "pass_through", "other"]
    opening_mark: str | None
    number_of_stories_above: int | None
    rough_opening_width_in: float | None
    rough_opening_height_in: float | None
    rough_opening_note: str
    header_size: str | None
    number_of_plies: int | None
    lumber_spec: LumberSpec | None
    header_clear_span_ft: float | None
    header_clear_span_note: str
    bearing_wall: bool
    available_bearing_in: float | None
    available_bearing_note: str
    jack_studs_per_side: int | None
    king_studs_per_side: int | None
    support_material: SupportMaterial | None
    tributary_width_ft: float | None
    tributary_width_note: str
    point_load_lbs: float | None
    point_load_source: str | None
    cripple_studs_above: bool | None
    cripple_studs_below: bool | None
    floor_live_load_psf: float | None
    roof_load_on_header_psf: float | None
    header_note: str
    uncertain_areas: List[str] | None

class TopPlate(BaseModel):
    zone: str
    configuration: Literal["single", "double"]
    size: str
    support_material: SupportMaterial | None
    splice_connector: str | None
    plate_note: str
    uncertain_areas: List[str] | None

class BottomPlate(BaseModel):
    zone: str
    size: str
    pressure_treated: bool | None
    support_material: SupportMaterial | None
    anchor_bolt_spacing_in: float | None
    plate_note: str
    uncertain_areas: List[str] | None

class WallSystemData(BaseModel):
    stud_walls: List[StudWall]
    headers: List[Header]
    top_plates: List[TopPlate]
    bottom_plates: List[BottomPlate]


class AgentState(BaseModel):
    file_uri: Optional[str] = None
    file_name: Optional[str] = None
    
    # Global Load / Project Data
    # project_data: Optional[ProjectData] = None
    # wind_load_data: Optional[WindLoadData] = None
    # seismic_load_data: Optional[SeismicLoadData] = None
    
    # Systems
    roof_system: Optional[RoofSystemData] = None
    floor_system: Optional[FloorSystemData] = None
    footing: Optional[FootingSystemData] = None
    post: Optional[PostData] = None
    shear_wall: Optional[ShearWallData] = None
    wall_system: Optional[WallSystemData] = None