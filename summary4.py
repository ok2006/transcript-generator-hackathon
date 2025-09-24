from transformers import pipeline

text = """
TCP/IP is the most widely used protocol suite. 
It has four layers: Application, Transport, Internet, and Network. 
Each layer has its own function, and together they enable reliable communication over the internet.
"""

summarizer = pipeline("summarization", model="t5-base")

def summarize(text):
    return summarizer("summarize: " + text, 
                      max_length=80, min_length=20, do_sample=False)[0]['summary_text']

print(summarize(text))
