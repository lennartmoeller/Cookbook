import os
from openai import OpenAI
from helpers import load_json, save_json

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

FORMAT_PROMPT = """
Regeln zum Formatieren von Rezepten:

- **Struktur**:
	- Das Rezept hat den Rezeptnamen als Titel, aber nicht mehr (z.B. Chili con Tofu). Der Titel soll eine Markdown-H1-Überschrift sein.
	- Nach dem Titel kommt eine Auflistung der Eckdaten des Rezepts als Stichpunkte, ohne Überschrift:
		- Ernährungseinschränkung: {omnivore, pescetarisch, vegetarisch, vegan}
		- Portionen: *Anzahl der Portionen einsetzen*
	- Die Zutaten werden mit einer Markdown-H3-Überschrift "Zutaten" eingeleitet.
	- Die Zubereitungsschritte werden mit einer Markdown-H3-Überschrift "Zubereitungsschritte" eingeleitet.
- **Zutaten**:
	- Die Zutaten werden als Aufzählung dargestellt, wobei jede Zeile mit einem Bindestrich beginnt, gefolgt von Menge, Einheit und dem Namen der Zutat (z. B. „350 g Räuchertofu“).
	- Die Zutaten werden in der Reihenfolge aufgelistet, in der sie in den Zubereitungsschritten verarbeitet werden. Falls das Originalrezept eine andere Reihenfolge vorgibt, ist diese zugunsten der klaren Ablaufbeschreibung anzupassen.
	- Es ist auf eine einheitliche Schreibweise der Einheiten und der Zutatennamen zu achten: kg, g, EL, TL, ml, L
	- Standard-Zutaten, die typischerweise zu Hause vorhanden sind, werden aus der Zutatenliste ausgelassen. Dazu gehören ausschließlich Salz, Pfeffer, Wasser, Olivenöl. Falls durch das Weglassen einer Zutat eine Mengenangabe verloren geht, muss diese Mengenangabe im entsprechenden Zubereitungsschritt explizit erwähnt werden.
- **Schritte**:
	- Die Zubereitungsschritte werden nummeriert, wobei jeder Schritt mit einer Zahl und einem Punkt beginnt (z. B. „1. Den Tofu und die Paprikas in kleine Würfel schneiden.“).
	- Alle Anweisungen werden als Infinitivsätze formuliert, ohne direkte Anrede oder Personalpronomen (z. B. „Die Zwiebel in kleine Würfel schneiden.“).
	- Imperativ- oder Bitte-Formulierungen („Bitte schneide…“, „Schneide…“) sind zu vermeiden.
	- Passivkonstruktionen („Die Zwiebel muss in kleine Würfel geschnitten werden.“) werden nicht verwendet; es wird aktiv und direkt formuliert.
	- Die Anweisungen sollen klar, kurz und präzise sein und genau beschreiben, welche Zutat wie verarbeitet wird.
	- Alle Schritte folgen einem konsistenten Satzmuster, sodass der Ablauf gut nachvollziehbar ist.
	- Zeit- und Temperatureinstellungen (z. B. „für 5 Minuten“, „2 Stunden köcheln“) werden klar und einheitlich angegeben.
	- Alle Rezepte werden in derselben Sprache und im gleichen sachlichen, neutralen Stil verfasst.
	- Jeder Zubereitungsschritt enthält nur eine logisch abgeschlossene Aufgabe.
	- Kombinationen mehrerer Aufgaben in einem Schritt sind nur zulässig, wenn sie einen natürlichen, zusammenhängenden Arbeitsablauf bilden und nicht zu einer überladenen Anweisung führen.
	- Aufgaben, die inhaltlich getrennt bearbeitet werden, sind in separate, klar abgegrenzte Schritte zu gliedern, um eine übersichtliche und nachvollziehbare Anleitung zu gewährleisten.

Ich möchte Rezepte für ein Kochbuch einheitlich verfassen. Bitte passe das Rezept so an, das es den oben genannten Regeln entspricht.  Achte darauf, den Inhalt des Rezepts nicht zu verändern. Bitte gebe mir nur das bearbeitete Rezept aus, nichts weiteres.
"""

def get_recipe_path(recipe):
    if recipe.get("category"):
        return os.path.join("recipes", recipe["category"], recipe["name"] + ".md")
    return os.path.join("recipes", recipe["name"] + ".md")

def format_recipe(content):
    prompt = FORMAT_PROMPT + "\n\n" + content
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def main():
    recipes = load_json("recipes.json")
    updated = False
    for recipe in recipes:
        if not recipe.get("formatted"):
            path = get_recipe_path(recipe)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                formatted = format_recipe(content)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(formatted)
                recipe["formatted"] = True
                updated = True
                print(f"Formatted recipe: {recipe['name']}")
    if updated:
        save_json(recipes, "recipes.json")
    else:
        print("All recipes are already formatted.")

if __name__ == "__main__":
    main()
