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
        """Find attendee by name or event_id (serial) - case insensitive"""
        from sqlalchemy import or_
        query = Event.query
        
        if name and serial:
            # Both name and serial provided - use OR condition for verification
            return query.filter(
                or_(
                    Event.name.ilike(f'%{name}%'),
                    Event.event_id.ilike(serial)
                )
            ).first()
        elif name:
            # Only name provided - case-insensitive search
            return query.filter(Event.name.ilike(f'%{name}%')).first()
        elif serial:
            # Only serial provided - case-insensitive search
            return query.filter(Event.event_id.ilike(serial)).first()
        
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
    "event_id": "gst-3wIPpMhrtDECV8O",
    "name": "Favour Abraham",
    "email": "abrahamfavour97@gmail.com",
    "Location": "Modibbo Adama University, Yola"
  },
  {
    "event_id": "gst-IYJISAmPz9jtiBD",
    "name": "Afiyina Yohanna Sandreson",
    "email": "afiyinayohannas@gmail.com",
    "Location": "MAU"
  },
  {
    "event_id": "gst-kwLsaJCXqwVXkQe",
    "name": "Catherine Yadima",
    "email": "ajicatherineyadima@gmail.com",
    "Location": "Federal housing"
  },
  {
    "event_id": "gst-6Y3XanAC1QF4X7N",
    "name": "Blessing Sarah",
    "email": "akinyoblessing@gmail.com",
    "Location": "Adamawa"
  },
  {
    "event_id": "gst-MVrOAYBBo2B8jKA",
    "name": "ALIYU SAAD BOSE",
    "email": "aliyusaadbose@gmail.com",
    "Location": "Modibbo Adama University Yola"
  },
  {
    "event_id": "gst-HUGhLNs3ENZrKTZ",
    "name": "Musa Abdulrahman Murtala",
    "email": "ammurtala1995@gmail.com",
    "Location": "Modibbo Adama university Yola"
  },
  {
    "event_id": "gst-4CzIhoQ0QI21wxs",
    "name": "Augustine Augustina Lucina",
    "email": "augustinea676@gmail.com",
    "Location": "Shagari phase two yola town"
  },
  {
    "event_id": "gst-pIgA9DHAoC7zGmJ",
    "name": "Augustine Ishaya",
    "email": "augustineishaya10@gmail.com",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-3K0RkkaVjt5SJFv",
    "name": "AUWAL idris",
    "email": "auwalidrisdarazo@gmail.com",
    "Location": "Futy"
  },
  {
    "event_id": "gst-UNpSY2134boMflA",
    "name": "Christopher Danlami Baba",
    "email": "christopherbaba715@gmail.com",
    "Location": "Sangere Futy"
  },
  {
    "event_id": "gst-5uICy0hjFmytOyc",
    "name": "Cletus Muoneke",
    "email": "cletusmuoneke23@gmail.com",
    "Location": "Behind jambutu motor park"
  },
  {
    "event_id": "gst-MJMjwUcGS2Fcnng",
    "name": "Beecroft Comfort",
    "email": "comfortbeecroft@gmail.com",
    "Location": "Adamawa State"
  },
  {
    "event_id": "gst-1WMatJ93b3Q6UWR",
    "name": "Daniel Garba",
    "email": "danielgarba101@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-9AQCKnBHSeoF6La",
    "name": "Daniel-Praise Eleojo Israel",
    "email": "danielpraiseisrael@gmail.com",
    "Location": ""
  },
  {
    "event_id": "gst-JCERbWCVlEZrENC",
    "name": "Dan Jumaa Ojei",
    "email": "danjumaaojei@mcc.org",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-ZNLN8bdgXrl2CPK",
    "name": "Deborah hasley Mohammed pori",
    "email": "deborahasley33@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-FCIAskLej3FSR2k",
    "name": "Deborah Ademola",
    "email": "deborahthedoc@gmail.com",
    "Location": ""
  },
  {
    "event_id": "gst-0Rf6XIKVOjVb0RA",
    "name": "Denis Denham Babangida",
    "email": "denisbabangida7@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-9S3vUWZQe7aaRqA",
    "name": "Faith Elihu Dalatu",
    "email": "elihufaithdalatu@gmail.com",
    "Location": "Modibbo Adama University Yola."
  },
  {
    "event_id": "gst-x8ooZLqbzvKRD6o",
    "name": "Enoch Augustine",
    "email": "enochaugustine17@gmail.com",
    "Location": "Adamawa State polytechnic"
  },
  {
    "event_id": "gst-EAEpUEEc4JUYKaj",
    "name": "Esthon Anyimauna",
    "email": "esthonanyimauna1@gmail.com",
    "Location": "MAU Yola"
  },
  {
    "event_id": "gst-CE7BUHV1Qf7mFE2",
    "name": "Florence Hauwa Aliyu",
    "email": "florencealiyu3@gmail.com",
    "Location": "Jimeta, Yola"
  },
  {
    "event_id": "gst-gjzVOlWfDCN0HL9",
    "name": "Frama Stephen",
    "email": "framastephen200@gmail.com",
    "Location": "Yola south"
  },
  {
    "event_id": "gst-CeUCAumyOs0Un5c",
    "name": "davidfromthenorth",
    "email": "fromthenorthsouth@gmail.com",
    "Location": "MODIBBO ADAMA UNIVERSITY YOLA"
  },
  {
    "event_id": "gst-Xml6kqr1xJlmoZB",
    "name": "Gabiya Danladi Yusuf",
    "email": "gabiyayusuf2019@gmail.com",
    "Location": "Girei"
  },
  {
    "event_id": "gst-tewQEBmsLgEaYXO",
    "name": "Gayawan Obida",
    "email": "gaya1obid@gmail.com",
    "Location": "Adamawa state"
  },
  {
    "event_id": "gst-IEm4CdKmRUxnLEX",
    "name": "Gideon",
    "email": "gideonmallam406@gmail.com",
    "Location": "Karu LGA, mararaba nasarawa state"
  },
  {
    "event_id": "gst-7GIe68kjUUUCI2U",
    "name": "Aisha Cheered Gloria Solomon From",
    "email": "gloriasolos01@gmail.com",
    "Location": "Adamawa State Nigeria"
  },
  {
    "event_id": "gst-Vua7K3GHDKGvAeG",
    "name": "Godwin Johnbaba",
    "email": "godwinjohnbaba@gmail.com",
    "Location": ""
  },
  {
    "event_id": "gst-oaHEBR0hDvCQwBn",
    "name": "Philip Godwin",
    "email": "godwinphilip139@gmail.com",
    "Location": "Bachure opposite Army Barracks Jimeta Yola"
  },
  {
    "event_id": "gst-KhEtGFc7XHf3zWR",
    "name": "Grace Markus Gwandi",
    "email": "gracegwandy@gmail.com",
    "Location": "Mautech"
  },
  {
    "event_id": "gst-JzpBfQi32cw3Gir",
    "name": "Hafsat Umar Sa'eed",
    "email": "hafsatumarsaeed2002@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-1ZfuJMyHbASbyLD",
    "name": "Ilochi Chibuzor Audu",
    "email": "hamiltonilochi90@gmail.com",
    "Location": "BADIRISA"
  },
  {
    "event_id": "gst-YUJI0RPTtoUldhr",
    "name": "Hassan Kwaghe Zira",
    "email": "hassankwaghe56@gmail.com",
    "Location": "Yola yoldepate"
  },
  {
    "event_id": "gst-CKXgHMUyf30yEWf",
    "name": "Hope Herbert",
    "email": "hopehanawa12@gmail.com",
    "Location": "Federal housing estate"
  },
  {
    "event_id": "gst-SXwtIO9sIlI3e1p",
    "name": "hyelladi alheri",
    "email": "hyelladi45@gmail.com",
    "Location": "Modibbo Adama University, Yola"
  },
  {
    "event_id": "gst-0CIeRmMaB1whnGP",
    "name": "Hyellablati Joseph",
    "email": "hyellajoseph29@gmail.com",
    "Location": "Bachure"
  },
  {
    "event_id": "gst-5xX7WzSpLuqm9r6",
    "name": "Ibrahim Mohammed Tukur",
    "email": "ibrahim84tukur@gmail.com",
    "Location": "Yola town, Lamido palace"
  },
  {
    "event_id": "gst-EHeGdBkxYxMQ1nA",
    "name": "Johnson 2",
    "email": "innoshg4@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-78OKni7SqHNiAw0",
    "name": "David Mani Ibrahim",
    "email": "itzlimincj@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-fvmi1DdXIl4K5eW",
    "name": "Muhammad Aliyu Jabbijo",
    "email": "jabbijo@gmail.com",
    "Location": "Girei"
  },
  {
    "event_id": "gst-T436M5twF89MVaG",
    "name": "Jessica Jacob",
    "email": "jacobjessica419@gmail.com",
    "Location": "MAU"
  },
  {
    "event_id": "gst-UJWXniQRxrda6wy",
    "name": "James Jairus Chabiri",
    "email": "jairusjames2004@gmail.com",
    "Location": "MAU"
  },
  {
    "event_id": "gst-2SuqFKRLFgTBjHZ",
    "name": "Jatong Deborah",
    "email": "jatdeb018@gmail.com",
    "Location": "Sangere Futy"
  },
  {
    "event_id": "gst-i2MV5wrqB9qt34H",
    "name": "Jatong Angela Maranzo",
    "email": "jatongangela@gmail.com",
    "Location": "Sangere futy"
  },
  {
    "event_id": "gst-wWwoxm2GgxrxcZm",
    "name": "Jennifer Havila",
    "email": "jenniferabanyi@gmail.com",
    "Location": "Sangere futy"
  },
  {
    "event_id": "gst-9A31UHQaq2Az0OP",
    "name": "Joy wuike Iliya",
    "email": "joywuikeiliya@gmail.com",
    "Location": "Modibbo Adama University, MAU YOLA"
  },
  {
    "event_id": "gst-WAxfwj15ce0MIgV",
    "name": "Judith Dati",
    "email": "judithpeter153@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-pn4g4DHcLuvbVQF",
    "name": "Julius Bayo",
    "email": "juliusadebayoaremu@gmail.com",
    "Location": "Sangere Futy"
  },
  {
    "event_id": "gst-nuQlt4M5dHwhzHq",
    "name": "Justice Luka Tizhe",
    "email": "justicestringz@gmail.com",
    "Location": "Yola, Nigeria"
  },
  {
    "event_id": "gst-63RAnuM5KZTxrIN",
    "name": "Kafte",
    "email": "kaftetemantika@gmail.com",
    "Location": "Girei"
  },
  {
    "event_id": "gst-ClY5BE2LWtueyA8",
    "name": "Veruwa",
    "email": "kalepvmasi@gmail.com",
    "Location": "Modibbo Adama University Yola"
  },
  {
    "event_id": "gst-qAwkrZTHhGzZt5v",
    "name": "Kauna Elkanah",
    "email": "kaunaelkanah@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-9HyRBaU9ZmEPd1q",
    "name": "Christopher Solomon",
    "email": "krissongs123@gmail.com",
    "Location": "Adamawa"
  },
  {
    "event_id": "gst-eHCwWKbSwBNy9eV",
    "name": "Gideon Eli",
    "email": "lastyblack@gmail.com",
    "Location": "Adamawa Yola"
  },
  {
    "event_id": "gst-9EoiFYBNWfznHqy",
    "name": "Lilian Iliya",
    "email": "lilianbeshi16@gmail.com",
    "Location": "Modibbo Adama University, Girei"
  },
  {
    "event_id": "gst-aeTZmVDkPTca16U",
    "name": "Hannah Lubba",
    "email": "lubbahannah18@gmail.com",
    "Location": "Yola, Adamawa State"
  },
  {
    "event_id": "gst-TiQvhMs5oDUtU7Y",
    "name": "Lubba Naaman Chandari",
    "email": "lubbanaaman8@gmail.com",
    "Location": "Jimata, yola"
  },
  {
    "event_id": "gst-u1A4zlOWS23qQpx",
    "name": "bishop fred lucas",
    "email": "lucasbishopfred@gmail.com",
    "Location": "Jalingo"
  },
  {
    "event_id": "gst-ckwTtHHUxjkv6Di",
    "name": "Manasseh John",
    "email": "manassehjohnkwaji@gmail.com",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-MABUGAtHHw623dk",
    "name": "Maureen Danladi",
    "email": "maureendanladi92@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-eHZEEy8Kb7UJgAX",
    "name": "Mercy Maxwell Machill",
    "email": "mercymaxwell639@gmail.com",
    "Location": "Sangere, Futy"
  },
  {
    "event_id": "gst-cLPDL6YDlCDo7eY",
    "name": "Miracle Jolly Justin",
    "email": "miraclejustin89@gmail.com",
    "Location": "Yola south"
  },
  {
    "event_id": "gst-c2B4ek4Ps120aLh",
    "name": "Margret Mosamnaro Lubba",
    "email": "mlubba123@gmail.com",
    "Location": "Adamawa"
  },
  {
    "event_id": "gst-sZPultrRFTgXeNU",
    "name": "Ninsunforibih Nuhu Akila",
    "email": "ninsunakila@gmail.com",
    "Location": "Adamawa, Yola"
  },
  {
    "event_id": "gst-YDLSywoIoulS38J",
    "name": "Nubiya Haziel",
    "email": "nubiyayerima@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-jve6KbdDAGiPppH",
    "name": "PHILIP EUCHERIA JELANI",
    "email": "philipeucheria090@gmail.com",
    "Location": "Karewa"
  },
  {
    "event_id": "gst-mRtHsafAmeW2N7E",
    "name": "Philip Stephen",
    "email": "philipstephen202@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-KPstvJg9ylEe575",
    "name": "Augustine 6",
    "email": "preciousaugustine778@gmail.com",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-uao87WWoVvgr4Ff",
    "name": "Rabi Kabiru",
    "email": "rabikabirmamman@gmail.com",
    "Location": "Yola north"
  },
  {
    "event_id": "gst-pOFO66PxIVqerSQ",
    "name": "Rahila Haruna",
    "email": "rahilaharuna100@gmail.com",
    "Location": "Jimeta yola"
  },
  {
    "event_id": "gst-skDJgJaMYYtyF5B",
    "name": "Nathan Renos",
    "email": "renosnathan@gmail.com",
    "Location": "Taraba State"
  },
  {
    "event_id": "gst-yYoXzpMmre0nKNq",
    "name": "Chiwar Rhoda",
    "email": "rhodachiwar@gmail.com",
    "Location": "Jimeta/Yola"
  },
  {
    "event_id": "gst-hCtySkFFRIQUTk7",
    "name": "Rita Danladi Panya",
    "email": "ritadanladipanya@gmail.com",
    "Location": "Jambutu Jimeta yola"
  },
  {
    "event_id": "gst-vziogKQEv48xO3D",
    "name": "Sadiq Khamisu Abdullahi",
    "email": "sadiqkhamisu2020@gmail.com",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-gYf3zzFlFn2MHKY",
    "name": "Salihu Abdulrauf",
    "email": "salihuabdulrauf2@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-QVH4dGVuZbQPw8R",
    "name": "Samson Homogome",
    "email": "samsonhomogome2019@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-4cRE7muVudpn8Ht",
    "name": "Samuel Suleiman",
    "email": "samuelsuleiman24@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-MWu9k5dcgaqBfsj",
    "name": "Shamsudeen Mohammed isa",
    "email": "sasumha2021@gmail.com",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-3uQqeeVf20tn4xi",
    "name": "Stephanie Monday",
    "email": "stephaniemonday4@gmail.com",
    "Location": "Jimeta"
  },
  {
    "event_id": "gst-9Y35zy2GBi3sSs8",
    "name": "Esther Micloth",
    "email": "stermicks1404@gmail.com",
    "Location": "Yola"
  },
  {
    "event_id": "gst-daUBvBOVlFNfC22",
    "name": "Simon Francis",
    "email": "swabada12@gmail.com",
    "Location": "Girie"
  },
  {
    "event_id": "gst-30ZSNIKMxv0GNHr",
    "name": "John Sylvester",
    "email": "sylvesterj772@gmail.com",
    "Location": "Modibbo Adama university"
  },
  {
    "event_id": "gst-A7hsxNyE9I1S0Na",
    "name": "Shadrack Peter",
    "email": "taiyetaiye97@gmail.com",
    "Location": "Bachure"
  },
  {
    "event_id": "gst-zIii2aGbAoKgUEk",
    "name": "Tamnwi Changbuin",
    "email": "tamnwi2020@gmail.com",
    "Location": "Sangere futy"
  },
  {
    "event_id": "gst-gmLYGd0nUtD9vvB",
    "name": "Joshua Lucas Samuel",
    "email": "thetastehub001@gmail.com",
    "Location": "Kaduna state"
  },
  {
    "event_id": "gst-PYCFceQdY4ZJwNj",
    "name": "Ukwe Sabo",
    "email": "ukwesabo010@gmail.com",
    "Location": "Adamawa State"
  },
  {
    "event_id": "gst-Cht1DjcD4M2EPcQ",
    "name": "Usmalik David Alexander",
    "email": "usmalikalexander001@gmail.com",
    "Location": "Mautech"
  },
  {
    "event_id": "gst-bUBk4tkQBw8pL16",
    "name": "Sarah James Vandi",
    "email": "vandisarahjames3@gmail.com",
    "Location": "Sengere futy"
  },
  {
    "event_id": "gst-Mv4rJsMVrl3Yb8c",
    "name": "Version Meshack",
    "email": "versionmeshack8@gmail.com",
    "Location": "Taraba"
  },
  {
    "event_id": "gst-XnMO3XHI4ki2eVV",
    "name": "WISDOM LUSETER ATSANAN",
    "email": "wisdomluseter@gmail.com",
    "Location": "Bachure Jimeta Yola"
  },
  {
    "event_id": "gst-7SJyEs0gqBltqxQ",
    "name": "Yakubu Harrison",
    "email": "yakubuharrison@gmail.com",
    "Location": "Girei Local Government Area, Adamawa State"
  },
  {
    "event_id": "gst-dfXCERgMymJx3UI",
    "name": "Yaruta Amos",
    "email": "yarutabonnkeamos@gmail.com",
    "Location": "Yola"
  }
]
# print(f'total number of attendees: {len(attendees)}'.title())