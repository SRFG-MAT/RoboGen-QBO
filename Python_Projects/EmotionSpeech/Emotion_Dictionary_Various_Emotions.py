# Dictionary wurde so gewählt, damit das Programm in Zukunft vielleicht diversere Emotionen bestimmen kann
# Positiv und Negativ muss noch in das Wörterbuch eingebaut werden, um oft verwendete Wörter abzudecken
#!/usr/bin/env python
# coding=utf-8

emo_dic = {
    "Wut": {
        "Ärger": ["ärger", "verärger", "zorn", "wut", "wüt", "rage", "grimm", "böse", "entrüst", "empör", "erzürn",
                  "erbost"],
        "Eifersucht": ["eifersucht", "eifersücht"],
        "Hass": ["hass", "verhass"],
        "Neid": ["neid", "neidisch", "missgunst", "missgünst"],
        "Unzufrieden": ["unzufried", "verdrossen", "missmut", "missmüt"],
        "Verachtung": ["veracht"]
    },
    "Ekel": ["ekel", "abscheu", "widerwill", "übel", "angewidert", "verleide"],
    "Angst": {
        "Angst": ["angst", "ängst", "bang", "sorge", "besorg", "beklomm", "beunruh", "beklemm"],
        "Furcht": ["furcht", "fürcht", "panik"],
        "Scham": ["scham", "schämen", "geschämt", "verschämt", "verlegen"],
        "Spannung/Stress": ["spannung", "erreg", "stress", "nerv", "unruh", "anspannung", "angespannt", "belast"],
        "Verzweiflung": ["verzweifl", "hoffnungslos", "entmutig", "ohnmacht", "ohnmächt", "hilflos", "machtlos"]
    },
    "Glücklich": {
        "Bewunderung": ["bewund", "verehr", "ehrfurcht", "ehrfürchtig"],
        "Dankbarkeit": ["dankbar"],
        "Entspanntheit": ["entspann", "gelöst", "locker", "ruhig", "ruhe", "cool", "gelass", "unbeschwert", "unbesorgt",
                          "ausgeglichen"],
        "Erleichterung": ["erleichter", "befrei", "erlös", "ermutig"],
        "Freude": ["freude", "erfreut", "frohlock", "jubel", "zück", "froh", "freudig"],
        "Glück": ["glück", "glücklich", "beglückt", "glückselig", "überglücklich", "selig", "wonne"],
        "Heiterkeit": ["heiter", "vergnüg", "fröhlich", "frohsinn", "lustig", "spass", "belustig", "gutgelaunt",
                       "ausgelassen"],
        "Hoffnung": ["hoffnung", "hoffnungsvoll", "zuversicht", "optimis"],
        "Liebe": ["liebe", "verliebt", "zärtlich", "zuneigung"],
        "Lust": ["lust", "lustvoll", "leidenschaft", "leidenschaftlich", "eksta"],
        "Stolz": ["stolz", "erfolg"],
        "Wohlbefinden": ["wohlgefühl", "wohlbefinden", "wohlfüh"],
        "Zufriedenheit": ["zufrieden", "befriedig", "genugtu"]
    },
    "Traurig": {
        "Enttäuschung": ["enttäusch", "frust", "ernüchter"],
        "Langeweile": ["langeweile", "langweil"],
        "Mitleid": ["mitleid", "mitleidgefühl", "mitleidig", "mitgefühl", "mitfühl", "mitempfind", "teilnahm",
                    "anteilnahm", "empathie"],
        "Rührung": ["rührung", "gerührt", "ergriffen", "bewegt"],
        "Schuld": ["schuld", "reue", "gewissensbiss", "schlechtesgewissen", "zerknirsch"],
        "Sehnsucht": ["sehnsucht", "sehnsüchtig", "sehen", "nostalg", "verlang", "heimweh", "fernweh"],
        "Traurigkeit": ["traurig", "trauer", "schwermut", "schwermüt", "trüb", "niedergeschlag", "bedrückt", "depress",
                        "melanchol", "wehm", "kummer", "kümmer", "verzagt", "gram", "weh", "resign"]
    },
    "Überrascht": {
        "Bestürzung": ["bestürz", "entsetz", "verstör", "schreck", "schock", "erschrock", "entgeist", "verdatter",
                       "betroffen", "fassungslos"],
        "Interesse": ["interess", "neugier", "enthusias", "begeist", "aufgestellt"],
        "Irritation": ["irrit", "verstimm", "unmut", "indig", "gereizt"],
        "Überraschung": ["überrasch", "erstaun", "verwund", "verblüff", "konsternier", "staun", "verdutz"]
    },
    "Positiv": ["schön", "gut", "toll", "angenehm", "positiv"],
    "Negativ": ["schlecht", "sauer", "lustlos", "mies", "ungut", "negativ"]
}