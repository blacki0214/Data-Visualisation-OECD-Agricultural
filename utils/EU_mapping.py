def get_eu_members():
    """
    Get a list of EU member countries with their ISO-3 codes.
    """
    #EU27 from February 2020
    eu27_2020_members = [
        'AUT',  'BEL',  'BGR',  'HRV',  'CYP',  'CZE',
        'DNK',  'EST',  'FIN',  'FRA',  'DEU',  'GRC',
        'HUN',  'IRL',  'ITA',  'LTU',  'LUX',  'LVA',
        'MLT',  'NLD',  'POL',  'PRT',  'ROU',  'SVK',
        'SVN',  'ESP',  'SWE'
    ]
    
    #EU28 before Brexit
    eu28_members = eu27_2020_members + ['GBR']  # United Kingdom
    
    #EU27 after Brexit
    eu27_members = [code for code in eu28_members if code != 'GBR']
    
    #Create a mapping for EU27 and EU28
    eu_mappings = {
        'EU27': eu27_members,
        'EU28': eu28_members,
        'EU27_2020': eu27_2020_members,
        'EU': eu28_members
    }
    
    return eu_mappings