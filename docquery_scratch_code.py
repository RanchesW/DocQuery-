from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import re
import tkinter as tk

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\BOSuser\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_path):
    img = Image.open(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text


def find_answer_in_text(text, question):
    key_phrase = question.replace('What is the', '').replace('?', '').strip().lower()
    
    pattern = re.compile(re.escape(key_phrase) + r'\s*[:\-]?\s*([\w\s\-\/]+)', re.IGNORECASE)
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    else:
        if 'date' in key_phrase:
            date_pattern = r'\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})\b'
            dates = re.findall(date_pattern, text)
            if dates:
                return ', '.join(dates)
        return "Answer not found."

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        extension = file_path.split('.')[-1].lower()
        if extension in ['jpg', 'jpeg', 'png']:
            text = extract_text_from_image(file_path)
        elif extension == 'pdf':
            text = extract_text_from_pdf(file_path)
        else:
            messagebox.showerror("Unsupported file", "This file type is not supported")
            return
        text_output.delete('1.0', tk.END)
        text_output.insert(tk.END, text)

def query():
    question = question_entry.get()
    text = text_output.get("1.0", tk.END)
    answer = find_answer_in_text(text, question)
    answer_output.delete('1.0', tk.END)
    answer_output.insert(tk.END, answer)


root = tk.Tk()
root.title("Document Query System")

load_button = tk.Button(root, text="Load Document", command=load_file)
load_button.pack(pady=20)

question_label = tk.Label(root, text="Enter your question:")
question_label.pack()

question_entry = tk.Entry(root, width=50)
question_entry.pack()

query_button = tk.Button(root, text="Submit Query", command=query)
query_button.pack(pady=10)

answer_label = tk.Label(root, text="Answer:")
answer_label.pack()

answer_output = tk.Text(root, height=1, width=50)
answer_output.pack(pady=20)

text_output = tk.Text(root, height=10, width=50)  
text_output.pack(pady=20)

root.mainloop()
