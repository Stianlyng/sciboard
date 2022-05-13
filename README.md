# Prosjektrapport SciBoard
## Innholdsfortegnelse
- Praktisk informasjon
	- Gruppenummer
	- Gruppedeltakere
	- URL Nettside
	- Tilganger og innlogging
		- ADMIN
		- VANLIG BRUKER
- Løsningsbeskrivelse
	- Databasebeskrivelse
		- Bruker og tilgang
		- Dokument katalog og tags
		- Kommentarer
		- Normalisering
	- Teknologivalg
		- Flask
		- Flask-SQLAlchemy
		- Flask-WTF
		- Flask-Mail
		- PyJWT
		- Tailwind CSS
		- Alpine JS
		- HTMX
	- Blueprints
		- API
		- Andre Blueprints
		- Statistiske filer og templates
	- SQL
- Prosjektdagbok
- Egne vurderinger


# Praktisk informasjon

#### Gruppenummer
- Canvas: Gruppe 3
- Github: Prosjektgruppe 39
#### Gruppedeltakere
- Stian Lyng Stræte
- Haakon Christopher Sandven
#### URL Nettside
- http://www.sciboard.onrender.com
#### Tilganger og innlogging
##### ADMIN
- Brukernavn: admin
- Passord: qwertyuiop
##### VANLIG BRUKER
- Brukernavn: bruker
- Passord: qwertyuiop

# Løsningsbeskrivelse

Løsningen vi har laget er et Content Management System (CMS) for formidling av forskningsartikler. Ved hjelp av løsningen vi har laget kan forskeren laste opp forskningsdokumenter, for eksempel bacheloroppgaver, masteroppgaver, Phd-Bloppgaver eller annen forskning til vår database. Forskeren bestemmer om forskningsrapporten skal være tilgjengelig for alle, eller kun innloggede brukere.

Løsningen er videre tilgjengelig for alle som ønsker å besøke den. Man kan registrere seg som bruker. Dette åpner for at man får tilgang til flere forskningsrapporter, i tillegg til at man kan laste opp sine egne. Brukere kan legge igjen kommentarer til en forskningsrapport.

  

## Databasebeskrivelse

Figuren under viser databasemodellen som er lagt til grunn i prosjektet. De ulike tabellene og sammenhengende beskrives under.

  

![](https://lh5.googleusercontent.com/idW1QivaBMucIZB3f5FPhjQ-H0RK4g0FO9mOp0O7NmNRwSoBZB2nc1VNPxmnts-hpkC1zng19DFuCcOm6e41MSfLm4IcMC527ZUCBQjnmTZ2QeHpF0px0Oc1meZc0fqcf_H6qDGOmS4WUiN8bA)

  

### Bruker og tilgang

Når brukere registrerer seg blir de lagt inn i tabellen User. Her genereres en bruker-ID, bruker legger inn informasjon om seg selv, passord lagres ved bruk av hash. Brukeren tildeles en token som brukes i forbindelse med verifisering av kontoen.

  

### Dokument, katalog og tags

Forskningsdokumentene lagres i BLOB-format i tabellen Document. Det er kun registrerte brukere som kan laste opp dokumenter, men ettersom det kan være medforfattere som ikke er registrert som bruker støtter løsningen at man kan legge inn disse. Disse blir lagret i tabellen Authors. 


Ettersom et dokument kan ha flere forfattere, og en forfatter kan publisere flere dokumenter er det laget en mange-til-mange-tabell DocumentHasAuthor for å håndtere dette. Hvert dokument inneholder også metadata lagret i tabellen DocumentHasMetadata, som legges inn når forfatteren laster opp dokumentet. Metadata er blant annet tittel på dokumentet, en beskrivelse, dato for opplasting og dokumentdato. I denne tabellen lagres også antall treff, antall kommentarer og antall likes. Denne tabellen knytter også sammen dokumentet med bruker, katalog og aksess. 

  

Hvert dokument lagres i en katalog. Katalogene er predefinert i tabellen Catalog. Videre kan det defineres en eller flere tags til hvert dokument. Tagsene er lagret i tabellen Tags. Ettersom en Tag kan knyttes til flere dokumenter, og et dokument kan ha flere tags er det opprettet en mange-til-mange tabell kalt DocumentHasTags. Tagsene er også knyttet til en Tag-kategori. Ettersom en tag kan tilhøre flere tag-kategorier og en tag-kategori kan ha flere tags knyttet til seg er mange-til-mange-tabellen TagCategoryHasTags opprettet. Vi har videre valgt å knytte Tag-kategori mot katalog-tabellen. Også her vil en Tag-kategori kunne være knyttet til flere kataloger og motsatt, så igjen er det brukt en mange-til-mange-tabell kalt CatalogHasTagCategory.

  

### Kommentarer

Registrerte brukere kan legge igjen kommentarer på de ulike forskningsrapportene. Kommentarer lagres i databasen Comment. Kommentarene er knyttet til et bestemt dokument og til en bestemt bruker. Ettersom man også kan kommentere en annens kommentar (kommentar til kommentar) vil idComment også fungere som en fremmednøkkel for å sikre oversikt over dette. Slettede kommentarer lagres i databasen DeletedComment.

### Normalisering

Databasen er normalisert i henhold til BCNF.


## Teknologivalg

Det ble bruk flere packages under utviklingen, men vi velger å legge spesielt fokus på de som er nevnt i dette delkapitlet.

### Flask

Flask er en Python-modul, som skaper et mikrorammeverk som åpner for å utvikle web-applikasjoner. Flask har en liten kjerne som enkelt lar seg skalere til større bruksområder. Dette sett i sammenheng med pensum i faget gjorde at valget ble enkelt. 

Flask er avhengig av Jinja template engine, og Wekzeug WSGI toolkit. Førstnevnte muliggjør for  “sandboxed execution” av html-templates, som gjør at man har full kontroll over alle templates som kjøres. Jinja inkluderer også automatisk HTML escaping, noe som reduserer sannsynligheten for XSS angrep. Alle templates i prosjektet returneres enten via render_template(), eller render_template_string(). Sistnevnte hadde tidligere ikke html escaping, men fikk dette implementert ved forrige oppdatering.

### Flask-SQLAlchemy

Som nevnt er Flask et mikro-rammeverk. Dette betyr at man ikke får en ORM med i Flask. Selv om selve ORM delen av SQLAlchemy ikke ble brukt i denne oppgaven er planen å implementere dette senere. 


Siden vi jobbet på hver vår kant og hadde planer om å fortsette med applikasjonen, var sømløshet mot andre teknologier og databaser viktig. Her gir SQLAlchemy oss noen viktige fordeler:

-   Lar oss definere database modellene i applkasjonskoden
	```python
	class User(UserMixin, db.Model):  
	    __tablename__ = 'User'  
	  
	    id = db.Column(db.Integer, primary_key=True)  
	    username = db.Column(db.String(64), index=True, unique=True)  
	    email = db.Column(db.String(120), index=True, unique=True)  
	    password_hash = db.Column(db.String(128))  
	    about_me = db.Column(db.String(140))  
	    first_name = db.Column(db.String(40),nullable=False)  
	    last_name = db.Column(db.String(40),nullable=False)  
	    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  
	    vertified = db.Column(db.Boolean, unique=False, default=False)  
	  
	  
	    def __repr__(self):  
	        return '<User {}>'.format(self.username)  
	  
	    def set_password(self, password):  
	        self.password_hash = generate_password_hash(password)  
	  
	    def check_password(self, password):  
	        return check_password_hash(self.password_hash, password)
	```

  

-   Muligheter for å oppdatere, gjøre endringer og kjøre backup av database via CLI
    
-   Pythonstil på koden gjør det oversiktlig, og sørger for en sammenheng og klar kontekst å jobbe under.
    
-   Konstruksjon av queries gjøres enkelt og med liten kode uavhengig av hvor man er i kodebasen. 
	```python
	catalogs = Catalog.query.all()
	```
    
-   Støtter flere databaser samtidig. Vi bruker SQlite i utviklingen og MariaDB via Google Cloud i produksjon. Dette ga oss muligheten til å teste kode og nye oppsett mye raskere. 
    
-   Har sikkerhet i fokus, med flere løsninger som hindrer de kjente sårbarhetene man ellers møter ved bruk av databaser
    

  

### Flask-WTF

Flask-WTF er en versjon av WTforms som er laget med fokus på integrasjon med Flask. WTform gjør det meste av jobben når det kommer til validering av forms via implementert CSRF beskyttelse i hvert enkelt form som blir lastet på siden. Siden WTF også er kombinert med Jinja, får man enkelt strukturert forms via blueprints i backend, for enklere håndtering. 

### Flask-Mail

Vi brukte Flask-mail for å konfigurere SMTP med applikasjonen. Som SMTP Tjener brukte vi gmail. 


```python
MAIL_SERVER = 'smtp.gmail.com'  
MAIL_PORT = 587  
MAIL_USE_TLS = 1  
MAIL_USERNAME = 'sciboard.org@gmail.com'  
MAIL_PASSWORD = 'Activate Commend7 Slip'  
ADMINS = ['sciboard.org@gmail.com']
```

### PyJWT

Prosjektbeskrivelsen etterlyste e-postvalidering ved opprettelse av ny bruker. Vi valgte å gå for en token løsning, der logikken i backend verifiserer gyldigheten ved input tilbake til applikasjonen. 

  

For å skape en token vil sendes bruker ID og “secret key” fra configfilen inn i denne funksjonen:

```python
def createToken(user_id,secret):  
    # Create an expirationdate  
    today = datetime.utcnow()  
    days = timedelta(days=2)  
    expirationDate = today + days  
    return jwt.encode({'user': user_id, 'expires': str(expirationDate)},secret, algorithm='HS256')
```

  

Funksjonen skaper en en dict der man har en bruker og et datetime objekt som er flyttet 2 dager frem i tid. Når da denne krypterte strengen kommer tilbake i url fra mailen til brukeren. Vil denne funksjonen decode strengen via denne funksjonen:


```python
def checkToken(token,secret):  
    # Create an expirationdate  
    today = datetime.utcnow()  
    # DEcode  
    token = jwt.decode(token, secret, algorithms=["HS256"])  
  
    if token["expires"] < str(today):  
        return False  
    else:  
        return token["user"]
```
  

Dersom datetime objektet ikke er større en datetime.now() vil funksjonen returnere bruker ID. Disse funksjonene brukes både til validering av ny bruker og glemt passord. I blueprint routen til user, vil ved validering User.validated gå fra False til True.

### Tailwind CSS

For styling begynte vi med Bootstrap, men gikk fort over til Tailwind da dette ga et større handlingsrom til å modifisere etter behov. Tailwind er på mange måter relativt likt Bootstrap, men har et større spekter av klasser og har også en god løsning for minimering av CSS script.

### Alpine JS

Det kan fort bli et stort behov for javascript i dagens web applikasjoner. Selv om javascript gir store muligheter for modifisering gir det også store muligheter for sårbarheter, tregere side og bugs. Vi valgte å gå for Alpine JS, fordi at det gir et lettvektig rammeverk for å lage inline logikk i HTML-koden. I tillegg til at Alpine er veldig lettvektig (21.9kB) er det også enkelt å bruke opp mot Tailwind CSS

### HTMX 

HTMX ga oss tilgang til AJAX, CSS Transitions, WebSockets og server sendte events direkte i HTML koden ved bruk av attributes. I HTML sin spede begynnelse var dette standarden, men ble etterhvert byttet ut med JavaScript og sendingen av events ble gjort i JSON. HTMX er laget av skaperen til Typescript, og har fått mye oppmerksomhet av webutviklere etter det ble lansert for et års tid siden. Vi vil forklare bruken av htmx i større detalj i API delen senere.

  

## Blueprints

Som følge av applikasjonenes muligheter for skalering og utvidelser bestemte vi oss tidlig for å tilrettelegge for en modulbasert tilnærming. Et annet viktig element i startfasen av prosjektet var at vi skulle legge til rette for å møte oppgavens krav fra starten av, og heller utvide funksjonaliteten dersom det ble tid til det. Ved å bruke blueprint fikk vi møtt mange av disse forutsetningene. 

  

Blueprints ble nyttige for oss i disse tilfellene:

-   Vi fikk separert kodebasen, 
    
-   Mindre kompleksitet
    
-   Større funksjonalitet
    
-   Tilgang til objekter via parameter i URL prefix eller subdomene
    

  

### API

Som nevnt tidligere valgte vi å gå for HTMX for å utføre klient/server HTTP requests på siden. I den sammenheng at vi ønsket å minimere kompleksiteten, og skape en dynamisk side der brukeren selv kan styre applikasjonens handlinger, var det nødvendig med en oversiktlig måte å kjøre API-calls til serveren. # SJEKK TERMINOLOGI HER

  

API blueprinten er strukturert med en __init__ fil, som igjen importerer de ulike objektene som er tilgjengelig. Mappestrukturen vil da se slik ut:

  

![](https://lh5.googleusercontent.com/0FgsPR9bxmd1DswaxOp-vQv2g9wqoPVzd4m804VlG40vL5XR9LUaWWY9Uy4pLFniFIEA_LHk_JrKibS_UzkFjuEHS1V8555YN2WT1-i4HzVeHoPbqsHreJgJNSarMRvnyDeUpsLCbB0sTHtl4w)

  

Det er også lagt inn en prefiks (/api) på alle “routes” i API blueprinten, noe som gjør at om disse skulle være tilgjengelig via URL, så må /api legges før de eventuelle URL’ene.

  

Et eksempel på bruken av et slikt objekt vil være innhentingen av “topp-brukere” på siden:


```python
@bp.route('/top-users/<int:count>', methods=['GET'])  
def getTopUsers(count) -> int:  
    # Get sum of views pr user  
    top_users = db.session.query(  
            func.sum(DocumentHasMetadata.views),  
            DocumentHasMetadata.fk_idUser,  
            User.first_name,  
            User.last_name,  
            User.username  
        ).join(  
            User, User.id == DocumentHasMetadata.fk_idUser  
        ).group_by(  
            DocumentHasMetadata.fk_idUser  
        ).limit(  
            count  
        ).all()  
  
    templ = """  
            {% for user in top_users %}            {% include 'components/top-user.html' %}            {% endfor %}            """    return render_template_string(templ,top_users=top_users)
```

  

Ved aktivering av linken api/top-users/<COUNT>, vil man kunne injisere html koden man ser i templ-variablen. I <count> delen av url kan man legge til et hvilket som helst tall for å bestemme hvor mange rader med brukere man ønsker å hente ut.

  

I Flask vil det være hensiktsmessig å bruke {{ url_from(api.getTopUsers) }} for å forhindre feilene som kan oppstå ved å endre root URL eller andre linker. 

  

Logikken for å aktivere og videre injisere brukerne inn i HTML-koden hos klienten, gjøres slik i HTML-koden:


```html
<div hx-get="{{ url_for('api.getTopUsers', count=5 )}}" hx-trigger="load" class="font-medium text-gray-900">  
  <!-- users get injected here -->  
</div>
```

## Andre Blueprints

De andre blueprintene 

### ![](https://lh6.googleusercontent.com/8FgGksalA2XtENETqCZk9TTyWjXk0evEoY3fj3j6ZY8kv1ruLsIMWlTHXz-D_Jh6RW93Kzn_ZlLiT8l16hLOmOLhZ0AHyINQgN3BVdZKE4eosZ2VOtqJNAjmjRmD9aJZ9dPo8WvY3YeEN9KYmQ)

Alle disse mappene følger lik struktur, med et __init__.py script som initierer mappen, og ved det endrer mappen til en Python Package Module. Her skal man kunne fjerne eller legge til en modul, uten at dette skulle ha noen innvirkning på resten av kodebasen. Dette fungerer som lukkede sandboxer, som skaper en oversiktlig og mindre kompleks kodebase å jobbe med. 

  

## Statistiske filer og templates

Disse mappene har vi valg å legge utenom blueprints da vi ikke så behovet for å å ulike stylesheets eller templates på de forskjellige modulene. Om vi derimot skulle utvide med en blogg eller lignende, kan man enkelt lage en egen statisk, eller templates mappe ved i å legge den inn i  blueprint statement i create_app (application factory) i main skriptet. 

  

# SQL
Som nevnt brukte vi SQLAlchemy sin funksjonalitet for å generere tabeller, vi har uansett valgt å legge ved en forward enigineeret versjon slik at man kan lese dette i raw SQL. 

Modellen for generering av scriptet finner man i kildekoden, med navnet models.py


```sql
CREATE TABLE Access ( 

    idAccess             INTEGER NOT NULL  PRIMARY KEY  ,

    accessType           VARCHAR(45) NOT NULL    

 );

  

CREATE TABLE Author ( 

    idAuthor             INTEGER NOT NULL  PRIMARY KEY  ,

    lastname             VARCHAR(80) NOT NULL    ,

    firstname            VARCHAR(80) NOT NULL    

 );

  

CREATE TABLE Catalog ( 

    idCatalog            INTEGER NOT NULL  PRIMARY KEY  ,

    catalogName          VARCHAR(80) NOT NULL    ,

    fk_idAccess          INTEGER     ,

    FOREIGN KEY ( fk_idAccess ) REFERENCES Access( idAccess )  

 );

  

CREATE TABLE Document ( 

    idDocument           INTEGER NOT NULL  PRIMARY KEY  ,

    size                 VARCHAR(10) NOT NULL    ,

    mimetype             VARCHAR(50) NOT NULL    ,

    filename             VARCHAR(250) NOT NULL    ,

    document             BLOB     

 );

  

CREATE TABLE DocumentHasAuthor ( 

    fk_idDokument        INTEGER NOT NULL    ,

    fk_idAuthor          INTEGER NOT NULL    ,

    CONSTRAINT pk_DocumentHasAuthor PRIMARY KEY ( fk_idDokument, fk_idAuthor ),

    FOREIGN KEY ( fk_idDokument ) REFERENCES Document( idDocument )  ,

    FOREIGN KEY ( fk_idAuthor ) REFERENCES Author( idAuthor )  

 );

  

CREATE TABLE DocumentHasViews ( 

    fk_idDokument        INTEGER NOT NULL  PRIMARY KEY  ,

    views                INTEGER     ,

    FOREIGN KEY ( fk_idDokument ) REFERENCES Document( idDocument )  

 );

  

CREATE TABLE DocumentType ( 

    idType               INTEGER NOT NULL  PRIMARY KEY  ,

    docType              VARCHAR(45) NOT NULL    

 );

  

CREATE TABLE TagCategory ( 

    idTagCategory        INTEGER NOT NULL  PRIMARY KEY  ,

    categoryName         VARCHAR(50) NOT NULL    

 );

  

CREATE TABLE Tags ( 

    idTags               INTEGER NOT NULL  PRIMARY KEY  ,

    tagName              VARCHAR(50) NOT NULL    

 );

  

CREATE TABLE User ( 

    id                   INTEGER NOT NULL  PRIMARY KEY  ,

    username             VARCHAR(64)     ,

    email                VARCHAR(120)     ,

    password_hash        VARCHAR(128)     ,

    about_me             VARCHAR(140)     ,

    first_name           VARCHAR(40) NOT NULL    ,

    last_name            VARCHAR(40) NOT NULL    ,

    last_seen            DATETIME     ,

    vertified            BOOLEAN     

 );

  

CREATE TABLE alembic_version ( 

    version_num          VARCHAR(32) NOT NULL  PRIMARY KEY  

 );

  

CREATE TABLE CatalogHasTagCategory ( 

    fk_idCatalog         INTEGER NOT NULL    ,

    fk_idTagCategory     INTEGER NOT NULL    ,

    CONSTRAINT pk_CatalogHasTagCategory PRIMARY KEY ( fk_idCatalog, fk_idTagCategory ),

    FOREIGN KEY ( fk_idCatalog ) REFERENCES Catalog( idCatalog )  ,

    FOREIGN KEY ( fk_idTagCategory ) REFERENCES TagCategory( idTagCategory )  

 );

  

CREATE TABLE Comment ( 

    idComment            INTEGER NOT NULL  PRIMARY KEY  ,

    date                 DATETIME     ,

    comment              TEXT(500) NOT NULL    ,

    fk_idUser            INTEGER NOT NULL    ,

    fk_idDokument        INTEGER NOT NULL    ,

    fk_idComment         INTEGER     ,

    FOREIGN KEY ( fk_idUser ) REFERENCES User( id )  ,

    FOREIGN KEY ( fk_idDokument ) REFERENCES Document( idDocument )  ,

    FOREIGN KEY ( fk_idComment ) REFERENCES Comment( idComment )  

 );

  

CREATE TABLE DeletedComment ( 

    idComment            INTEGER NOT NULL  PRIMARY KEY  ,

    date                 DATETIME     ,

    comment              TEXT(500) NOT NULL    ,

    fk_idUser            INTEGER NOT NULL    ,

    fk_idDokument        INTEGER NOT NULL    ,

    fk_idComment         INTEGER     ,

    FOREIGN KEY ( fk_idUser ) REFERENCES User( id )  ,

    FOREIGN KEY ( fk_idDokument ) REFERENCES Document( idDocument )  ,

    FOREIGN KEY ( fk_idComment ) REFERENCES DeletedComment( idComment )  

 );

  

CREATE TABLE DocumentHasMetadata ( 

    idMetadata           INTEGER NOT NULL  PRIMARY KEY  ,

    title                VARCHAR(250) NOT NULL    ,

    description          TEXT NOT NULL    ,

    uploadDate           DATETIME     ,

    creationDate         DATE NOT NULL    ,

    views                INTEGER     ,

    comments             INTEGER     ,

    votes                INTEGER     ,

    fk_idDokument        INTEGER NOT NULL    ,

    fk_idDocumentType    INTEGER NOT NULL    ,

    fk_idUser            INTEGER NOT NULL    ,

    fk_idCatalog         INTEGER NOT NULL    ,

    fk_idAccess          INTEGER NOT NULL    ,

    FOREIGN KEY ( fk_idDokument ) REFERENCES Document( idDocument )  ,

    FOREIGN KEY ( fk_idDocumentType ) REFERENCES DocumentType( idType )  ,

    FOREIGN KEY ( fk_idUser ) REFERENCES User( id )  ,

    FOREIGN KEY ( fk_idCatalog ) REFERENCES Catalog( idCatalog )  ,

    FOREIGN KEY ( fk_idAccess ) REFERENCES Access( idAccess )  

 );

  

CREATE TABLE DocumentHasTags ( 

    fk_idDokument        INTEGER NOT NULL    ,

    fk_idTags            INTEGER NOT NULL    ,

    CONSTRAINT pk_DocumentHasTags PRIMARY KEY ( fk_idDokument, fk_idTags ),

    FOREIGN KEY ( fk_idDokument ) REFERENCES Document( idDocument )  ,

    FOREIGN KEY ( fk_idTags ) REFERENCES Tags( idTags )  

 );

  

CREATE TABLE TagCategoryHasTags ( 

    fk_idTagCategory     INTEGER NOT NULL    ,

    fk_idTags            INTEGER NOT NULL    ,

    CONSTRAINT pk_TagCategoryHasTags PRIMARY KEY ( fk_idTagCategory, fk_idTags ),

    FOREIGN KEY ( fk_idTagCategory ) REFERENCES TagCategory( idTagCategory )  ,

    FOREIGN KEY ( fk_idTags ) REFERENCES Tags( idTags )  

 );

  

CREATE TABLE Thumbnail ( 

    idThumbnail          INTEGER NOT NULL  PRIMARY KEY  ,

    size                 VARCHAR(10) NOT NULL    ,

    mimetype             VARCHAR(50) NOT NULL    ,

    filename             VARCHAR(250) NOT NULL    ,

    image                BLOB     ,

    fk_idUser            INTEGER NOT NULL    ,

    FOREIGN KEY ( fk_idUser ) REFERENCES User( id )  

 );

  

CREATE UNIQUE INDEX ix_User_email ON User ( email );

  

CREATE UNIQUE INDEX ix_User_username ON User ( username );
```

  
  

# Prosjektdagbok

Tabellen under viser arbeidsfordelingen på prosjektdeltakerne

| Oppgave                                       | Prosjektdeltager | Tidsbruk |
|-----------------------------------------------|------------------|----------|
| Designe database                              | Haakon           | 3 timer  |
| Lage testdata                                 | Haakon           | 3 timer  |
| Lage spørringer                               | Haakon           | 4 timer  |
| Oppsett av Flask                              | Stian            | 4 timer  |
| Oppsett i github                              | Stian            | 2 timer  |
| Lagt inn bootstrap                            | Haakon           | 1 time   |
| Testing av teknologi                          | Felles           | 5 timer  |
| Implementering av DB                          | Haakon           | 8 timer  |
| Lage templates og få ut alle sider            | Stian            | 10 timer |
| Flytte av repo over på riktig (datateknikk)   | Haakon           | 5 timer  |
| Endring over til SQLAlchemy                   | Stian            | 5 timer  |
| Diverse utvikling                             | Felles           | 30 timer |
| Endring fra Bootstrap til Tailwind (Redesign) | Stian            | 10 timer |
| Siste finpuss                                 | Felles           | 15 timer |
| Deployment                                    | Stian            | 5 timer  |
  

# Egne vurderinger

Det har vært en meget lærerik prosess å jobbe med denne løsningen, og funksjonalitet har gradvis blitt utvidet etterhvert som vi ble modnet inn i de tekniske mulighetene som finnes gjennom blant annet Flask. Vi har lagt til grunn en iterativ og agil utviklingsprosess, der vi har testet løsningen jevnlig for å se om vi skal fortsette i det samme eller i et nytt spor. Den endelige løsningen har dermed blitt relativt annerledes enn de initielle idèene vi startet med. 

  

Løsningen er utarbeidet med tanke på skalerbarhet. Den kan enkelt utvides både med tanke på ny funksjonalitet og i forhold til nye tabeller og data. Eksempelvis kan den lett utvides med nye katalogkategorier, tags-kategorier og tags. Det kan også enkelt legges til nye brukergrupper som for eksempel moderatorer.

  

Slik arkitekturen og teknologien er utviklet kan løsningen også enkelt utvides med ny funksjonalitet. Noen tanker rundt dette kobling mot sosiale medier som Facebook, LinkedIn og Twitter der man kan dele rapporten på sosiale medier. Andre ting kan være mulighet til å invitere venner. Vi tenker også at løsningen enkelt kan være en “whitelabel”-løsning, der plattformen benyttes av for eksempel universiteter eller høyskoler - eller i helt andre bransjer eller bruksområder.