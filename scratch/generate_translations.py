import polib
import os

locale_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale')
languages = {
    'fr': {
        "Home Dashboard": "Tableau de Bord",
        "Welcome to Your New App!": "Bienvenue dans votre nouvelle application !",
        "Home": "Accueil",
        "About": "À propos",
        "Services": "Services",
        "Dark Theme": "Thème Sombre",
        "Light Theme": "Thème Clair",
        "Sunset Theme": "Thème Coucher de Soleil",
        "Click Me!": "Cliquez ici !",
        "It works!": "Ça marche !",
        "Glassmorphism": "Verre Dépoli",
        "Dynamic Themes": "Thèmes Dynamiques",
    },
    'es': {
        "Home Dashboard": "Panel Principal",
        "Welcome to Your New App!": "¡Bienvenido a tu nueva aplicación!",
        "Home": "Inicio",
        "About": "Acerca de",
        "Services": "Servicios",
        "Dark Theme": "Tema Oscuro",
        "Light Theme": "Tema Claro",
        "Sunset Theme": "Tema Atardecer",
        "Click Me!": "¡Haga Clic!",
        "It works!": "¡Funciona!",
        "Glassmorphism": "Cristal Esmerilado",
        "Dynamic Themes": "Temas Dinámicos",
    }
}

for lang, translations in languages.items():
    lang_dir = os.path.join(locale_dir, lang, 'LC_MESSAGES')
    os.makedirs(lang_dir, exist_ok=True)
    
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2026-04-10 14:00+0000',
        'PO-Revision-Date': '2026-04-10 14:00+0000',
        'Last-Translator': 'you <you@example.com>',
        'Language-Team': f'{lang} <yourteam@example.com>',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }
    
    for msgid, msgstr in translations.items():
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
            msgctxt=''
        )
        po.append(entry)
        
    po.save(os.path.join(lang_dir, 'django.po'))
    po.save_as_mofile(os.path.join(lang_dir, 'django.mo'))
    print(f"Generated translations for {lang}")
