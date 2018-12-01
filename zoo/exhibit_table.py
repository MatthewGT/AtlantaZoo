from flask_table import Table, Col, LinkCol

class Results(Table):
    Name = Col('Name')
    Size = Col('Size')
    WaterFeature = Col('WaterFeature')

