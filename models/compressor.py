from pydantic import BaseModel, Field
from typing import List, Optional, Union

class CompressorSpec(BaseModel):
    # Product Information
    product_name: Optional[str] = None
    compressor_type: Optional[str] = Field(
        None,
        description="Type of compressor, e.g., Reciprocating, Hermetic, Single Phase, Three Phase, Two Stage Single Phase, etc."
    )
    brand: Optional[str] = Field(
        None,
        description="Brand name, e.g. Copeland"
    )
    model_no: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    used_in: Optional[List[str]] = Field(
        None,
        description="Model numbers of complete HVAC products this part is used in, e.g. WJA436000K000K"
    )
    price: Optional[str] = None
    
    # Dimensions
    length_in: Optional[float] = None
    width_in: Optional[float] = None
    height_in: Optional[float] = None
    dimensional_weight: Optional[float] = None
    mounting_dimensions: Optional[str] = None
    
    # Weight and Physical Properties
    weight_lb: Optional[float] = None
    mass_flow: Optional[List[str]] = None
    cubic_measurement: Optional[float] = None
    
    # Electrical and Performance Specifications
    amps: Optional[float] = None
    locked_rotor_amps: Optional[float] = None
    rated_load_amps: Optional[List[float]] = None
    voltage: Optional[str] = None
    phase: Optional[str] = None
    lower_rpm: Optional[int] = None
    upper_rpm: Optional[int] = None
    cycle_hertz: Optional[List[int]] = None
    tonnage: Optional[float] = None
    
    # Refrigerant and Cooling Specifications
    refrigerant: Optional[str] = None
    oil_type: Optional[str] = None
    oil_charge_initial: Optional[float] = None
    return_gas_temperature: Optional[List[str]] = None
    evaporating_temperature: Optional[List[str]] = None
    condensing_temperature: Optional[str] = None
    liquid_temperature: Optional[List[str]] = None
    
    # Connections
    suction_line_fitting_type: Optional[str] = None
    suction_line_size: Optional[str] = None
    discharge_connection_type: Optional[str] = None
    discharge_connection_size: Optional[str] = None
    
    # Additional Details
    displacement_unit: Optional[str] = None
    displacement: Optional[float] = None
    sound_level: Optional[str] = None
    country_of_origin: Optional[str] = None
    prop_65: Optional[str] = None
    ul_listed: Optional[str] = None
    uom: Optional[str] = None
    upc: Optional[str] = None
    ratings: Optional[str] = None
    substantial_commodity: Optional[str] = None
    protection: Optional[str] = None
    opt_code: Optional[str] = None
    btu_output: Optional[str] = None
    compressor_housing: Optional[str] = None
    compressor_type: Optional[str] = None
