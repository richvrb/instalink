# 🚀 Instagram Bio Link Tracker - Deployment Guide

## Wat heb je gemaakt?

Een Flask app die:
- ✅ Elke klik op je Instagram bio link tracked
- ✅ IP adres, land, stad, device type, browser logt
- ✅ Doorverwijst naar instagram.com/richvrb
- ✅ Dashboard op `/dashboard` om statistieken te zien

## 📁 Bestanden

- `app.py` - Hoofd Flask applicatie
- `requirements.txt` - Python dependencies
- `Procfile` - Railway start command
- `railway.json` - Railway configuratie
- `tracking_data.csv` - Data opslag (wordt automatisch aangemaakt)

## 🚂 Deployment naar Railway.app

### Stap 1: Maak Railway account
1. Ga naar https://railway.app
2. Klik "Login" rechtsboven
3. Login met GitHub (aangeraden) of email
4. Verifieer je email als gevraagd

### Stap 2: Upload je code naar GitHub
1. Ga naar https://github.com/new
2. Maak een nieuwe repository (bijvoorbeeld: `instagram-tracker`)
3. Zet op **Private** (belangrijk voor privacy!)
4. Klik "Create repository"

5. Upload alle bestanden:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`

   Je kunt dit via de GitHub web interface doen (drag & drop) of via terminal:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/JOUW_USERNAME/instagram-tracker.git
   git push -u origin main
   ```

### Stap 3: Deploy op Railway
1. Ga naar https://railway.app/dashboard
2. Klik "New Project"
3. Kies "Deploy from GitHub repo"
4. Selecteer je `instagram-tracker` repository
5. Railway detecteert automatisch Python en start deployment
6. Wacht 1-2 minuten tot deployment klaar is

### Stap 4: Krijg je link
1. Klik op je project in Railway dashboard
2. Ga naar "Settings" tab
3. Scroll naar "Domains"
4. Klik "Generate Domain"
5. Je krijgt een URL zoals: `https://instagram-tracker-production-xxxx.up.railway.app`

**DIT IS JE INSTAGRAM BIO LINK! 🎉**

### Stap 5: Test je link
1. Open de link in je browser
2. Je wordt doorgestuurd naar instagram.com/richvrb
3. Ga naar `https://jouw-link.up.railway.app/dashboard`
4. Zie je eerste click met IP, locatie, device info!

### Stap 6: Zet in Instagram bio
1. Open Instagram app
2. Ga naar je profiel
3. Klik "Edit Profile"
4. Plak je Railway link in "Website" veld
5. Klik "Done"

## 📊 Dashboard gebruiken

- **Hoofd link**: `https://jouw-link.up.railway.app` → redirects naar Instagram
- **Dashboard**: `https://jouw-link.up.railway.app/dashboard` → zie statistieken

Dashboard toont:
- Total clicks
- Aantal landen
- Top device (Mobile/Desktop/Tablet)
- Clicks per land
- Recente clicks met details

Dashboard vernieuwt automatisch elke 30 seconden.

## 💰 Kosten

Railway geeft **$5 gratis credit per maand**.

Deze app gebruikt ongeveer:
- ~$0.20-$1.00 per maand (afhankelijk van traffic)
- Bij 1000-5000 clicks/maand blijf je ruim onder de gratis $5

**Belangrijk**: Voeg een creditcard toe aan Railway (vereist), maar je wordt pas belast als je $5 credit op is.

## 🔒 Privacy & Beveiliging

**Belangrijke tips:**
1. Zet je GitHub repo op **PRIVATE**
2. Deel je `/dashboard` link NIET publiekelijk
3. Je logt IP adressen - dit is persoonlijke data
4. Gebruik alleen voor je eigen Instagram profiel
5. Verwijder oude data regelmatig als je wilt

**GDPR compliance (als je in EU bent):**
- Overweeg een privacy policy toe te voegen
- Verwijder oude data na X dagen
- Informeer bezoekers dat je tracking gebruikt

## 🛠️ Aanpassingen

### Andere redirect URL
Open `app.py` en wijzig regel 9:
```python
REDIRECT_URL = f"https://www.instagram.com/{INSTAGRAM_USERNAME}"
```
Naar bijvoorbeeld:
```python
REDIRECT_URL = "https://jouwwebsite.com"
```

### Dashboard beveiligen met wachtwoord
Voeg toe aan `app.py` onder de imports:
```python
DASHBOARD_PASSWORD = "geheim123"

@app.route('/dashboard')
def dashboard():
    password = request.args.get('pw', '')
    if password != DASHBOARD_PASSWORD:
        return "Unauthorized", 401
    # rest van de functie...
```

Dan moet je naar: `https://jouw-link.up.railway.app/dashboard?pw=geheim123`

## 🐛 Problemen oplossen

**App start niet:**
- Check Railway logs: klik op je project → "Deployments" → laatste deployment → "View Logs"
- Kijk naar errors in rood

**Geen data in dashboard:**
- Controleer of mensen je link hebben geklikt
- Check Railway logs voor errors bij schrijven naar CSV

**Link werkt niet:**
- Controleer of deployment succeeded is (groen vinkje in Railway)
- Test of domain gegenereerd is in Settings → Domains

**CSV data verdwijnt na redeploy:**
- Railway heeft geen permanente storage op gratis tier
- Voor permanente opslag: upgrade naar Railway database (PostgreSQL) of gebruik externe service

## 📞 Support

Vragen? Check:
- Railway docs: https://docs.railway.app
- Flask docs: https://flask.palletsprojects.com

## ✅ Checklist

- [ ] Railway account gemaakt
- [ ] GitHub repo aangemaakt (PRIVATE!)
- [ ] Code geüpload naar GitHub
- [ ] Project deployed op Railway
- [ ] Domain gegenereerd
- [ ] Link getest (redirect werkt)
- [ ] Dashboard gecontroleerd (data wordt gelogd)
- [ ] Link in Instagram bio gezet
- [ ] Eerste clicks ontvangen! 🎉

Succes met je Instagram bio link tracker! 🚀
