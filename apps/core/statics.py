TEAM_CHOICES = [
    {'shortname': 'AFG', 'longname': 'Afghanistan', 'super12': True, 'group': '2'},
    {'shortname': 'AUS', 'longname': 'Australia', 'super12': True, 'group': '1'},
    {'shortname': 'BAN', 'longname': 'Bangladesh', 'super12': True, 'group': '1'},
    {'shortname': 'ENG', 'longname': 'England', 'super12': True, 'group': '1'},
    {'shortname': 'IND', 'longname': 'India', 'super12': True, 'group': '2'},
    {'shortname': 'IRE', 'longname': 'Ireland', 'super12': False},
    {'shortname': 'NAM', 'longname': 'Namibia', 'super12': False},
    {'shortname': 'NED', 'longname': 'Netherlands', 'super12': False},
    {'shortname': 'NZ', 'longname': 'New Zealand', 'super12': True, 'group': '2'},
    {'shortname': 'OMN', 'longname': 'Oman', 'super12': False},
    {'shortname': 'PAK', 'longname': 'Pakistan', 'super12': True, 'group': '2'},
    {'shortname': 'PNG', 'longname': 'Papua New Guinea', 'super12': False},
    {'shortname': 'SCO', 'longname': 'Scotland', 'super12': True,  'group': '2'},
    {'shortname': 'SA', 'longname': 'South Africa', 'super12': True, 'group': '1'},
    {'shortname': 'SRI', 'longname': 'Srilanka', 'super12': True, 'group': '1'},
    {'shortname': 'WI', 'longname': 'West Indies', 'super12': True, 'group': '1'},
    {'shortname': 'A2', 'longname': 'RunnerUp Group A', 'super12': True, 'group': '2'},
]

GROUP_CHOICES = [
    ('1', '1'),
    ('2', '2'),
]

STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('completed', 'Completed'),
    ('abandoned', 'Abandoned'),
]

WIN_CHOICES = [
    ('wickets', 'wickets'),
    ('runs', 'runs')
]

MATCH_CHOICES = [
    ('super12', 'Super 12'),
    ('sf', 'Semi Final'),
    ('final', 'Final'),
]

BET_STATUS = [
    ('placed', 'Placed'),
    ('default', 'Default'),
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('noresult', 'No Result'),
]
