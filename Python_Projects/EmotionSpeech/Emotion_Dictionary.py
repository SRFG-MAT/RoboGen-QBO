# Die sehr einfache Variante des Dictionaries
# coding=utf-8

emo_dic = {
    "Wut": [
        "aerger", "veraerger", "zorn", "wut", "wuet", "rage", "grimm", "boese", "entruest", "empoer", "erzuern",
        "erbost","eifersucht", "eifersuecht", "hass", "verhass", "neid", "neidisch", "missgunst", "missguenst",
        "unzufried", "verdrossen", "missmut", "missmuet", "veracht", "sauer", "mies", "ungut"
    ],
    "Ekel": ["ekel", "abscheu", "widerwill", "uebel", "angewidert", "verleide"],
    "Angst": [
        "angst", "aengst", "bang", "sorge", "besorg", "beklomm", "beunruh", "beklemm", "furcht", "fuercht", "panik",
        "scham", "schaemen", "geschaemt", "verschaemt", "verlegen", "spannung", "erreg", "stress", "nerv", "unruh",
        "anspannung", "angespannt", "belast","verzweifl", "hoffnungslos", "entmutig", "ohnmacht", "ohnmaecht",
        "hilflos", "machtlos"
    ],
    "Gluecklich": [
        "bewund", "verehr", "ehrfurcht", "ehrfuerchtig", "dankbar", "entspann", "geloest", "locker", "ruhig", "ruhe",
        "cool", "gelass", "unbeschwert", "unbesorgt", "ausgeglichen", "erleichter", "befrei", "erloes", "ermutig",
        "freude", "erfreut", "frohlock", "jubel", "zueck", "froh", "freudig", "glueck", "gluecklich", "beglueckt",
        "glueckselig", "uebergluecklich", "selig", "wonne", "heiter", "vergnueg", "froehlich", "frohsinn", "lustig", "spass",
        "belustig", "gutgelaunt", "ausgelassen", "hoffnung", "hoffnungsvoll", "zuversicht", "optimis", "liebe",
        "verliebt", "zaertlich", "zuneigung", "lust", "lustvoll", "leidenschaft", "leidenschaftlich", "eksta", "stolz",
        "erfolg", "wohlgefuehl", "wohlbefinden", "wohlfueh", "zufrieden", "befriedig", "genugtu", "schoen", "gut", "toll",
        "angenehm", "positiv"
    ],
    "Traurig": [
        "enttaeusch", "frust", "ernuechter", "langeweile", "langweil", "mitleid", "mitleidgefuehl", "mitleidig",
        "mitgefuehl", "mitfuehl", "mitempfind", "teilnahm", "anteilnahm", "empathie", "ruehrung", "geruehrt", "ergriffen",
        "bewegt", "schuld", "reue", "gewissensbiss", "schlechtesgewissen", "zerknirsch", "sehnsucht", "sehnsuechtig",
        "sehen", "nostalg", "verlang", "heimweh", "fernweh", "traurig", "trauer", "schwermut", "schwermuet", "trueb",
        "niedergeschlag", "bedrueckt", "depress", "melanchol", "wehm", "kummer", "kuemmer", "verzagt", "gram", "weh",
        "resign", "schlecht", "lustlos", "negativ"
    ],
    "Ueberrascht": [
        "bestuerz", "entsetz", "verstoer", "schreck", "schock", "erschrock", "entgeist", "verdatter", "betroffen",
        "fassungslos", "interess", "neugier", "enthusias", "begeist", "aufgestellt", "irrit", "verstimm", "unmut",
        "indig", "gereizt", "ueberrasch", "erstaun", "verwund", "verblueff", "konsternier", "staun", "verdutz"
    ],
}

# Es koennten noch mehrer Emotionsaenderer inkludiert werden, die z.B. eine Emotion abschwaechen, verstaerken, etc.
emo_changers = {
    "Negators": ["nicht", "nichts", "kein", "keine", "niemand", "ohne"]
}