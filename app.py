import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import langid

# تحديد اللغات المطلوبة
langid.set_languages(['ar', 'en'])

# Test English
text1 = "This is an English sentence."
print("English:", langid.classify(text1))

# Test Arabic
text2 = "هذه جملة باللغة العربية."
print("Arabic:", langid.classify(text2))


import langid
import pandas as pd

langid.set_languages(['ar', 'en'])

sentences = [
    "Artificial Intelligence is changing the world.",
    "الذكاء الاصطناعي بيغير العالم.",
    "Machine Learning is a part of AI."
]

results = []

for sentence in sentences:
    language, score = langid.classify(sentence)

    results.append({
        "Text": sentence,
        "Language": language,
        "Score": score
    })

df = pd.DataFrame(results)

print(df.head(10))

for sentence in sentences:
    language, confidence = langid.classify(sentence)

    print("Text:", sentence)
    print("Language:", language)
    print("Score:", confidence)
    print("-" * 40)



import langid

langid.set_languages(['ar', 'en'])

results = []

for sentence in sentences:
    language, score = langid.classify(sentence)

   

langid.set_languages(['ar', 'en'])

results = []

for sentence in sentences:
    language, score = langid.classify(sentence)

    results.append({
        "Text": sentence,
        "Language": language,
        "Score": score
    })

df = pd.DataFrame(results)

print(df.head(10))

df['Word_Count'] = df['Text'].apply(lambda x: len(x.split()))

language_counts = df.groupby('Language')['Word_Count'].sum()

total_words = language_counts.sum()

language_percentage = (language_counts / total_words) * 100

summary = pd.DataFrame({
    'Word_Count': language_counts,
    'Percentage': language_percentage
})

print(summary)

import matplotlib.pyplot as plt

plt.figure(figsize=(7, 7))

plt.pie(
    summary['Word_Count'],
    labels=summary.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=['#FF69B4', '#87CEEB']
)

plt.title('Language Distribution in PDF')
plt.show()

print("Total Words:", total_words)

print("\nLanguage Distribution:")
print(summary)

print("\nNumber of Sentences:", len(df))

arabic_percentage = summary.loc['ar', 'Percentage'] if 'ar' in summary.index else 0

english_percentage = summary.loc['en', 'Percentage'] if 'en' in summary.index else 0

if arabic_percentage == 100:
    result = "Arabic"

elif english_percentage == 100:
    result = "English"

else:
    result = "Mixed"

print("PDF Language:", result)

import matplotlib.pyplot as plt

plt.figure(figsize=(7, 5))

colors = {
    'ar': '#FF69B4',
    'en': '#87CEEB'
}

plt.bar(
    ['Arabic' if lang == 'ar' else 'English' for lang in summary.index],
    summary['Percentage'],
    color=[colors[lang] for lang in summary.index]
)

plt.title('PDF Language Distribution')
plt.xlabel('Language')
plt.ylabel('Percentage (%)')

plt.ylim(0, 100)

for i, value in enumerate(summary['Percentage']):
    plt.text(i, value + 1, f'{value:.2f}%', ha='center')

plt.show()



import gradio as gr
import fitz
import langid
import pandas as pd
import matplotlib.pyplot as plt
import re

# تحديد اللغات
langid.set_languages(['ar', 'en'])


# Main Function
def analyze_pdf(file_path):

    if file_path is None:
        return "Please upload a PDF file.", None

    # 1. Extract text from PDF
    doc = fitz.open(file_path)

    full_text = ""

    for page in doc:
        full_text += page.get_text() + "\n"

    doc.close()

    if not full_text.strip():
        return "No readable text found in this PDF.", None

    # 2. Split text into sentences
    sentences = re.split(r'(?<=[.!؟?])\s+', full_text)

    sentences = [s.strip() for s in sentences if s.strip()]

    # 3. Detect language
    results = []

    for sentence in sentences:

        language, score = langid.classify(sentence)

        results.append({
            "Text": sentence,
            "Language": language,
            "Score": score
        })

    df = pd.DataFrame(results)

    # 4. Count words
    df['Word_Count'] = df['Text'].apply(
        lambda x: len(x.split())
    )

    # 5. Calculate language percentages
    language_counts = df.groupby('Language')['Word_Count'].sum()

    language_counts = language_counts.reindex(
        ['ar', 'en'], fill_value=0
    )

    total_words = language_counts.sum()

    if total_words == 0:
        return "No words found in PDF.", None

    language_percentage = (
        language_counts / total_words
    ) * 100

    summary = pd.DataFrame({
        'Word_Count': language_counts,
        'Percentage': language_percentage
    })

    # 6. Determine PDF language
    arabic_percentage = summary.loc['ar', 'Percentage']
    english_percentage = summary.loc['en', 'Percentage']

    if arabic_percentage == 100:
        result = "Arabic"

    elif english_percentage == 100:
        result = "English"

    else:
        result = "Mixed"

    # 7. Generate report
    report = f"""
PDF LANGUAGE DETECTOR
=====================

Final Result: {result}

Arabic:
Word Count: {language_counts['ar']}
Percentage: {arabic_percentage:.2f}%

English:
Word Count: {language_counts['en']}
Percentage: {english_percentage:.2f}%

Total Words: {total_words}

Total Sentences: {len(df)}
"""

    # 8. Generate chart
    fig, ax = plt.subplots(figsize=(7, 5))

    languages = ['Arabic', 'English']

    percentages = [
        arabic_percentage,
        english_percentage
    ]

    colors = ['#FF69B4', '#87CEEB']

    ax.bar(
        languages,
        percentages,
        color=colors
    )

    ax.set_title('PDF Language Distribution')
    ax.set_xlabel('Language')
    ax.set_ylabel('Percentage (%)')
    ax.set_ylim(0, 110)

    for i, value in enumerate(percentages):
        ax.text(
            i,
            value + 1,
            f'{value:.2f}%',
            ha='center'
        )

    plt.tight_layout()

    return report, fig


# 9. Create Gradio Interface
demo = gr.Interface(

    fn=analyze_pdf,

    inputs=gr.File(
        label="Upload Your PDF",
        file_types=[".pdf"],
        type="filepath"
    ),

    outputs=[
        gr.Textbox(
            label="Analysis Report",
            lines=12
        ),

        gr.Plot(
            label="Language Distribution"
        )
    ],

    title="PDF Language Detector",

    description=(
        "Upload a PDF file to detect Arabic "
        "and English languages automatically."
    )

)

# 10. Launch Application
demo.launch()