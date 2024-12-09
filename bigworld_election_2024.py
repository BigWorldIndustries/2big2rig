# initial seed data, starting rates and candidates
seed_rates = {
    'BigDaddy': 0.0,
    'Tony': 0.0,
    'TheNightPatrol': 0.0
}


categories = ['WeLoveMatt', 'WeLoveTony', '3rdpartyFTW', 'Shneibler Islands', 'Canada', 'Maharnegonia', 'Zazuland']  # List of categories

# ordered from least favored to most favored
categories_by_bias = {
    'Tony': [
        'WeLoveMatt',
        'Canada',
        'Zazuland',
        'Maharnegonia',
        'Shneibler Islands',
        '3rdpartyFTW',
        'WeLoveTony'
    ],
    'BigDaddy': [
        'WeLoveTony',
        'Shneibler Islands',
        'Canada',
        'Maharnegonia',
        'Zazuland',
        '3rdpartyFTW',
        'WeLoveMatt'
    ],
    'TheNightPatrol': [
        'Maharnegonia',
        'Shneibler Islands',
        'WeLoveTony',
        'WeLoveMatt',
        'Zazuland',
        'Canada',
        '3rdpartyFTW'
    ]
}