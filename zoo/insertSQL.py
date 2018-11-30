from hell_cp import db, User, Staff, Admin, Visitor, Animal,Show,Exhibit,AnimalCare,VisitShow,VisitExhibit



if __name__ == '__main__':
	db.drop_all()
	db.create_all()

	##inset user data
	usernames = ['martha_johnson','benjamin_rao','ethan_roswell','xavier_swenson','isabella_rodriguez','nadias_tevens','robert_bernheardt','admin1']
	passwords = ['password1','password2','password3','password4','password5','password6','password7','adminpassword']
	emails = ['marthajohnson@hotmail.com','benjaminrao@gmail.com','ethanroswell@yahoo.com','xavierswenson@outlook.com','isabellarodriguez@mail.com','nadiastevens@gmail.com','robertbernheardt@yahoo.com','adminemail@mail.com']
	types = ['staff','staff','staff','visitor','visitor','visitor','visitor','admin']
	for i in range(len(usernames)):
		if(types[i] == 'staff'):
			username = User(Username=usernames[i],Password=passwords[i],Email=emails[i],UserType=types[i])
			staffname = Staff(user_staff=username)
			db.session.add_all([username,staffname])
			db.session.commit()
		if(types[i] == 'visitor'):
			username = User(Username=usernames[i],Password=passwords[i],Email=emails[i],UserType=types[i])
			visitorname = Visitor(user_visitor=username)
			db.session.add_all([username,visitorname])
			db.session.commit()
		if(types[i] == 'admin'):
			username = User(Username=usernames[i],Password=passwords[i],Email=emails[i],UserType=types[i])
			adminname = Admin(user_admin=username)
			db.session.add_all([username,adminname])
			db.session.commit()

	##insert exhibit data
	exhibitnames = ['Pacific','Jungle','Sahara','Mountainous','Birds']
	WaterFeatures = ['Yes','No', 'No','No','Yes']
	sizes = [850,600,1000,1200,1000]
	for i in range(len(exhibitnames)):
		exhibit = Exhibit(Name=exhibitnames[i],WaterFeature=WaterFeatures[i],Size=sizes[i])
		db.session.add(exhibit)
		db.session.commit()

	###insert show data
	shownames = ['Jungle Cruise','Feed the Fish','Fun Facts','Climbing','Flight of the Birds','Jungle Cruise','Feed the Fish','Fun Facts','Climbing','Flight of the Birds','Bald Eagle Show']
	Datetimes = ['10/6/18 9:00AM','10/8/18 12:00PM','10/9/18 3:00PM','10/10/18 4:00PM','10/11/18 3:00PM','10/12/18 2:00PM','10/12/18 2:00PM','10/13/18 1:00PM','10/13/18 5:00PM','10/14/18 2:00PM','10/15/18 2:00PM']
	hosts = ['martha_johnson','martha_johnson','martha_johnson','benjamin_rao','ethan_roswell','martha_johnson','ethan_roswell','benjamin_rao','benjamin_rao','ethan_roswell','ethan_roswell']
	exhibitnames = ['Jungle','Pacific','Sahara','Mountainous','Birds','Jungle','Pacific','Sahara','Mountainous','Birds','Birds']
	for i in range(len(shownames)):
		show = Show(Name=shownames[i],Datetime=Datetimes[i],Host=hosts[i],Exhibit=exhibitnames[i])
		db.session.add(show)
		db.session.commit()

	###insert animal data 
	animalnames = ['Goldy','Nemo','Pedro','Lincoln','Greg','Brad']
	speciesname = ['Goldfish','Clownfish','Poison Dart frog','Lion','Goat','Bald Eagle']
	types = ['Fish','Fish','Amphibian','Mammal','Mammal','Bird']
	ages = [1,2,3,8,6,4]
	exhibitnames = ['Pacific','Pacific','Jungle','Sahara','Mountainous','Birds']
	for i in range(len(ages)):
		animal = Animal(Name=animalnames[i],Species=speciesname[i],Type=types[i],Age=ages[i],Exhibit=exhibitnames[i])
		db.session.add(animal)
		db.session.commit()

