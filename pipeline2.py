import os
import random
import json
import spacy
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from transformers import pipeline

# 🔹 Added imports for Supabase
from supabase import create_client
from dotenv import load_dotenv

# 🔹 Load env variables
load_dotenv()
SUPABASE_URL = "https://ngguxusvlqpbizmuphkf.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#SUMMARIZER
summarizer = pipeline("summarization", model="google/pegasus-xsum", temperature=0.2)

def summarize_text(text, max_len=100, min_len=50):
    """Summarize the input text using PEGASUS."""
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']

# ---------- QUIZ GENERATOR ----------
nlp = spacy.load("en_core_web_sm")

def generate_quiz(text, num_questions=3):
    """Generate quiz questions (Fill-in-the-Blank, True/False, MCQs) from text."""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents if len(sent.text.split()) > 4]

    quizzes = []

    for sent in sentences[:num_questions]:
        doc_sent = nlp(sent)

        # --- Try entities first, fallback to nouns ---
        ents = [ent.text for ent in doc_sent.ents]
        if ents:
            keyword = ents[0]
        else:
            nouns = [tok.text for tok in doc_sent if tok.pos_ in ["NOUN", "PROPN"]]
            if not nouns:
                continue
            keyword = nouns[0]

        # --- Build distractors dynamically from other nouns/entities ---
        distractors_pool = [tok.text for tok in doc if tok.pos_ in ["NOUN", "PROPN"] and tok.text != keyword]
        distractors = random.sample(distractors_pool, min(3, len(distractors_pool))) or ["Rome", "Egypt", "Pharaoh"]

        # ---------- Fill-in-the-Blank ----------
        fb = sent.replace(keyword, "_")
        quizzes.append({"type": "fill_blank", "q": fb, "a": keyword})

        # ---------- True/False ----------
        false_sent = sent.replace(keyword, random.choice(distractors))  # smarter replacement
        quizzes.append({"type": "true_false", "q": sent, "a": True})
        quizzes.append({"type": "true_false", "q": false_sent, "a": False})

        # ---------- MCQ ----------
        options = [keyword] + distractors
        random.shuffle(options)
        quizzes.append({
            "type": "mcq",
            "q": sent.replace(keyword, "_"),
            "options": options,
            "a": keyword
        })

    return quizzes

# ---------- PIPELINE ----------
def get_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    if "embed/" in url:
        return url.split("embed/")[-1].split("?")[0]
    if "/v/" in url:
        return url.split("/v/")[-1].split("?")[0]
    return None

# 🔹 Fetch latest video from Supabase instead of input()
def get_latest_video():
    response = supabase.table("videos").select("id, source_url").order("id", desc=True).limit(1).execute()
    if response.data:
        return response.data[0]["id"], response.data[0]["source_url"]
    return None, None

if __name__ == "__main__":  # <-- FIXED THIS
    # 🔹 Get video from DB
    video_row_id, url = get_latest_video()
    if not url:
        print("⚠️ No video found in 'videos' table.")
        exit()

    video_id = get_video_id(url)
    api = YouTubeTranscriptApi()

    try:
        # Step 1: Fetch transcript
        transcript_list = api.fetch(video_id, languages=["en"])
        transcript_text = " ".join(entry.text for entry in transcript_list)

        # Save transcript
        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript_text)
        print("Transcript saved to transcript.txt ✅")

        # Step 2: Summarize
        summary = summarize_text(transcript_text, max_len=180, min_len=80)
        print("\n===== SUMMARY =====")
        print(summary)

        # Save summary as plain text
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        print("Summary saved to summary.txt ")

        # Step 3: Generate Quiz
        quiz = generate_quiz(summary, num_questions=3)
        print("\n===== QUIZ =====")
        for q in quiz:
            print(q)

        # Save quiz as JSON (for Supabase JSONB)
        with open("quiz.json", "w", encoding="utf-8") as f:
            json.dump(quiz, f, indent=4, ensure_ascii=False)
        print("\nQuiz saved to quiz.json ")

        # Save summary + quiz
        with open("quiz_output.txt", "w", encoding="utf-8") as f:
            f.write("===== SUMMARY =====\n")
            f.write(summary + "\n\n")
            f.write("===== QUIZ =====\n")
            for q in quiz:
                f.write(str(q) + "\n")
        print("\nQuiz saved to quiz_output.txt ")

        # Step 4: Save summary into summaries table
        supabase.table("summaries").insert({
            "video_id": video_row_id,
            "content": summary
        }).execute()
        print("✅ Summary inserted into 'summaries' table.")

        # Step 5: Save quiz JSON into quizzes table
        supabase.table("quizzes").insert({
            "video_id": video_row_id,
            "quiz_json": quiz   # quiz is a Python list/dict → will be stored as JSONB
        }).execute()
        print("✅ Quiz inserted into 'quizzes' table.")

    except TranscriptsDisabled:
        print("No captions available for this video.")