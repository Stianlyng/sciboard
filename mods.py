from app import create_app,db
from datetime import date

from app.models import Access,User,Author,Catalog,TagCategory,Tags,CatalogHasTagCategory,TagCategoryHasTags,Document,DocumentHasMetadata,Thumbnail,DocumentHasTags,Comment,DocumentType
from configs.db.docData import *
from config import TestingConfig,ProductionConfig,DevelopmentConfig
from sqlalchemy import or_, func

class DatabaseRunner():
    def __init__(self,config_class):
        self.app = create_app(config_class)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def testQuery(self):
        query = db.session.query(
            TagCategory.idTagCategory,
            TagCategory.categoryName
        ).join(
            CatalogHasTagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
        ).filter(
            CatalogHasTagCategory.fk_idCatalog == 2
        ).all()

        print(query)
        self.app_context.pop()

    def create(self):
        db.create_all()
        self.app_context.pop()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def insertData(self):
        db.session.add_all([
            Access(accessType='Public'),
            Access(accessType='User'),
            Access(accessType='Admin'),

            User(username='Stian', email='diversebrukere@protonmail.no', first_name='Stian', last_name='Lyng', password_hash=stdPwd),
            User(username='Haakon', email='test2@yo.no', first_name='Haakon', last_name='Beckhham', password_hash=stdPwd),
            User(username='Tiger', email='test3@yo.no', first_name='Tiger', last_name='Woods', password_hash=stdPwd),
            User(username='Elon', email='test4@yo.no', first_name='Elon', last_name='Musk', password_hash=stdPwd),
            User(username='Richard', email='test5@yo.no', first_name='Richard', last_name='Brandson', password_hash=stdPwd),
            User(username='Jeff', email='stian.sls@gmail.com', first_name='Jeff', last_name='Bezos', password_hash=stdPwd),


            Thumbnail(size='432826', mimetype='image/png', filename='stian.png',image=thumb1, fk_idUser=1),
            Thumbnail(size='686762', mimetype='image/png', filename='haakon.png',image=thumb2, fk_idUser=2),
            Thumbnail(size='708838', mimetype='image/png', filename='tiger.png',image=thumb3, fk_idUser=3),
            Thumbnail(size='784936', mimetype='image/png', filename='musk.png',image=thumb4, fk_idUser=4),
            Thumbnail(size='1193580', mimetype='image/png', filename='richard.png',image=thumb5, fk_idUser=5),
            Thumbnail(size='452140', mimetype='image/png', filename='jeff.png',image=thumb6, fk_idUser=6),

            Author(lastname='Lyng', firstname='Stian'),
            Author(lastname='Sandven', firstname='Haakon'),
            Author(lastname='Beckham', firstname='David'),
            Author(lastname='Woods', firstname='Tiger'),
            Author(lastname='Musk', firstname='Elon'),
            Author(lastname='Brandson', firstname='Richard'),

            Catalog(catalogName='Humanities and Arts'),
            Catalog(catalogName='Social Sciences and Law'),
            Catalog(catalogName='Business and Administration'),
            Catalog(catalogName='Engineering and Techinal Studies'),
            Catalog(catalogName='Health, Welfare and Sports'),
            Catalog(catalogName='Primary Industries'),
            Catalog(catalogName='hdsjhgadjshgjhasd'),

            DocumentType(docType='Master Thesis'),
            DocumentType(docType='Bachelor Thesis'),
            DocumentType(docType='Doctoral Thesis'),
            DocumentType(docType='Journal Article'),
            DocumentType(docType='Peer Reviewed'),
            DocumentType(docType='Research Report'),
            DocumentType(docType='Student Paper'),
            DocumentType(docType='Working Paper'),


            TagCategory(categoryName='English'),
            TagCategory(categoryName='English Literature'),
            TagCategory(categoryName='Fine Art'),
            TagCategory(categoryName='Norwegian Language and Society'),
            TagCategory(categoryName='Theoretical Linguistics'),
            TagCategory(categoryName='Environmental Law'),
            TagCategory(categoryName='Governance and Entrepreneurship'),
            TagCategory(categoryName='Indigenous Studies'),
            TagCategory(categoryName='Law of the Sea'),
            TagCategory(categoryName='Master of Philosophy'),
            TagCategory(categoryName='Nordic Urban Planning'),
            TagCategory(categoryName='Northern Studies'),
            TagCategory(categoryName='Ocean Leadership'),
            TagCategory(categoryName='Peace and Conflict Transformation'),
            TagCategory(categoryName='Arctic Adventure Tourism'),
            TagCategory(categoryName='Tourism Studies'),
            TagCategory(categoryName='Aerospace Control Engineering'),
            TagCategory(categoryName='Applied Computer Science'),
            TagCategory(categoryName='Biology'),
            TagCategory(categoryName='Biomedicine'),
            TagCategory(categoryName='Computer Science'),
            TagCategory(categoryName='Electrical Engineering'),
            TagCategory(categoryName='Engineering Design'),
            TagCategory(categoryName='Geology'),
            TagCategory(categoryName='Arctic Nature Guide'),
            TagCategory(categoryName='Biomedicine'),
            TagCategory(categoryName='Public Health'),
            TagCategory(categoryName='Biology'),

            Tags(tagName='Multilingualism'),
            Tags(tagName='Psycholinguistics'),
            Tags(tagName='Neurocognition'),
            Tags(tagName='Syntax'),
            Tags(tagName='Phonology'),
            Tags(tagName='post-colonial'),
            Tags(tagName='romanticism'),
            Tags(tagName='modernism'),
            Tags(tagName='contemporary'),
            Tags(tagName='literature'),
            Tags(tagName='art'),
            Tags(tagName='exhibitions'),
            Tags(tagName='expressions'),
            Tags(tagName='presentation'),
            Tags(tagName='civilization'),
            Tags(tagName='history'),
            Tags(tagName='literature'),
            Tags(tagName='Culture'),
            Tags(tagName='phonology'),
            Tags(tagName='syntax'),
            Tags(tagName='language-acquisition'),
            Tags(tagName='philosophy'),

            CatalogHasTagCategory(fk_idCatalog=1, fk_idTagCategory=1),
            CatalogHasTagCategory(fk_idCatalog=1, fk_idTagCategory=2),
            CatalogHasTagCategory(fk_idCatalog=1, fk_idTagCategory=3),
            CatalogHasTagCategory(fk_idCatalog=1, fk_idTagCategory=4),
            CatalogHasTagCategory(fk_idCatalog=1, fk_idTagCategory=5),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=6),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=7),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=8),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=9),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=10),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=11),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=12),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=13),
            CatalogHasTagCategory(fk_idCatalog=2, fk_idTagCategory=14),
            CatalogHasTagCategory(fk_idCatalog=3, fk_idTagCategory=15),
            CatalogHasTagCategory(fk_idCatalog=3, fk_idTagCategory=16),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=17),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=18),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=19),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=20),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=21),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=22),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=23),
            CatalogHasTagCategory(fk_idCatalog=4, fk_idTagCategory=24),
            CatalogHasTagCategory(fk_idCatalog=5, fk_idTagCategory=25),
            CatalogHasTagCategory(fk_idCatalog=5, fk_idTagCategory=26),
            CatalogHasTagCategory(fk_idCatalog=5, fk_idTagCategory=27),
            CatalogHasTagCategory(fk_idCatalog=6, fk_idTagCategory=28),

            TagCategoryHasTags(fk_idTagCategory=1, fk_idTags=1),
            TagCategoryHasTags(fk_idTagCategory=1, fk_idTags=2),
            TagCategoryHasTags(fk_idTagCategory=1, fk_idTags=3),
            TagCategoryHasTags(fk_idTagCategory=1, fk_idTags=4),
            TagCategoryHasTags(fk_idTagCategory=1, fk_idTags=5),
            TagCategoryHasTags(fk_idTagCategory=2, fk_idTags=6),
            TagCategoryHasTags(fk_idTagCategory=2, fk_idTags=7),
            TagCategoryHasTags(fk_idTagCategory=2, fk_idTags=8),
            TagCategoryHasTags(fk_idTagCategory=2, fk_idTags=9),
            TagCategoryHasTags(fk_idTagCategory=2, fk_idTags=10),
            TagCategoryHasTags(fk_idTagCategory=3, fk_idTags=11),
            TagCategoryHasTags(fk_idTagCategory=3, fk_idTags=12),
            TagCategoryHasTags(fk_idTagCategory=3, fk_idTags=13),
            TagCategoryHasTags(fk_idTagCategory=3, fk_idTags=14),
            TagCategoryHasTags(fk_idTagCategory=4, fk_idTags=15),
            TagCategoryHasTags(fk_idTagCategory=4, fk_idTags=16),
            TagCategoryHasTags(fk_idTagCategory=4, fk_idTags=17),
            TagCategoryHasTags(fk_idTagCategory=4, fk_idTags=18),
            TagCategoryHasTags(fk_idTagCategory=5, fk_idTags=19),
            TagCategoryHasTags(fk_idTagCategory=5, fk_idTags=20),
            TagCategoryHasTags(fk_idTagCategory=5, fk_idTags=21),
            TagCategoryHasTags(fk_idTagCategory=5, fk_idTags=22),

            Document(size='456604', mimetype='application/pdf', filename='no.ntnu_inspera_81689313_82837975.pdf',document=doc1),
            Document(size='2485650', mimetype='application/pdf', filename='18967_FULLTEXT.pdf', document=doc2),
            Document(size='7376648', mimetype='application/pdf', filename='no.ntnu_inspera_56692029_57168904.pdf',document=doc3),
            Document(size='6823227', mimetype='application/pdf', filename='no.ntnu_inspera_56803644_22271503.pdf',document=doc4),
            Document(size='2111787', mimetype='application/pdf', filename='17656_FULLTEXT.pdf', document=doc5),
            Document(size='5232735', mimetype='application/pdf', filename='18336_FULLTEXT.pdf', document=doc6),

            DocumentHasMetadata(title=tit1, description=desc1, creationDate=date.today(), fk_idDokument=1, fk_idUser=1,
                                fk_idCatalog=1, fk_idAccess=1,fk_idDocumentType=1),
            DocumentHasMetadata(title=tit2, description=desc2, creationDate=date.today(), fk_idDokument=2, fk_idUser=2,
                                fk_idCatalog=1, fk_idAccess=1,fk_idDocumentType=2),
            DocumentHasMetadata(title=tit3, description=desc3, creationDate=date.today(), fk_idDokument=3, fk_idUser=3,
                                fk_idCatalog=1, fk_idAccess=1,fk_idDocumentType=1),
            DocumentHasMetadata(title=tit4, description=desc4, creationDate=date.today(), fk_idDokument=4, fk_idUser=4,
                                fk_idCatalog=1, fk_idAccess=1,fk_idDocumentType=2),
            DocumentHasMetadata(title=tit5, description=desc5, creationDate=date.today(), fk_idDokument=5, fk_idUser=5,
                                fk_idCatalog=1, fk_idAccess=1,fk_idDocumentType=1),
            DocumentHasMetadata(title=tit6, description=desc6, creationDate=date.today(), fk_idDokument=6, fk_idUser=6,
                                fk_idCatalog=1, fk_idAccess=1,fk_idDocumentType=1),


            Comment(comment="This is the first comment, on document 1,and its great to write such a nice comment for u peeps",fk_idUser=1, fk_idDokument=1),
            Comment(comment="This is the second comment, on document 1,and its great to write such a nice comment for u peeps",fk_idUser=2, fk_idDokument=1)
        ])
        db.session.commit()
        self.app_context.pop()


def databaseSetup(activeConfig, run=False, test=False):
    if run is True:
        dropDB = DatabaseRunner(activeConfig)
        dropDB.tearDown()

        createDB = DatabaseRunner(activeConfig)
        createDB.create()

        insertDB = DatabaseRunner(activeConfig)
        insertDB.insertData()
    if test is True:
        testDB = DatabaseRunner(activeConfig)
        testDB.testQuery()

databaseSetup(TestingConfig, run=True, test=False)



