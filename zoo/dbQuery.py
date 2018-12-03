from flask import Flask, render_template
import pymysql

app = Flask(__name__)


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "wei.0423"
        db = "test"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()


    def get_user(self,email):
        self.cur.execute("SELECT * FROM test.user where Email = (%s)",(email))
        result = self.cur.fetchall()
        return result
    def get_user_username(self,UserName):
        self.cur.execute("SELECT * FROM test.user where Username = (%s)",(UserName))
        result = self.cur.fetchall()
        return result

    def register_user(self,username, email,  usertype, password):
        self.cur.execute("INSERT INTO test.user values ('"+username+"', '"+email+"', '"+usertype+"', '"+password+"')")
        if(usertype == "visitor"):
            self.cur.execute("INSERT INTO test.visitor values ('"+username+"')")
        elif(usertype == "staff"):
            self.cur.execute("INSERT INTO test.staff values ('"+username+"')")
        self.con.commit()


##########Visitor operation

    def search_exhibits_visitor(self, ExhibitName, NumAnimalMax, NumAnimalMin, SizeMax, SizeMin, WaterFeature):
        a = "SELECT Name, Size, Num_animal, WaterFeature FROM test.Exhibit , (SELECT test.Exhibit.Name As Ename, COUNT( * ) AS Num_animal FROM test.Exhibit LEFT OUTER JOIN test.Animal ON test.Exhibit.Name = test.Animal.Exhibit GROUP BY Ename) AS temp WHERE test.Exhibit.Name = temp.Ename And test.Exhibit.Size >= %s AND test.Exhibit.Size <= %s AND Num_Animal >= %s AND Num_Animal <= %s "
        if ExhibitName != "":
            a = a +  "AND test.Exhibit.Name = '"+ExhibitName+"'"
        if WaterFeature != "":
            a = a +  "AND test.Exhibit.WaterFeature = '"+WaterFeature+"'"
        self.cur.execute(a, (SizeMin, SizeMax, NumAnimalMin, NumAnimalMax))
        result = self.cur.fetchall()
        return result

    def search_show_visitor(self, ShowName, ExhibitName, Date_Time):
        a = "SELECT Name, Datetime, Exhibit FROM test.Show WHERE True "
        if ShowName != "":
            a = a + "AND test.Show.Name = '"+ShowName+"'"
        if ExhibitName != "":
            a = a + "AND test.Show.Exhibit = '"+ExhibitName+"'"
        if Date_Time != "":
            a = a + "AND test.Show.Datetime = '"+Date_Time+"'"
        self.cur.execute(a)
        result = self.cur.fetchall()
        return result

    def search_animal_visitor(self, AnimalName, ExhibitName, MinAge, MaxAge, Species, Type):
        a = "SELECT Name, Species, Type, Age, Exhibit FROM test.Animal WHERE test.Animal.Age >= %s AND test.Animal.Age <= %s "
        if AnimalName != "":
            a = a + "AND test.Animal.Name = '"+AnimalName+"'"
        if Species != "":
            a = a + "AND test.Animal.Species = '"+Species+"'"
        if ExhibitName != "":
            a = a + "AND test.Animal.Exhibit = '"+ExhibitName+"'"
        if Type != "":
            a = a + "AND test.Animal.Type = '"+Type+"'"
        self.cur.execute(a, (MinAge, MaxAge))
        result = self.cur.fetchall()
        return result

    def search_exhibit_history(self, ExhibitName, VisitMin, VisitMax, Datetime, username):
        a = "SELECT Exhibit, Datetime, Num_visit FROM test.VisitExhibit, (SELECT Exhibit AS Ename, COUNT( * ) AS Num_visit FROM test.VisitExhibit GROUP BY Ename) AS temp WHERE Exhibit = Ename AND Visitor = '"+username+"' AND Num_visit >= %s AND Num_visit <= %s "
        if ExhibitName != "":
            a = a + "AND Exhibit = '"+ExhibitName+"' "
        if Datetime != "":
            a = a + "AND Datetime = '"+Datetime+"' "
        self.cur.execute(a, (VisitMin, VisitMax))
        result = self.cur.fetchall()
        return result


    def search_show_history(self, ShowName, ExhibitName, Date_Time, UserName):
        a = "SELECT Name, test.VisitShow.Datetime, Exhibit From test.VisitShow, test.Show WHERE test.VisitShow.ShowName = test.Show.Name AND test.VisitShow.Datetime = test.Show.Datetime AND test.VisitShow.Visitor = '"+UserName+"' "
        if ShowName != "":
            a = a + "AND test.VisitShow.ShowName = '"+ShowName+"'"
        if ExhibitName != "":
            a = a + "AND test.Show.Exhibit = '"+ExhibitName+"'"
        if Date_Time != "":
            a = a + "AND test.VisitShow.Datetime = '"+Date_Time+"'"
        self.cur.execute(a)
        result = self.cur.fetchall()
        return result


##########Admin operation
    def view_visitor_admin (self,order):
        a = "SELECT Username, Email FROM test.user WHERE UserType = 'visitor'"
        if (order == 1):
            a = a + "ORDER BY Username"
        if (order == 2):
            a = a + "ORDER BY Username DESC"
        if (order == 3):
            a = a + "ORDER BY Email"
        if (order == 4):
            a = a + "ORDER BY Email DESC"
        self.cur.execute (a)
        result = self.cur.fetchall ()
        return result


    def view_staff_admin (self,order):
        a = "SELECT Username, Email FROM test.user WHERE UserType = 'staff'"
        if (order == 1):
            a = a + "ORDER BY Username"
        if (order == 2):
            a = a + "ORDER BY Username DESC"
        if (order == 3):
            a = a + "ORDER BY Email"
        if (order == 4):
            a = a + "ORDER BY Email DESC"
        self.cur.execute (a)
        result = self.cur.fetchall ()
        return result


    def admin_add_animal(self,Name,Species,Type,Age,Exhibit):
        self.cur.execute ("INSERT INTO test.animal VALUES (%s,%s,%s,%s,%s)",(Name,Species,Type,Age,Exhibit))
        self.con.commit ()


    def admin_add_show(self, Name, Time, Host, Ename):
        self.cur.execute ("INSERT INTO test.show  VALUES (%s,%s,%s,%s)",(Name, Time, Host, Ename))
        self.con.commit ()



###admin operations 
    def admin_delete_visitor (self, Username):
        self.cur.execute ("DELETE FROM test.user WHERE Username = %s",(Username))
        self.con.commit()

    def admin_delete_staff (self, Username):
        self.cur.execute ("DELETE FROM test.user WHERE Username = %s",(Username))
        self.con.commit()


    def admin_delete_show (self,name,datetime):
        self.cur.execute ("DELETE FROM test.show WHERE Name = %s AND Datetime = %s", (name,datetime))
        self.con.commit ()

    def admin_delete_animal (self,Name,Species):
        self.cur.execute ("DELETE FROM test.animal WHERE Name = %s AND Species = %s",(Name,Species))
        self.con.commit ()

###visitor operations
    def visitor_exhibit_detail(self, ExhibitName):
        self.cur.execute("SELECT test.Exhibit.Name, Size, WaterFeature, COUNT(*) AS Num_animal FROM test.Exhibit LEFT OUTER JOIN test.Animal ON test.Exhibit.Name = test.Animal.Exhibit WHERE test.Exhibit.Name = '"+ExhibitName+"' GROUP BY test.Animal.Exhibit")
        result = self.cur.fetchall()
        return result
    def visitor_exhibit_animal(self, ExhibitName):
        self.cur.execute("SELECT Name, Species, Exhibit From Animal Where Exhibit = '"+ExhibitName+"'")
        result = self.cur.fetchall()
        return result
    def exhibit_log_visit(self, username, exhibitname):
        self.cur.execute("INSERT INTO test.VisitExhibit values('"+exhibitname+"','"+username+"', DATE_FORMAT(NOW(), '%m-%d-%Y %h:%i%p'))")
        self.con.commit ()

    def click_animal_detail(self, Name, Species):
        self.cur.execute("SELECT Name, Species, Type, Age, Exhibit From Animal Where Name = '"+Name+"' And Species = '"+Species+"'")
        result = self.cur.fetchall()
        return result

    def show_log_visit(self, username, showname, date_time):
        self.cur.execute("INSERT INTO test.VisitShow values('"+showname+"', '"+date_time+"', '"+username+"')")
        self.con.commit ()


#####staff operations
    def staff_view_show (self,Username,order):
        a = "SELECT Name, Datetime, Exhibit FROM test.show WHERE Host = '"+Username+"'"
        if (order == 1):
            a = a + "ORDER BY Name"
        if (order == 2):
            a = a + "ORDER BY Name DESC"
        if (order == 3):
            a = a + "ORDER BY Datetime"
        if (order == 4):
            a = a + "ORDER BY Datetime DESC"
        if (order == 5):
            a = a + "ORDER BY Exhibit"
        if (order == 6):
            a = a + "ORDER BY Exhibit DESC"
        self.cur.execute (a)
        result = self.cur.fetchall ()
        return result

    def staff_view_note(self,Name, Species, order):
        a = "SELECT StaffMember, Text, Datetime FROM test.animalcare WHERE AnimalName = '"+Name+"' AND SpeciesName = '"+Species+"'"
        if (order == 1):
            a = a + "ORDER BY StaffMember"
        if (order == 2):
            a = a + "ORDER BY StaffMember DESC"
        if (order == 3):
            a = a + "ORDER BY Text"
        if (order == 4):
            a = a + "ORDER BY Text DESC"
        if (order == 5):
            a = a + "ORDER BY Datetime"
        if (order == 6):
            a = a + "ORDER BY Datetime DESC"
        self.cur.execute (a)
        result = self.cur.fetchall ()
        return result

    def staff_log_notes(self,AnimalName,SpeciesName,StaffMember,Text):
        self.cur.execute ("INSERT INTO test.animalcare VALUES ('"+AnimalName+"','"+SpeciesName+"','"+StaffMember+"',DATE_FORMAT(NOW(), '%m-%d-%Y %h:%i%p'),'"+Text+"')")
        self.con.commit ()


##########Find username from Email
    def find_user_name(self, email):
        a = "SELECT Username FROM test.User WHERE test.User.Email = '"+email+"'"
        self.cur.execute(a)
        result = self.cur.fetchall()
        return result



















