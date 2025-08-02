from src.models import db
from flask_login import UserMixin
import datetime

class Event(UserMixin, db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(225), unique=True, nullable=False)
    name = db.Column(db.String(225), nullable=False)
    email = db.Column(db.String(225), nullable=False)
    location = db.Column(db.String(225), nullable=False)
    checked_in = db.Column(db.Boolean, default=False, nullable=True)
    checked_in_time = db.Column(db.DateTime, nullable=True)
    
    @staticmethod
    def get_total_registered():
        """Get the total number of registered users"""
        return Event.query.count()
    
    @staticmethod
    def get_checked_in_attendees():
        """Get checked in attendees count"""
        return Event.query.filter_by(checked_in=True).count()

    @staticmethod
    def get_checked_in_rate():
        """Get rate of checked in attendees over total registered"""
        total_registered = Event.get_total_registered()
        checked_in = Event.get_checked_in_attendees()
        if total_registered > 0:
            return round((checked_in / total_registered) * 100, 1)
        return 0
        
    @staticmethod
    def get_event_capacity():
        """Get the total capacity of the event"""
        return 500
    
    @staticmethod
    def find_by_name_or_serial(name=None, serial=None):
        """Find attendee by name or event_id (serial)"""
        query = Event.query
        
        if name and serial:
            return query.filter_by(name=name, event_id=serial).first()
        elif name:
            return query.filter(Event.name.ilike(f'%{name}%')).first()
        elif serial:
            return query.filter_by(event_id=serial).first()
        
        return None
    
    def check_in_attendee(self):
        """Mark this attendee as checked in"""
        if not self.checked_in:
            self.checked_in = True
            self.checked_in_time = datetime.datetime.utcnow()
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return f'<Event {self.name} - {self.event_id}>'

# Sample attendees data - 97 attendees for testing
attendees = [
    {
        "event_id": "gst-SHoKlPKV5U1wI9j",
        "name": "Usama Abdulhamid Kambari",
        "email": "abdulhamidusamakambari@gmail.com",
        "Location": "Sengere futy"
    },
    {
        "event_id": "gst-5ezcWzcqJto89jz", 
        "name": "Abdullahi Muhammed",
        "email": "abdullahimuhammed7195@gmail.com",
        "Location": "Yola, Adamawa state."
    },
    {
        "event_id": "gst-ABC123XYZ",
        "name": "John Doe",
        "email": "john.doe@example.com", 
        "Location": "Test Location"
    },
    {
        "event_id": "gst-DEF456UVW",
        "name": "Jane Smith", 
        "email": "jane.smith@example.com",
        "Location": "Another Location"
    },
    {
        "event_id": "gst-A1B2C3D4E5",
        "name": "Aisha Mohammed",
        "email": "aisha.mohammed@gmail.com",
        "Location": "Yola North"
    },
    {
        "event_id": "gst-F6G7H8I9J0",
        "name": "Ibrahim Hassan",
        "email": "ibrahim.hassan@yahoo.com",
        "Location": "Jimeta"
    },
    {
        "event_id": "gst-K1L2M3N4O5",
        "name": "Fatima Usman",
        "email": "fatima.usman@hotmail.com",
        "Location": "Yola South"
    },
    {
        "event_id": "gst-P6Q7R8S9T0",
        "name": "Ahmed Aliyu",
        "email": "ahmed.aliyu@gmail.com",
        "Location": "Dougirei"
    },
    {
        "event_id": "gst-U1V2W3X4Y5",
        "name": "Khadija Bello",
        "email": "khadija.bello@yahoo.com",
        "Location": "Karewa"
    },
    {
        "event_id": "gst-Z6A7B8C9D0",
        "name": "Musa Adamu",
        "email": "musa.adamu@gmail.com",
        "Location": "Alkaleri"
    },
    {
        "event_id": "gst-E1F2G3H4I5",
        "name": "Hauwa Garba",
        "email": "hauwa.garba@hotmail.com",
        "Location": "Mbamba"
    },
    {
        "event_id": "gst-J6K7L8M9N0",
        "name": "Yusuf Ibrahim",
        "email": "yusuf.ibrahim@yahoo.com",
        "Location": "Nassarawo"
    },
    {
        "event_id": "gst-O1P2Q3R4S5",
        "name": "Zainab Suleiman",
        "email": "zainab.suleiman@gmail.com",
        "Location": "Luggere"
    },
    {
        "event_id": "gst-T6U7V8W9X0",
        "name": "Umar Yahaya",
        "email": "umar.yahaya@hotmail.com",
        "Location": "Viniklang"
    },
    {
        "event_id": "gst-Y1Z2A3B4C5",
        "name": "Amina Abdullahi",
        "email": "amina.abdullahi@yahoo.com",
        "Location": "Ajiya"
    },
    {
        "event_id": "gst-D6E7F8G9H0",
        "name": "Sani Ahmad",
        "email": "sani.ahmad@gmail.com",
        "Location": "Bekaji"
    },
    {
        "event_id": "gst-I1J2K3L4M5",
        "name": "Halima Musa",
        "email": "halima.musa@hotmail.com",
        "Location": "Wuro Jabbe"
    },
    {
        "event_id": "gst-N6O7P8Q9R0",
        "name": "Bashir Yusuf",
        "email": "bashir.yusuf@yahoo.com",
        "Location": "Yolde Pate"
    },
    {
        "event_id": "gst-S1T2U3V4W5",
        "name": "Maryam Salisu",
        "email": "maryam.salisu@gmail.com",
        "Location": "Sangere"
    },
    {
        "event_id": "gst-X6Y7Z8A9B0",
        "name": "Aliyu Baba",
        "email": "aliyu.baba@hotmail.com",
        "Location": "Yelwa"
    },
    {
        "event_id": "gst-C1D2E3F4G5",
        "name": "Safiya Haruna",
        "email": "safiya.haruna@yahoo.com",
        "Location": "Gwadabawa"
    },
    {
        "event_id": "gst-H6I7J8K9L0",
        "name": "Garba Audu",
        "email": "garba.audu@gmail.com",
        "Location": "Alkaleri Ward"
    },
    {
        "event_id": "gst-M1N2O3P4Q5",
        "name": "Rukayya Danjuma",
        "email": "rukayya.danjuma@hotmail.com",
        "Location": "Wuro Hausa"
    },
    {
        "event_id": "gst-R6S7T8U9V0",
        "name": "Ismail Tanko",
        "email": "ismail.tanko@yahoo.com",
        "Location": "Jabbi Lamba"
    },
    {
        "event_id": "gst-W1X2Y3Z4A5",
        "name": "Nafisa Umar",
        "email": "nafisa.umar@gmail.com",
        "Location": "Makama"
    },
    {
        "event_id": "gst-B6C7D8E9F0",
        "name": "Kabiru Suleiman",
        "email": "kabiru.suleiman@hotmail.com",
        "Location": "Toungo"
    },
    {
        "event_id": "gst-G1H2I3J4K5",
        "name": "Asma'u Balarabe",
        "email": "asmau.balarabe@yahoo.com",
        "Location": "Ribadu"
    },
    {
        "event_id": "gst-L6M7N8O9P0",
        "name": "Salisu Gidado",
        "email": "salisu.gidado@gmail.com",
        "Location": "Kofare"
    },
    {
        "event_id": "gst-Q1R2S3T4U5",
        "name": "Hadiza Mamman",
        "email": "hadiza.mamman@hotmail.com",
        "Location": "Wuro Bokki"
    },
    {
        "event_id": "gst-V6W7X8Y9Z0",
        "name": "Adamu Bello",
        "email": "adamu.bello@yahoo.com",
        "Location": "Sabon Layi"
    },
    {
        "event_id": "gst-A1B2C3D4E6",
        "name": "Mariam Abdulkarim",
        "email": "mariam.abdulkarim@gmail.com",
        "Location": "Wuro Chekke"
    },
    {
        "event_id": "gst-F7G8H9I0J1",
        "name": "Yakubu Ahmadu",
        "email": "yakubu.ahmadu@hotmail.com",
        "Location": "Girei"
    },
    {
        "event_id": "gst-K2L3M4N5O6",
        "name": "Zahra'u Sadiq",
        "email": "zahrau.sadiq@yahoo.com",
        "Location": "Wuro Dole"
    },
    {
        "event_id": "gst-P7Q8R9S0T1",
        "name": "Haruna Jika",
        "email": "haruna.jika@gmail.com",
        "Location": "Gereng"
    },
    {
        "event_id": "gst-U2V3W4X5Y6",
        "name": "Hauwa'u Lawal",
        "email": "hauwau.lawal@hotmail.com",
        "Location": "Wuro Boki"
    },
    {
        "event_id": "gst-Z7A8B9C0D1",
        "name": "Abdullahi Abubakar",
        "email": "abdullahi.abubakar@yahoo.com",
        "Location": "Mayo Belwa"
    },
    {
        "event_id": "gst-E2F3G4H5I6",
        "name": "Falmata Hassan",
        "email": "falmata.hassan@gmail.com",
        "Location": "Bangshika"
    },
    {
        "event_id": "gst-J7K8L9M0N1",
        "name": "Muhammad Tijjani",
        "email": "muhammad.tijjani@hotmail.com",
        "Location": "Lamurde"
    },
    {
        "event_id": "gst-O2P3Q4R5S6",
        "name": "Rabi'a Yusuf",
        "email": "rabia.yusuf@yahoo.com",
        "Location": "Song"
    },
    {
        "event_id": "gst-T7U8V9W0X1",
        "name": "Isa Garba",
        "email": "isa.garba@gmail.com",
        "Location": "Fufore"
    },
    {
        "event_id": "gst-Y2Z3A4B5C6",
        "name": "Fatima Aliyu",
        "email": "fatima.aliyu@hotmail.com",
        "Location": "Shelleng"
    },
    {
        "event_id": "gst-D7E8F9G0H1",
        "name": "Sulaiman Buba",
        "email": "sulaiman.buba@yahoo.com",
        "Location": "Madagali"
    },
    {
        "event_id": "gst-I2J3K4L5M6",
        "name": "Aisha Maina",
        "email": "aisha.maina@gmail.com",
        "Location": "Michika"
    },
    {
        "event_id": "gst-N7O8P9Q0R1",
        "name": "Usman Bala",
        "email": "usman.bala@hotmail.com",
        "Location": "Mubi North"
    },
    {
        "event_id": "gst-S2T3U4V5W6",
        "name": "Khadija Umar",
        "email": "khadija.umar@yahoo.com",
        "Location": "Mubi South"
    },
    {
        "event_id": "gst-X7Y8Z9A0B1",
        "name": "Ibrahim Sadiq",
        "email": "ibrahim.sadiq@gmail.com",
        "Location": "Numan"
    },
    {
        "event_id": "gst-C2D3E4F5G6",
        "name": "Hafsat Ahmed",
        "email": "hafsat.ahmed@hotmail.com",
        "Location": "Demsa"
    },
    {
        "event_id": "gst-H7I8J9K0L1",
        "name": "Ali Mamman",
        "email": "ali.mamman@yahoo.com",
        "Location": "Gombi"
    },
    {
        "event_id": "gst-M2N3O4P5Q6",
        "name": "Zulaiha Sani",
        "email": "zulaiha.sani@gmail.com",
        "Location": "Hong"
    },
    {
        "event_id": "gst-R7S8T9U0V1",
        "name": "Aminu Jalo",
        "email": "aminu.jalo@hotmail.com",
        "Location": "Jada"
    },
    {
        "event_id": "gst-W2X3Y4Z5A6",
        "name": "Halima Abubakar",
        "email": "halima.abubakar@yahoo.com",
        "Location": "Ganye"
    },
    {
        "event_id": "gst-B7C8D9E0F1",
        "name": "Yusuf Bello",
        "email": "yusuf.bello@gmail.com",
        "Location": "Toungo Ward"
    },
    {
        "event_id": "gst-G2H3I4J5K6",
        "name": "Maimuna Hassan",
        "email": "maimuna.hassan@hotmail.com",
        "Location": "Mayo Farang"
    },
    {
        "event_id": "gst-L7M8N9O0P1",
        "name": "Ahmad Babangida",
        "email": "ahmad.babangida@yahoo.com",
        "Location": "Guyuk"
    },
    {
        "event_id": "gst-Q2R3S4T5U6",
        "name": "Sauda Musa",
        "email": "sauda.musa@gmail.com",
        "Location": "Yola Ward"
    },
    {
        "event_id": "gst-V7W8X9Y0Z1",
        "name": "Abubakar Saleh",
        "email": "abubakar.saleh@hotmail.com",
        "Location": "Jimeta Ward"
    },
    {
        "event_id": "gst-A2B3C4D5E7",
        "name": "Hafsa Ibrahim",
        "email": "hafsa.ibrahim@yahoo.com",
        "Location": "Bachure"
    },
    {
        "event_id": "gst-F8G9H0I1J2",
        "name": "Murtala Adamu",
        "email": "murtala.adamu@gmail.com",
        "Location": "Kilange"
    },
    {
        "event_id": "gst-K3L4M5N6O7",
        "name": "Aisha Garba",
        "email": "aisha.garba@hotmail.com",
        "Location": "Limawa"
    },
    {
        "event_id": "gst-P8Q9R0S1T2",
        "name": "Hamisu Yakubu",
        "email": "hamisu.yakubu@yahoo.com",
        "Location": "Mbamba Ward"
    },
    {
        "event_id": "gst-U3V4W5X6Y7",
        "name": "Fatima Bello",
        "email": "fatima.bello@gmail.com",
        "Location": "Ngurore"
    },
    {
        "event_id": "gst-Z8A9B0C1D2",
        "name": "Salihu Usman",
        "email": "salihu.usman@hotmail.com",
        "Location": "Damare"
    },
    {
        "event_id": "gst-E3F4G5H6I7",
        "name": "Zainab Hassan",
        "email": "zainab.hassan@yahoo.com",
        "Location": "Pariya"
    },
    {
        "event_id": "gst-J8K9L0M1N2",
        "name": "Abdulkarim Jika",
        "email": "abdulkarim.jika@gmail.com",
        "Location": "Bole"
    },
    {
        "event_id": "gst-O3P4Q5R6S7",
        "name": "Hadiza Sani",
        "email": "hadiza.sani@hotmail.com",
        "Location": "Wuro Patuwal"
    },
    {
        "event_id": "gst-T8U9V0W1X2",
        "name": "Aliyu Hassan",
        "email": "aliyu.hassan@yahoo.com",
        "Location": "Gombe Abba"
    },
    {
        "event_id": "gst-Y3Z4A5B6C7",
        "name": "Mariam Baba",
        "email": "mariam.baba@gmail.com",
        "Location": "Wuro Gude"
    },
    {
        "event_id": "gst-D8E9F0G1H2",
        "name": "Sani Mamman",
        "email": "sani.mamman@hotmail.com",
        "Location": "Rumde"
    },
    {
        "event_id": "gst-I3J4K5L6M7",
        "name": "Rahma Umar",
        "email": "rahma.umar@yahoo.com",
        "Location": "Wuro Bagga"
    },
    {
        "event_id": "gst-N8O9P0Q1R2",
        "name": "Garba Suleiman",
        "email": "garba.suleiman@gmail.com",
        "Location": "Alkaleri Central"
    },
    {
        "event_id": "gst-S3T4U5V6W7",
        "name": "Amina Jalo",
        "email": "amina.jalo@hotmail.com",
        "Location": "Wuro Yero"
    },
    {
        "event_id": "gst-X8Y9Z0A1B2",
        "name": "Yakubu Aliyu",
        "email": "yakubu.aliyu@yahoo.com",
        "Location": "Sabon Gari"
    },
    {
        "event_id": "gst-C3D4E5F6G7",
        "name": "Nafisa Ahmed",
        "email": "nafisa.ahmed@gmail.com",
        "Location": "Yelwa Gongoba"
    },
    {
        "event_id": "gst-H8I9J0K1L2",
        "name": "Muhammad Bello",
        "email": "muhammad.bello@hotmail.com",
        "Location": "Gwadabawa Central"
    },
    {
        "event_id": "gst-M3N4O5P6Q7",
        "name": "Hafsat Haruna",
        "email": "hafsat.haruna@yahoo.com",
        "Location": "Namtari"
    },
    {
        "event_id": "gst-R8S9T0U1V2",
        "name": "Isma'il Garba",
        "email": "ismail.garba@gmail.com",
        "Location": "Alkaleri East"
    },
    {
        "event_id": "gst-W3X4Y5Z6A7",
        "name": "Khadija Aliyu",
        "email": "khadija.aliyu@hotmail.com",
        "Location": "Wuro Haawa"
    },
    {
        "event_id": "gst-B8C9D0E1F2",
        "name": "Usman Jika",
        "email": "usman.jika@yahoo.com",
        "Location": "Doubeli"
    },
    {
        "event_id": "gst-G3H4I5J6K7",
        "name": "Sakinah Umar",
        "email": "sakinah.umar@gmail.com",
        "Location": "Sangere Shuwa"
    },
    {
        "event_id": "gst-L8M9N0O1P2",
        "name": "Ahmad Hassan",
        "email": "ahmad.hassan@hotmail.com",
        "Location": "Wuro Nyibango"
    },
    {
        "event_id": "gst-Q3R4S5T6U7",
        "name": "Hauwa Baba",
        "email": "hauwa.baba@yahoo.com",
        "Location": "Tella"
    },
    {
        "event_id": "gst-V8W9X0Y1Z2",
        "name": "Musa Aliyu",
        "email": "musa.aliyu@gmail.com",
        "Location": "Wuro Lainde"
    },
    {
        "event_id": "gst-A3B4C5D6E8",
        "name": "Zulaihat Mamman",
        "email": "zulaihat.mamman@hotmail.com",
        "Location": "Ribadu Square"
    },
    {
        "event_id": "gst-F9G0H1I2J3",
        "name": "Kabiru Hassan",
        "email": "kabiru.hassan@yahoo.com",
        "Location": "Karewa Central"
    },
    {
        "event_id": "gst-K4L5M6N7O8",
        "name": "Fatima Jika",
        "email": "fatima.jika@gmail.com",
        "Location": "Demsawo"
    },
    {
        "event_id": "gst-P9Q0R1S2T3",
        "name": "Abdullahi Garba",
        "email": "abdullahi.garba@hotmail.com",
        "Location": "Makama A"
    },
    {
        "event_id": "gst-U4V5W6X7Y8",
        "name": "Maryam Hassan",
        "email": "maryam.hassan@yahoo.com",
        "Location": "Luggere Central"
    },
    {
        "event_id": "gst-Z9A0B1C2D3",
        "name": "Yusuf Aliyu",
        "email": "yusuf.aliyu@gmail.com",
        "Location": "Wuro Billi"
    },
    {
        "event_id": "gst-E4F5G6H7I8",
        "name": "Aisha Bello",
        "email": "aisha.bello@hotmail.com",
        "Location": "Nassarawo Central"
    },
    {
        "event_id": "gst-J9K0L1M2N3",
        "name": "Suleiman Umar",
        "email": "suleiman.umar@yahoo.com",
        "Location": "Viniklang Central"
    },
    {
        "event_id": "gst-O4P5Q6R7S8",
        "name": "Halima Hassan",
        "email": "halima.hassan@gmail.com",
        "Location": "Ajiya Central"
    },
    {
        "event_id": "gst-T9U0V1W2X3",
        "name": "Muhammad Aliyu",
        "email": "muhammad.aliyu@hotmail.com",
        "Location": "Bekaji Central"
    },
    {
        "event_id": "gst-Y4Z5A6B7C8",
        "name": "Khadijat Bello",
        "email": "khadijat.bello@yahoo.com",
        "Location": "Wuro Jabbe Central"
    },
    {
        "event_id": "gst-D9E0F1G2H3",
        "name": "Ibrahim Usman",
        "email": "ibrahim.usman@gmail.com",
        "Location": "Yolde Pate Central"
    },
    {
        "event_id": "gst-I4J5K6L7M8",
        "name": "Safiyyah Hassan",
        "email": "safiyyah.hassan@hotmail.com",
        "Location": "Sangere Central"
    },
    {
        "event_id": "gst-N9O0P1Q2R3",
        "name": "Aliyu Mamman",
        "email": "aliyu.mamman@yahoo.com",
        "Location": "Yelwa Central"
    },
    {
        "event_id": "gst-S4T5U6V7W8",
        "name": "Rukayya Hassan",
        "email": "rukayya.hassan@gmail.com",
        "Location": "Gwadabawa East"
    },
    {
        "event_id": "gst-X9Y0Z1A2B3",
        "name": "Ahmad Bello",
        "email": "ahmad.bello@hotmail.com",
        "Location": "Alkaleri West"
    },
    {
        "event_id": "gst-C4D5E6F7G8",
        "name": "Hadiza Aliyu",
        "email": "hadiza.aliyu@yahoo.com",
        "Location": "Wuro Hausa Central"
    },
    {
        "event_id": "gst-H9I0J1K2L3",
        "name": "Bashir Hassan",
        "email": "bashir.hassan@gmail.com",
        "Location": "Jabbi Lamba Central"
    },
    {
        "event_id": "gst-M4N5O6P7Q8",
        "name": "Zainab Bello",
        "email": "zainab.bello@hotmail.com",
        "Location": "Makama Central"
    }
]