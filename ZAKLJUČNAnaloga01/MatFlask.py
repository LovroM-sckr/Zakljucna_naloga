#  Dobrodošel v klepetalnici!
#  V tej datoteki se nahaja osnovna implementacija klepetalnice s Flaskom in TinyDB-jem.
#  Sledi navodilom v komentarjih in izpolni naloge.
#  Će boš tu investiral čas, ga boš prihranil pri izdelavi zaključne naloge.
#  Srečno!
#  Aja, naloga ti lahko prinese DO 10% dodatnih točk pri zaključni nalogi.
#  O bonusu se ne pogajamo! :) 

# VSA KODA RAZEN CSS MORA BITI POPOLNOMA RAZUMETA IN NAPISANA SAMOSTOJNO! 
# TESTIRAJ! TESTIRAJ! TESTIRAJ!
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import os

# Ustvarimo Flask aplikacijo
# Flask je mikro ogrodje za spletne aplikacije v Pythonu
# Več info: https://flask.palletsprojects.com/
app = Flask(__name__)
app.secret_key = "skrivni_kljuc_123"  # V produkciji uporabi pravi skrivni ključ!

# ---- RAZLAGA: TinyDB ----
# TinyDB je preprosta dokumentna podatkovna baza za Python
# Shranjuje podatke v JSON datoteko - brez potrebe po SQL strežniku
# Idealno za manjše aplikacije in učenje
# Več info: https://tinydb.readthedocs.io/
# --------------------------
db = TinyDB('klepet.json')
users = db.table('uporabniki')  # Tabela za uporabnike
messages = db.table('sporocila')  # Tabela za sporočila
User = Query()  # Za poizvedbe po bazi




# ---- RAZLAGA: Flask Routes (Poti) ----
# @app.route() je dekorator, ki pove Flask-u, katero URL pot naj poveže s katero funkcijo
# Ko uporabnik obišče določeno pot v brskalniku, Flask pokliče ustrezno funkcijo
# / = glavna stran (root)
# Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#routing
# --------------------------------------
@app.route('/')
def index():
    # ---- RAZLAGA: Flask Sessions ----
    # session je Flaskov način za shranjevanje podatkov za posameznega uporabnika
    # Deluje podobno kot piškotki, vendar so podatki shranjeni na strežniku in zaščiteni
    # Seja se uporablja za preverjanje, ali je uporabnik prijavljen
    # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#sessions
    # ------------------------------

    # ZNAJE ZA ZAGOVOR: najdi session v brskalniku 
    # Zapiši še nekaj v cookie in nekaj preberi iz njega (npr. število obiskov,  čas zadnjega obiska, ipd.)
    # Cookie in njegovo vsebino najdi v brskalniku.
    if 'username' in session:
        #return render_template('chat.html')
        return render_template('index.html')
        #return redirect(url_for('indexL'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # ---- RAZLAGA: request.method ----
    # request.method nam pove, katera vrsta HTTP zahteve je bila poslana
    # Z 'if request.method == "POST":' preverjamo, ali je bila poslana POST zahteva (oddaja obrazca)
    # Če ni bila POST, je verjetno GET (uporabnik je obiskal stran)
    # GET zahteve običajno uporabljamo za prikaz strani, POST za oddajo obrazca
    # metodo določimo v Ajax zahtevi ali v HTML formi
    # klic iz brskalnika je vedno GET
    # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#accessing-request-data
    # -----------------------------
    # ZNANJE ZA ZAGOVOR: nujno razumeti kdaj prikažemo predlogo in kdaj JSON

    if request.method == 'POST':
        # try v tem primeru prepreči, da bi aplikacija sesula, če pride do napake
        try:
            # ---- RAZLAGA: request.form ----
            # request.form je slovar, ki vsebuje podatke obrazca, poslane z metodo POST
            # Dostopamo do njih z request.form['ime_polja']
            # GET zahteve (običajno) uporabljajo request.args za dostop do parametrov 
            # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#the-request-object
            # -----------------------------
            username = request.form['username']
            password = request.form['password']
            # če bi uporabljal GET, bi uporabil request.args.get('username')
            
            # Preveri, ali uporabnik obstaja v bazi
            user = users.get(User.username == username)
            
            if user:
                # Uporabnik obstaja, preveri geslo
                # če bi želeli uporabiti cookies, bi lahko tukaj preverili tudi username iz piškotka
                if user['password'] == password:
                    session['username'] = username
                    # ---- RAZLAGA: jsonify ----
                    # jsonify pretvori Python slovar v JSON odgovor
                    # jsonify ni potreben, vendar je priporočljiv za doslednost
                    # To je uporabno za AJAX zahteve, kjer klient pričakuje JSON
                    # Več info: https://flask.palletsprojects.com/en/2.0.x/api/#flask.json.jsonify
                    # --------------------------

                    # ta return se izvede samo, če je prijava uspešna
                    return jsonify({'success': True})
                    #return render_template('index.html')
                    
                else:
                    # ta return se izvede samo, če je geslo napačno
                    return jsonify({'success': False, 'error': 'Napačno geslo'})
            else:
                # Uporabnik ne obstaja, ustvari novega
                users.insert({'username': username, 'password': password})

                # ---- RAZLAGA: session['key'] ----
                # session je slovar, v katerem lahko shranjujemo podatke za uporabnika
                # session['key'] shrani vrednost pod ključ
                # Uporabljamo ga za shranjevanje podatkov o prijavi uporabnika
                # session poteče, ko uporabnik zapre brskalnik
                # za daljše seje uporabi piškotke (pogooglaj max cookie age )
                # Več info: https://flask.palletsprojects.com/en/2.0.x/quickstart/#sessions
                # --------------------------

                session['username'] = username
                # ta return se izvede samo, če je uporabnik nov
                return jsonify({'success': True})
                
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    
    # Če je metoda GET, prikaži predlogo za prijavo
    # ZNANJE ZA ZAGOVOR: nujno razumeti kdaj prikažemo predlogo in kdaj JSON
    return render_template('login.html')
    # return render_template('loginL.html') # tu bo mala spremebica
    
@app.route('/index', methods=['GET', 'POST'])
def indexL():
     return render_template('index.html')

@app.route('/logout')
def logout():
    # ---- RAZLAGA: session.pop ----
    # session.pop() odstrani ključ iz seje
    # Drugi parameter (None) je privzeta vrednost, če ključ ne obstaja
    # To se uporablja za odjavo uporabnika - odstranimo njegovo uporabniško ime iz seje
    # --------------------------

    # ZNANJE ZA ZAGOVOR: preveri razliko med session, cookies in local storage in kako se uporabljajo
    
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/kontakt')
def kontakt():
    # ---- RAZLAGA: session.pop ----
    # session.pop() odstrani ključ iz seje
    # Drugi parameter (None) je privzeta vrednost, če ključ ne obstaja
    # To se uporablja za odjavo uporabnika - odstranimo njegovo uporabniško ime iz seje
    # --------------------------

    # ZNANJE ZA ZAGOVOR: preveri razliko med session, cookies in local storage in kako se uporabljajo
    
    #session.pop('username', None)
    return render_template('kontakt.html')

@app.route('/karte')
def karte():
    
    return render_template('karte.html')

@app.route('/majice')
def majice():
    
    return render_template('majice.html')
@app.route('/kape')
def kape():
    
    return render_template('kape.html')
@app.route('/zastave')
def zastave():
    
    return render_template('zastave.html')

@app.route('/get_messages')
def get_messages():
    # Tukaj preprečimo nepooblaščen dostop do sporočil
    # Torej, če uporabnik ni prijavljen, mu vrnemo napako
    if 'username' not in session:
        # ---- RAZLAGA: HTTP Status Codes ----
        # Drugi parameter v jsonify() določa HTTP status kodo
        # 401 = Unauthorized (Nepooblaščen dostop)
        # Druge pogoste kode: 200 (OK), 404 (Not Found), 500 (Server Error)
        # Več info: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        # ----------------------------------
        return jsonify({'error': 'Niste prijavljeni'}), 401
    
    all_messages = messages.all()
    return jsonify(all_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'error': 'Niste prijavljeni'}), 401
    
    try:
        message_text = request.form['message']
        username = session['username']
        # NALOGA: Oblikuj timestamp v lepši format.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Vstavi sporočilo v bazo
        messages.insert({
            'username': username,
            'message': message_text,
            'timestamp': timestamp
        })
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Napaka pri pošiljanju sporočila: {str(e)}")
        return jsonify({'success': False, 'error': 'Napaka pri pošiljanju'})


if __name__ == "__main__":
    
    app.run(debug=True, port = 8080)
    