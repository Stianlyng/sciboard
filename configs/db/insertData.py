from flask_sqlalchemy import SQLAlchemy
from app import create_app,db
from datetime import date
from app import models as m
from configs.db.docData  import tit1,tit2,tit3,tit4,tit5,tit6,desc1,desc2,desc3,desc4,desc5,desc6,doc1,doc2,doc3,doc4,doc5,doc6

####################################
#         Fetchall tables         #
####################################

def addToAccess():
    objects = [
        'Public',
        'User',
        'Admin'
    ]

    for i in objects:
        item = m.Access(accessType=i)
        db.session.add(item)
    db.session.commit()

def addToUser():
    objects = [
        ['Stian', 'stian@yoyo.com','Stian','Lyng', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
        ['Haakon', 'haakon@yoyo.com','Stian','Sandven', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
        ['David', 'david@yoyo.com','David','Beckhham', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
        ['Tiger', 'tiger@yoyo.com','Tiger','Woods', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
        ['Elon', 'musk@yoyo.com','Elon','Musk', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
        ['Richard', 'rich@yoyo.com','Richard','Brandson', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
        ['Bezoz', 'jeff@yoyo.com','Jeff','Bezos', 'pbkdf2:sha256:260000$ufeCneSL7gRGeGGI$b70fa9915068ada3d0b2cfb66cf911538a0840908fac3729e9812980785cd386'],
    ]

    for i in objects:
        item = m.User(username=i[0],email=i[1],first_name=i[2],last_name=i[3], password_hash=i[4])
        db.session.add(item)
    db.session.commit()

def addToAuthor():
    objects = [
        ['Lyng', 'Stian'],
        ['Sandven', 'Haakon'],
        ['Beckham', 'David'],
        ['Woods', 'Tiger'],
        ['Musk', 'Elon'],
        ['Brandson', 'Richard'],
        ['Jeff', 'Bezoz'],
    ]

    for i in objects:
        item = m.Author(lastname=i[0],firstname=i[1])
        db.session.add(item)
    db.session.commit()

def addToCatalog():
    objects = [
        'Humanities and Arts',
        'Social Sciences and Law',
        'Business and Administration',
        'Engineering and Techinal Studies',
        'Health, Welfare and Sports',
        'Primary Industries',
    ]
    for i in objects:
        item = m.Catalog(catalogName=i)
        db.session.add(item)

    db.session.commit()


def addToTagCategory():
    objects = [
        'English',
        'English Literature',
        'Fine Art',
        'Norwegian Language and Society',
        'Theoretical Linguistics',
        'Environmental Law',
        'Governance and Entrepreneurship',
        'Indigenous Studies',
        'Law of the Sea',
        'Master of Philosophy',
        'Nordic Urban Planning',
        'Northern Studies',
        'Ocean Leadership',
        'Peace and Conflict Transformation',
        'Arctic Adventure Tourism',
        'Tourism Studies',
        'Aerospace Control Engineering',
        'Applied Computer Science',
        'Biology',
        'Biomedicine',
        'Computer Science',
        'Electrical Engineering',
        'Engineering Design',
        'Geology',
        'Arctic Nature Guide',
        'Biomedicine',
        'Public Health',
        'Biology'
    ]

    for i in objects:
        item = m.TagCategory(categoryName=i)
        db.session.add(item)

    db.session.commit()


def addToTags():
    objects = [
        'Multilingualism',
        'Psycholinguistics',
        'Neurocognition',
        'Syntax',
        'Phonology',
        'post-colonial',
        'romanticism',
        'modernism',
        'contemporary',
        'literature',
        'art',
        'exhibitions',
        'expressions',
        'presentation',
        'civilization',
        'history',
        'literature',
        'Culture',
        'phonology',
        'syntax',
        'language-acquisition',
        'philosophy',
    ]

    for i in objects:
        item = m.Tags(tagName=i)
        db.session.add(item)
    db.session.commit()


def addToCatalogHasTagCategory():
    objects = [
        [1, 1],
        [1, 2],
        [1, 3],
        [1, 4],
        [1, 5],
        [2, 6],
        [2, 7],
        [2, 8],
        [2, 9],
        [2, 10],
        [2, 11],
        [2, 12],
        [2, 13],
        [2, 14],
        [3, 15],
        [3, 16],
        [4, 17],
        [4, 18],
        [4, 19],
        [4, 20],
        [4, 21],
        [4, 22],
        [4, 23],
        [4, 24],
        [5, 25],
        [5, 26],
        [5, 27],
        [6, 28]
    ]

    for i in objects:
        #print(f"idcat: {i[0]}, idtagCat: {i[1]}")
        item = m.CatalogHasTagCategory(fk_idCatalog=i[0], fk_idTagCategory=i[1])
        db.session.add(item)
    db.session.commit()

def addToTagCategoryHasTags():
    objects = [
        [1, 1],
        [1, 2],
        [1, 3],
        [1, 4],
        [1, 5],
        [2, 6],
        [2, 7],
        [2, 8],
        [2, 9],
        [2, 10],
        [3, 11],
        [3, 12],
        [3, 13],
        [3, 14],
        [4, 15],
        [4, 16],
        [4, 17],
        [4, 18],
        [5, 19],
        [5, 20],
        [5, 21],
        [5, 22]
    ]

    for i in objects:
        #print(f"idcat: {i[0]}, idtagCat: {i[1]}")
        item = m.TagCategoryHasTags(fk_idTagCategory=i[0], fk_idTags=i[1])
        db.session.add(item)
    db.session.commit()



def addToDocument():

    objects = [
        ['456604',	'application/pdf',	'no.ntnu_inspera_81689313_82837975.pdf',doc1],
        ['2485650',	'application/pdf',	'18967_FULLTEXT.pdf', doc2],
        ['7376648',	'application/pdf',	'no.ntnu_inspera_56692029_57168904.pdf', doc3],
        ['6823227',	'application/pdf',	'no.ntnu_inspera_56803644_22271503.pdf', doc4],
        ['2111787',	'application/pdf',	'17656_FULLTEXT.pdf',doc5],
        ['5232735',	'application/pdf',	'18336_FULLTEXT.pdf', doc6]
    ]

    for i in objects:
        item = m.Document(size=i[0], mimetype=i[1], filename=i[2], document=i[3])
        db.session.add(item)
    db.session.commit()


def addToDocumentHasMeta():

    objects = [
        [tit1, desc1, '2022-01-01', 1, 1, 1, 1],
        [tit2, desc2, '2022-01-01', 2, 1, 1, 1],
        [tit3, desc3, '2022-01-01', 3, 1, 1, 1],
        [tit4, desc4, '2022-01-01', 4, 1, 1, 1],
        [tit5, desc5, '2022-01-01', 5, 1, 1, 1],
        [tit6, desc6, '2022-01-01', 6, 1, 1, 1],
    ]

    for i in objects:
        item = m.DocumentHasMetadata(title=i[0], description=i[1], creationDate=date.today(),fk_idDokument=i[3],fk_idUser=i[4],fk_idCatalog=i[5],fk_idAccess=i[6])
        db.session.add(item)
    db.session.commit()


