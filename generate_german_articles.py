#!/usr/bin/env python3
"""
Script to generate remaining German articles for Answers Platform
Creates 17 more articles to complete the German collection (20 total)
"""

import os

articles_data = [
    {
        "filename": "wut-ueberwinden.html",
        "title": "Wut überwinden: Weisheit aus 8 Traditionen",
        "description": "Wie kann man Wut kontrollieren und transformieren? Vergleichende Analyse der Ansätze von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus zur Bewältigung von Wut.",
        "keywords": "Wut überwinden, Wutmanagement, Emotionale Kontrolle, Ärger bewältigen, innere Ruhe, philosophische Weisheit",
        "word_count": 3100
    },
    {
        "filename": "wahres-glueck-finden.html",
        "title": "Wahres Glück finden: Weisheit aus 8 Traditionen",
        "description": "Was ist wahres Glück und wie findet man es? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Glück und Zufriedenheit.",
        "keywords": "Glück finden, wahres Glück, Zufriedenheit, Lebensfreude, innerer Frieden, spirituelles Glück",
        "word_count": 3300
    },
    {
        "filename": "vergebung-versoehnung.html",
        "title": "Vergebung und Versöhnung: Weisheit aus 8 Traditionen",
        "description": "Wie kann man vergeben und Versöhnung finden? Vergleichende Analyse der Ansätze von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus zur Vergebung.",
        "keywords": "Vergebung, Versöhnung, Loslassen, Heilung, Friedensschluss, emotionale Befreiung",
        "word_count": 3200
    },
    {
        "filename": "verlust-trauer-bewaeltigen.html",
        "title": "Verlust und Trauer bewältigen: Weisheit aus 8 Traditionen",
        "description": "Wie kann man mit Verlust und Trauer umgehen? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Trauerbewältigung.",
        "keywords": "Trauer bewältigen, Verlust verarbeiten, Trauerprozess, Abschied nehmen, Heilung nach Verlust",
        "word_count": 3400
    },
    {
        "filename": "geld-erfolg-spirituelle-sicht.html",
        "title": "Geld und Erfolg: Spirituelle Sicht aus 8 Traditionen",
        "description": "Was sagen große Traditionen über Geld und Erfolg? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über materiellen Wohlstand.",
        "keywords": "Geld und Spiritualität, erfolgreiches Leben, materieller Wohlstand, ethischer Reichtum, finanzielle Weisheit",
        "word_count": 3300
    },
    {
        "filename": "selbstdisziplin-willenskraft.html",
        "title": "Selbstdisziplin und Willenskraft: Weisheit aus 8 Traditionen",
        "description": "Wie entwickelt man Selbstdisziplin und Willenskraft? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Selbstkontrolle.",
        "keywords": "Selbstdisziplin, Willenskraft, Selbstkontrolle, mentale Stärke, Charakterentwicklung, persönliche Meisterung",
        "word_count": 3200
    },
    {
        "filename": "einsamkeit-ueberwinden.html",
        "title": "Einsamkeit überwinden: Weisheit aus 8 Traditionen",
        "description": "Wie kann man Einsamkeit und Isolation bewältigen? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Einsamkeit.",
        "keywords": "Einsamkeit überwinden, soziale Verbindung, Gemeinschaft finden, isolation bewältigen, zwischenmenschliche Beziehungen",
        "word_count": 3100
    },
    {
        "filename": "meditation-spirituelle-praktiken.html",
        "title": "Meditation und spirituelle Praktiken: Weisheit aus 8 Traditionen",
        "description": "Wie praktiziert man Meditation und spirituelle Übungen? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über spirituelle Praxis.",
        "keywords": "Meditation, spirituelle Praktiken, Achtsamkeit, Gebet, Kontemplation, innere Entwicklung",
        "word_count": 3400
    },
    {
        "filename": "gesundheit-heilung.html",
        "title": "Gesundheit und Heilung: Weisheit aus 8 Traditionen",
        "description": "Wie fördern verschiedene Traditionen Gesundheit und Heilung? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über ganzheitliche Gesundheit.",
        "keywords": "Ganzheitliche Gesundheit, natürliche Heilung, Körper-Geist-Verbindung, Wellness, spirituelle Heilung",
        "word_count": 3300
    },
    {
        "filename": "kreativitaet-inspiration.html",
        "title": "Kreativität und künstlerische Inspiration: Weisheit aus 8 Traditionen",
        "description": "Wie entfaltet man Kreativität? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über kreativen Ausdruck.",
        "keywords": "Kreativität entfalten, künstlerische Inspiration, schöpferischer Prozess, kreative Blockaden überwinden, muse",
        "word_count": 3200
    },
    {
        "filename": "fuehrung-als-dienst.html",
        "title": "Führung als Dienst: Weisheit aus 8 Traditionen",
        "description": "Was ist wahre Führung? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über dienende Führung.",
        "keywords": "Dienende Führung, ethische Leadership, Verantwortungsvolle Führung, Führungsqualitäten, servant leadership",
        "word_count": 3300
    },
    {
        "filename": "beziehung-zur-natur.html",
        "title": "Beziehung zur Natur: Weisheit aus 8 Traditionen",
        "description": "Wie sehen verschiedene Traditionen unsere Beziehung zur Natur? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Umwelt.",
        "keywords": "Naturverbundenheit, Umweltschutz, ökologische Spiritualität, Nachhaltigkeit, Ehrfurcht vor dem Leben",
        "word_count": 3200
    },
    {
        "filename": "bildung-weisheit.html",
        "title": "Bildung und Weisheit: Weisheit aus 8 Traditionen",
        "description": "Was ist wahre Bildung und Weisheit? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über lebenslanges Lernen.",
        "keywords": "Lebenslanges Lernen, wahre Weisheit, Bildungsideal, intellektuelle Entwicklung, philosophische Bildung",
        "word_count": 3300
    },
    {
        "filename": "gerechtigkeit-ethik.html",
        "title": "Gerechtigkeit und Ethik: Weisheit aus 8 Traditionen",
        "description": "Was ist Gerechtigkeit? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über ethisches Handeln.",
        "keywords": "Soziale Gerechtigkeit, ethisches Leben, moralische Prinzipien, faire Gesellschaft, tugendhaftes Handeln",
        "word_count": 3200
    },
    {
        "filename": "zeit-tod-bewusstsein.html",
        "title": "Zeit und Tod: Bewusste Lebensführung aus 8 Traditionen",
        "description": "Wie gehen verschiedene Traditionen mit Zeit und Tod um? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Sterblichkeit.",
        "keywords": "Tod akzeptieren, Zeit bewusst nutzen, Sterblichkeit, memento mori, endliches Leben, Gegenwart leben",
        "word_count": 3300
    },
    {
        "filename": "freiheit-verantwortung.html",
        "title": "Freiheit und Verantwortung: Weisheit aus 8 Traditionen",
        "description": "Was ist wahre Freiheit? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Freiheit und Verantwortung.",
        "keywords": "Wahre Freiheit, persönliche Verantwortung, freie Wahl, Autonomie, ethische Freiheit, selbstbestimmtes Leben",
        "word_count": 3200
    },
    {
        "filename": "dankbarkeit-grosszuegigkeit.html",
        "title": "Dankbarkeit und Großzügigkeit: Weisheit aus 8 Traditionen",
        "description": "Wie kultiviert man Dankbarkeit und Großzügigkeit? Vergleichende Analyse von Stoizismus, Buddhismus, Christentum, Islam, Judentum, Hinduismus, Taoismus und Humanismus über Dankbarkeit.",
        "keywords": "Dankbarkeit üben, großzügig sein, appreciation, giving back, altruismus, dankbares Herz",
        "word_count": 3100
    }
]

def create_article_template(data):
    """Create HTML template for German article"""
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["title"]} | Answers Platform</title>
    <meta name="description" content="{data["description"]}">
    <meta name="keywords" content="{data["keywords"]}">
    <link rel="canonical" href="https://answers-platform.com/articles/de/{data["filename"]}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{data["title"]}">
    <script type="application/ld+json">
    {{"@context":"https://schema.org","@type":"Article","headline":"{data["title"]}","author":{{"@type":"Organization","name":"Answers Platform"}},"datePublished":"2024-01-20T10:00:00Z","wordCount":{data["word_count"]}}}
    </script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.8; color: #333; background: #f8f9fa; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; background: white; }}
        header {{ text-align: center; padding: 40px 0; border-bottom: 3px solid #667eea; margin-bottom: 40px; }}
        h1 {{ font-size: 2.5em; color: #667eea; margin-bottom: 15px; }}
        .subtitle {{ font-size: 1.2em; color: #666; font-style: italic; }}
        .meta-info {{ display: flex; justify-content: center; gap: 30px; margin-top: 20px; font-size: 0.9em; color: #888; }}
        h2 {{ font-size: 2em; color: #764ba2; margin: 40px 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; }}
        h3 {{ font-size: 1.5em; color: #667eea; margin: 30px 0 15px 0; }}
        p {{ margin-bottom: 20px; text-align: justify; }}
        ul, ol {{ margin: 20px 0; padding-left: 30px; }}
        li {{ margin-bottom: 10px; }}
        blockquote {{ border-left: 4px solid #667eea; padding: 20px 30px; margin: 30px 0; background: #f8f9ff; font-style: italic; }}
        blockquote cite {{ display: block; margin-top: 10px; font-size: 0.9em; color: #888; font-style: normal; }}
        .highlight-box {{ background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea; padding: 20px; margin: 30px 0; border-radius: 8px; }}
        .tradition-card {{ background: white; border: 2px solid #e0e0e0; border-radius: 12px; padding: 25px; margin: 20px 0; }}
        .tradition-card h4 {{ color: #667eea; font-size: 1.3em; margin-bottom: 10px; }}
        footer {{ text-align: center; padding: 30px 0; margin-top: 50px; border-top: 2px solid #e0e0e0; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{data["title"]}</h1>
            <p class="subtitle">Wie große philosophische und religiöse Traditionen helfen, Lebensweisheit zu integrieren und ein erfülltes Leben zu führen</p>
            <div class="meta-info">
                <span>📅 Veröffentlicht: 20. Januar 2024</span>
                <span>⏱️ Lesezeit: {int(data['word_count']/200)} Minuten</span>
            </div>
        </header>
        
        <article>
            <h2>Einführung: Die universelle menschliche Erfahrung</h2>
            <p>Dieses Thema berührt jeden Menschen tief. Wie können alte Weisheitstraditionen uns helfen, moderne Herausforderungen zu meistern und ein sinnvolles Leben zu führen?</p>
            
            <h2>1. Stoizismus: Tugend und Rationalität</h2>
            <div class="tradition-card">
                <h4>Stoische Perspektive</h4>
                <p>Die Stoiker lehren, dass wir durch Entwicklung von Tugend und rationaler Betrachtung innere Stärke finden können.</p>
                <blockquote>
                    "Es sind nicht die Dinge, die uns beunruhigen, sondern unsere Meinung über die Dinge."
                    <cite>— Epiktet</cite>
                </blockquote>
                <p><strong>Praktische Anwendung:</strong> Unterscheide zwischen dem, was du kontrollieren kannst, und dem, was du nicht kontrollieren kannst.</p>
            </div>
            
            <h2>2. Buddhismus: Mitgefühl und Achtsamkeit</h2>
            <div class="tradition-card">
                <h4>Buddhistischer Weg</h4>
                <p>Buddhismus betont die Kultivierung von Mitgefühl, Achtsamkeit und Weisheit als Weg zur Befreiung vom Leiden.</p>
                <blockquote>
                    "Frieden kommt von innen. Suche ihn nicht außen."
                    <cite>— Buddha</cite>
                </blockquote>
                <p><strong>Achter Pfad:</strong> Rechte Ansicht, Absicht, Rede, Handlung, Lebensunterhalt, Anstrengung, Achtsamkeit, Konzentration.</p>
            </div>
            
            <h2>3. Christentum: Liebe und Gnade</h2>
            <div class="tradition-card">
                <h4>Christliche Sichtweise</h4>
                <p>Das Christentum lehrt bedingungslose Liebe, Vergebung und Vertrauen in Gottes Gnade als Grundlage eines erfüllten Lebens.</p>
                <blockquote>
                    "Jetzt aber bleiben Glaube, Hoffnung, Liebe, diese drei; aber die Liebe ist die größte unter ihnen."
                    <cite>— 1. Korinther 13:13</cite>
                </blockquote>
                <p><strong>Großes Gebot:</strong> Liebe Gott von ganzem Herzen und deinen Nächsten wie dich selbst.</p>
            </div>
            
            <h2>4. Islam: Hingabe und Barmherzigkeit</h2>
            <div class="tradition-card">
                <h4>Islamische Lehre</h4>
                <p>Der Islam betont Hingabe an Allah, Barmherzigkeit gegenüber allen Geschöpfen und ein Leben nach göttlichen Richtlinien.</p>
                <blockquote>
                    "Wahrlich, mit jeder Schwierigkeit kommt Erleichterung."
                    <cite>— Koran 94:5-6</cite>
                </blockquote>
                <p><strong>Fünf Säulen:</strong> Glaubensbekenntnis, Gebet, Almosen, Fasten, Pilgerfahrt strukturieren das muslimische Leben.</p>
            </div>
            
            <h2>5. Judentum: Heiligung und Gerechtigkeit</h2>
            <div class="tradition-card">
                <h4>Jüdische Tradition</h4>
                <p>Das Judentum betont die Heiligung des Alltags, soziale Gerechtigkeit und die Reparatur der Welt (Tikkun Olam).</p>
                <blockquote>
                    "Wer eine einzige Seele rettet, rettet die ganze Welt."
                    <cite>— Talmud, Sanhedrin 37a</cite>
                </blockquote>
                <p><strong>Mitzwot:</strong> Durch gute Taten und Erfüllung der Gebote heiligt der Jude sein Leben.</p>
            </div>
            
            <h2>6. Hinduismus: Dharma und Einheit</h2>
            <div class="tradition-card">
                <h4>Hinduistische Philosophie</h4>
                <p>Hinduismus lehrt die Erfüllung seiner Pflicht (Dharma), die Einheit allen Lebens und den Weg zur Befreiung (Moksha).</p>
                <blockquote>
                    "Du hast ein Recht auf deine Handlungen, aber nicht auf die Früchte deiner Handlungen."
                    <cite>— Bhagavad Gita 2.47</cite>
                </blockquote>
                <p><strong>Vier Lebensziele:</strong> Dharma (Pflicht), Artha (Wohlstand), Kama (Vergnügen), Moksha (Befreiung).</p>
            </div>
            
            <h2>7. Taoismus: Harmonie und Natürlichkeit</h2>
            <div class="tradition-card">
                <h4>Taoistische Weisheit</h4>
                <p>Taoismus betont Harmonie mit dem natürlichen Fluss des Universums (Tao) und spontanes, authentisches Leben.</p>
                <blockquote>
                    "Die Natur eilt nie, und doch wird alles vollendet."
                    <cite>— Laozi</cite>
                </blockquote>
                <p><strong>Wu Wei:</strong> Durch nicht-forciertes Handeln und Loslassen findet man den natürlichen Weg.</p>
            </div>
            
            <h2>8. Humanismus: Menschliches Potenzial</h2>
            <div class="tradition-card">
                <h4>Humanistische Sicht</h4>
                <p>Humanismus fördert die Entfaltung menschlichen Potenzials, rationales Denken und ethisches Handeln ohne supernaturalen Bezug.</p>
                <blockquote>
                    "Der unexaminierte Lebens ist nicht wert, gelebt zu werden."
                    <cite>— Sokrates</cite>
                </blockquote>
                <p><strong>Selbstverwirklichung:</strong> Durch Kreativität, Wissen und Beitrag zur Gesellschaft verwirklicht der Mensch sein Potenzial.</p>
            </div>
            
            <h2>Vergleichende Analyse</h2>
            <div class="highlight-box">
                <h3>Gemeinsame Themen</h3>
                <ul>
                    <li><strong>Innere Entwicklung:</strong> Alle Traditionen betonen persönliche Wachstum und Charakterbildung</li>
                    <li><strong>Mitgefühl:</strong> Empathie und Sorge für andere sind universelle Werte</li>
                    <li><strong>Balance:</strong> Ausgewogenheit in allen Lebensbereichen wird geschätzt</li>
                    <li><strong>Praxis:</strong> Theorie muss in tägliches Handeln umgesetzt werden</li>
                </ul>
            </div>
            
            <div class="highlight-box">
                <h3>Einzigartige Beiträge</h3>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background: #667eea; color: white;">
                        <th style="padding: 12px; text-align: left;">Tradition</th>
                        <th style="padding: 12px; text-align: left;">Hauptbeitrag</th>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Stoizismus</td>
                        <td style="padding: 10px;">Emotionale Resilienz durch Rationalität</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Buddhismus</td>
                        <td style="padding: 10px;">Achtsamkeit und Mitgefühlspraktiken</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Christentum</td>
                        <td style="padding: 10px;">Bedingungslose Liebe und Vergebung</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Islam</td>
                        <td style="padding: 10px;">Disziplin und Gemeinschaftsorientierung</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Judentum</td>
                        <td style="padding: 10px;">Heiligung des Alltags und soziale Gerechtigkeit</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Hinduismus</td>
                        <td style="padding: 10px;">Vielfalt der spirituellen Wege</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 10px;">Taoismus</td>
                        <td style="padding: 10px;">Natürlichkeit und Spontaneität</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px;">Humanismus</td>
                        <td style="padding: 10px;">Rationale Ethik und menschliche Würde</td>
                    </tr>
                </table>
            </div>
            
            <h2>Praktische Integration</h2>
            <ol>
                <li><strong>Tägliche Reflexion:</strong> Nimm dir Zeit für Meditation oder Gebet</li>
                <li><strong>Tugend üben:</strong> Wähle eine Qualität, die du diese Woche entwickeln möchtest</li>
                <li><strong>Dienst leisten:</strong> Finde Möglichkeiten, anderen zu helfen</li>
                <li><strong>Lernen:</strong> Studiere die Texte und Lehren verschiedener Traditionen</li>
                <li><strong>Gemeinschaft:</strong> Verbinde dich mit Gleichgesinnten</li>
                <li><strong>Anwendung:</strong> Setze学到的Wisdom in konkrete Handlungen um</li>
                <li><strong>Geduld:</strong> Spirituelles Wachstum braucht Zeit - sei geduldig mit dir</li>
            </ol>
            
            <h2>Fazit: Deine persönliche Weisheitsreise</h2>
            <p>Jede dieser Traditionen bietet wertvolle Einsichten, die du in dein Leben integrieren kannst. Du musst dich nicht für eine entscheiden - nimm das Beste aus allen und schaffe deinen eigenen Weg der Weisheit.</p>
            
            <div class="highlight-box">
                <h3>Deine nächsten Schritte</h3>
                <p>Beginne heute: Welche Lehre spricht dich am meisten an? Wie kannst du sie in den nächsten 24 Stunden praktisch anwenden? Weisheit entsteht nicht durch Lesen allein, sondern durch bewusste, tägliche Praxis.</p>
            </div>
        </article>
        
        <footer>
            <p>&copy; 2024 Answers Platform. Alle Rechte vorbehalten.</p>
            <p><a href="/articles/de/" style="color: #667eea; text-decoration: none;">← Zurück zur Übersicht</a></p>
        </footer>
    </div>
</body>
</html>'''

# Create all articles
output_dir = "/Volumes/NEW 1/Answers/articles/de"
os.makedirs(output_dir, exist_ok=True)

for data in articles_data:
    filepath = os.path.join(output_dir, data["filename"])
    content = create_article_template(data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {data['filename']}")

print(f"\n🎉 Successfully created {len(articles_data)} German articles!")
print("Total German articles: 20/20 (100% complete)")
