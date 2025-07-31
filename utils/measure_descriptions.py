"""
Utility functions for providing user-friendly descriptions of measure codes
"""

def get_measure_description(measure_code):
    """
    Get a user-friendly description for a measure code
    
    Parameters:
    - measure_code: The measure code to describe
    
    Returns:
    - String description of the measure
    """
    descriptions = {
        # Agricultural Land and Crop Production
        'A1': 'Agricultural production (total)',
        'A11': 'Crop production',
        'A12': 'Livestock production',
        'A13': 'Mixed farming',
        'A14': 'Agricultural services',
        'A19': 'Other agricultural activities',
        'AGR': 'Total agricultural sector',
        'AGR_SOIL': 'Agricultural soil management',
        'A_LAND': 'Agricultural land area',
        'A_P_CROP': 'Agricultural production per crop',
        'TOTAGR_LAND': 'Total agricultural land',
        'PERMA': 'Permanent crops',
        'PERMPASTURE': 'Permanent pasture',
        'T_CROP': 'Temporary crops',
        
        # Greenhouse Gas Emissions
        'CH4': 'Methane emissions',
        'CH4AGR': 'Agricultural methane emissions',
        'CO2': 'Carbon dioxide emissions',
        'CO2AGR': 'Agricultural CO2 emissions',
        'N2O': 'Nitrous oxide emissions',
        'N2OAGR': 'Agricultural N2O emissions',
        'GHG_AG': 'Agricultural greenhouse gas emissions',
        'TOTGHG_GAZ': 'Total greenhouse gas emissions',
        'TOTGHG_LULU': 'GHG from land use',
        'TOTGHG_LULUCF': 'GHG from land use, land-use change and forestry',
        'TOTGHG_SOURCE': 'Total GHG by source',
        
        # Energy and Resource Use
        'NRJ': 'Energy use',
        'TOTNRJ': 'Total energy consumption',
        'TOTNRJAG': 'Total agricultural energy use',
        
        # Water Resources
        'TOTFRESHW': 'Total freshwater use',
        'TOTFRESHAG': 'Agricultural freshwater use',
        'IRRIGABLEAREA': 'Irrigable area',
        'IRRIGATIONAREA': 'Irrigated area',
        
        # Pesticides and Chemicals
        'TOTPEST': 'Total pesticide use',
        'F_PEST': 'Fungicide use',
        'H_PEST': 'Herbicide use',
        'I_PEST': 'Insecticide use',
        'OT_PEST': 'Other pesticide use',
        'M_PEST': 'Mixed pesticides',
        'AGPEST': 'Agricultural pesticides',
        
        # Nutrients and Fertilizers
        'MANUR': 'Manure application',
        'MANURE': 'Manure production',
        'LIM': 'Lime application',
        
        # Environmental Indicators
        'NH3AGR': 'Agricultural ammonia emissions',
        'NH3TOT': 'Total ammonia emissions',
        'WIND_SOIL': 'Wind soil erosion',
        'WATER_SOIL': 'Water soil erosion',
        'BIRDS': 'Bird population indicators',
        'BIRDSF': 'Farmland bird indicators',
        
        # Economic Indicators
        'B0': 'Gross value added',
        'B0_H': 'Gross value added per hectare',
        'B1': 'Net value added',
        
        # Others
        'WASTE': 'Agricultural waste',
        'RICE': 'Rice production',
        'SF': 'Set-aside area',
        'UA': 'Utilized agricultural area',
        'TR': 'Transport-related emissions',
        'RES': 'Residential emissions',
        'OTH': 'Other categories',
        'OTH_SECTOR': 'Other sectors',
        'MIC': 'Miscellaneous'
    }
    
    return descriptions.get(measure_code, f'Unknown measure: {measure_code}')

def get_nutrient_description(nutrient_type):
    """
    Get a user-friendly description for a nutrient type
    
    Parameters:
    - nutrient_type: The nutrient type to describe
    
    Returns:
    - String description of the nutrient
    """
    descriptions = {
        'Nitrogen': 'Essential for plant growth, but excess can cause water pollution and greenhouse gas emissions',
        'Phosphorus': 'Critical for root development and flowering, limited global reserves make efficient use important',
        'Not applicable': 'Metrics not specifically related to nitrogen or phosphorus nutrients'
    }
    
    return descriptions.get(nutrient_type, f'Unknown nutrient: {nutrient_type}')

def format_measure_label(measure_code):
    """
    Create a formatted label combining the code and description
    
    Parameters:
    - measure_code: The measure code
    
    Returns:
    - Formatted string with code and description
    """
    description = get_measure_description(measure_code)
    if description.startswith('Unknown'):
        return measure_code
    return f"{measure_code} - {description}"
