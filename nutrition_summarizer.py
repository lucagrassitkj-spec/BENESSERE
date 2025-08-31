import feedparser
import yaml
import os
import random
from datetime import datetime, timedelta

# Lista completa di frasi motivazionali
motivational_quotes = [
    "Ogni piccolo passo verso la salute è un grande passo verso la felicità!",
    "Il benessere inizia da ciò che scegli di mangiare oggi.",
    "Prenditi cura del tuo corpo, è l’unico posto in cui devi vivere.",
    "Mangiare sano è un atto di amore verso te stesso.",
    "Un giorno alla volta: scegli il cibo che ti dà energia e gioia.",
    "Mangiare sano è un regalo che fai al tuo corpo ogni giorno.",
    "Ogni pasto è un’opportunità per nutrire il tuo benessere.",
    "Il benessere parte dal piatto e arriva al cuore.",
    "Scegli cibi che ti danno energia, non solo sazietà.",
    "Ogni piccolo cambiamento nella dieta porta grandi risultati.",
    "La tua salute merita ogni scelta consapevole che fai.",
    "Il cibo è il carburante della tua felicità.",
    "Mangiare bene oggi significa sentirsi meglio domani.",
    "Prenditi cura del tuo corpo: è l’unico posto in cui vivi.",
    "Il piacere del cibo sano è anche il piacere della vita.",
    "Sii gentile con te stesso: scegli ciò che nutre davvero.",
    "Ogni pasto sano è un passo verso una vita più lunga e felice.",
    "Il benessere non è una dieta, è uno stile di vita.",
    "Mangiare con consapevolezza è un atto di amore verso se stessi.",
    "Nutri il tuo corpo e la tua mente ti ringrazieranno.",
    "La salute inizia da ciò che metti nel piatto.",
    "Più colori nel piatto, più vitalità nel corpo.",
    "Il cibo sano è il primo investimento nella tua energia.",
    "Prenditi cura del tuo corpo oggi e ti ringrazierà domani.",
    "Scegli il cibo che ti fa sentire leggero, energico e felice."
]

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def fetch_articles(feed_url, lookback_hours):
    feed = feedparser.parse(feed_url)
    cutoff = datetime.utcnow() - timedelta(hours=lookback_hours)
    links = []
    for entry in feed.entries[:5]:
        published = None
        if hasattr(entry, "published_parsed"):
            published = datetime(*entry.published_parsed[:6])
        if published and published < cutoff:
            continue
        links.append(entry.link)
    return links

def main():
    config = load_config()
    os.makedirs("output", exist_ok=True)
    fname = f"output/rassegna_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    all_links = []

    for cat in config["categories"]:
        for feed in cat["feeds"]:
            try:
                articles = fetch_articles(feed, config.get("lookback_hours", 72))
                all_links.extend(articles[:config.get("max_per_category", 2)])
            except Exception as e:
                print(f"Errore con {feed}: {e}")

    # Seleziona una frase motivazionale a caso
    quote = random.choice(motivational_quotes)

    # Scrivi la frase prima dei link
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"{quote}\n\n")
        for link in all_links:
            f.write(f"{link}\n")

    print("File salvato:", fname)

if __name__ == "__main__":
    main()
