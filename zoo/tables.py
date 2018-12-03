from flask_table import Table, Col, LinkCol

class exhibit_table(Table):
    Name = Col('Name')
    Size = Col('Size')
    Num_animal = Col('Num_animal')
    WaterFeature = Col('WaterFeature')
    exhibit_detail = LinkCol('Exhibit Detail','exhibit_detail',url_kwargs=dict(Name='Name'))

class exhibit_detail_table(Table):
    Name = Col('Name')
    Size = Col('Size')
    Num_animal = Col('Num_animal')
    WaterFeature = Col('WaterFeature')
    log_visit = LinkCol('log visit','log_visit',url_kwargs=dict(Name='Name',DName='Name'))


class show_table(Table):
    Name = Col('Name')
    Exhibit = Col('Exhibit')
    Datetime = Col('Datetime')
    show_log_visit = LinkCol('show log visit','show_log_visit',url_kwargs=dict(Name='Name',Datetime='Datetime'))


class staff_show_table(Table):
    Name = Col('Name')
    Exhibit = Col('Exhibit')
    Datetime = Col('Datetime')

class animal_detail_table(Table):
    Name = Col('Name')
    Species = Col('Species')
    Exhibit = Col('Exhibit',show=False)
    animal_detail = LinkCol('Animal Detail','view_animal_detail',url_kwargs=dict(Name='Name',Species='Species',Ename ='Exhibit'))

class animal_table(Table):
    Name = Col('Name')
    Species = Col('Species')
    Age =Col('Age')
    Exhibit = Col('Exhibit')
    Type = Col('Type')

class exhibit_animal_table(Table):
    Name = Col('Name')
    Species = Col('Species')
    Age =Col('Age')
    Exhibit = Col('Exhibit')
    Type = Col('Type')
    exhibit_detail = LinkCol('Exhibit Detail','exhibit_detail',url_kwargs=dict(Name='Exhibit'))

class staff_animal_table(Table):
    Name = Col('Name')
    Species = Col('Species')
    Age =Col('Age')
    Exhibit = Col('Exhibit')
    Type = Col('Type')
    animal_care_detail = LinkCol('Animal Care Detail','animal_care_detail',url_kwargs=dict(Name='Name',Species='Species'))

class animal_care_table(Table):
    StaffMember = Col('StaffMember')
    Text = Col('Note')
    Datetime = Col('Datetime')
    


class viewexhibit_table(Table):
    Exhibit = Col('Name')
    Datetime = Col('Datetime')
    Num_visit = Col('Num_visit')
    exhibit_detail = LinkCol('Exhibit Detail','exhibit_history_detail',url_kwargs=dict(Exhibit='Exhibit'))


class viewshow_table(Table):
    Name = Col('Show Name')
    Datetime = Col('Datetime')
    Exhibit = Col('Exhibit')


class admin_visitor_table(Table):
    Username = Col('Visitor Name')
    Email = Col('Email')
    delete = LinkCol('Delete Visitor','delete_visitor',url_kwargs=dict(Username='Username'))


class admin_staff_table(Table):
    Username = Col('Staff Name')
    Email = Col('Email')
    delete = LinkCol('Delete Staff','delete_staff',url_kwargs=dict(Username='Username'))

class admin_show_table(Table):
    Name = Col('Name')
    Exhibit = Col('Exhibit')
    Datetime = Col('Datetime')
    delete = LinkCol('Delete Show','delete_show',url_kwargs=dict(Name='Name',Datetime='Datetime'))

class admin_animal_table(Table):
    Name = Col('Name')
    Species = Col('Species')
    Age =Col('Age')
    Exhibit = Col('Exhibit')
    Type = Col('Type')
    delete = LinkCol('Delete Animal','delete_animal',url_kwargs=dict(Name='Name',Species='Species'))
