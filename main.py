import newspaper as nw
from gtts import gTTS
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

class TextSource(ABC):
    @abstractmethod
    def get_text(self) -> None:
        """
        Abstract method to retrieve text from different sources.

        Returns:
            str: The extracted text.
        """
        pass

class FileTextSource(TextSource):
    def __init__(self, filename):
        self.filename = filename
    
    def get_text(self):
        """
        Reads text from a file.

        Returns:
            str: The text content of the file.
        """
        try:
            with open(self.filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            messagebox.showerror("","File not found")
            return ""
        
class UrlTextSource(TextSource):
    def __init__(self, url):
        self.url = url
    
    def get_text(self):
        """
        Extracts text from a given URL.

        Returns:
            str: The extracted text from the webpage.
        """
        try:
            article = nw.Article(self.url)
            article.download()
            article.parse()
            return article.text
        except Exception:
            messagebox.showerror("",f"Failed to fetch URL: {Exception}")
            return ""

class HandmadeTextSource(TextSource):
    def __init__(self, text):
        self.text = text

    def get_text(self):
        """
        Returns the provided text.

        Returns:
            str: The provided text.
        """
        return self.text
    
class TextSave(ABC):
    @abstractmethod
    def text_save(self, txtname: str, text: str) -> None:
        """
        Abstract method to save text to a file.

        Args:
            txtname (str): The name of the output file.
            text (str): The text to be saved.
        """
        pass

class TextSaveTXT(TextSave):
    def text_save(self, txtname, text):
        """
        Saves text to a TXT file.

        Args:
            txtname (str): The name of the output file.
            text (str): The text to be saved.
        """
        try:
            with open(txtname + ".txt", "w+") as f:
                f.write(text)
        except Exception:
            messagebox.showerror("", f"Failed to save text: {Exception}")

class AudioProcessor(ABC):
    @abstractmethod
    def process_audio(self, output_file: str, textSource: str) -> None:
        """
        Abstract method to process and save audio.

        Args:
            output_file (str): The name of the output audio file.
            textSource (str): The text to convert to speech.
        """
        pass

class Español(AudioProcessor):
    def process_audio(self, output_file, textSource):
        """
        Processes and saves audio.

        Args:
            output_file (str): The name of the output audio file.
            textSource (str): The text to convert to speech.
        """
        audio = gTTS(text=textSource, lang="es", slow=False)
        audio.save(f"{output_file}.mp3")

class English(AudioProcessor):
    def process_audio(self, output_file, textSource):
        """
        Processes and saves audio.

        Args:
            output_file (str): The name of the output audio file.
            textSource (str): The text to convert to speech.
        """
        audio = gTTS(text=textSource, lang="en", slow=False)
        audio.save(f"{output_file}.mp3")

class Français(AudioProcessor):
    def process_audio(self, output_file, textSource):
        """
        Processes and saves audio.

        Args:
            output_file (str): The name of the output audio file.
            textSource (str): The text to convert to speech.
        """
        audio = gTTS(text=textSource, lang="fr", slow=False)
        audio.save(f"{output_file}.mp3")

class AppTextSpeech(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text to Speech Converter")
        self.config(background="lightgreen")
        self.create_widgets()
        
    def create_widgets(self):
        """
            Creates the widgets of the application
        """
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", background="green", foreground="white")

        self.option_label = ttk.Label(text="Choose an option to convert:", background="lightgreen")
        self.option_label.pack(padx=10,pady=10)
        self.option_var = tk.StringVar() 
        self.option_combobox = ttk.Combobox(textvariable=self.option_var, values=["File name", "URL", "Text"])
        self.option_combobox.pack(padx=10,pady=(0,10))

        self.input_text_label = ttk.Label(text="Introduce your file name, url or text:", background="lightgreen")
        self.input_text_label.pack(padx=10,pady=10)
        self.input_text = scrolledtext.ScrolledText(height=3, width=30)
        self.input_text.pack(padx=10,pady=(0,10))

        self.language_label = ttk.Label(text="Choose the language:", background="lightgreen")
        self.language_label.pack(padx=10,pady=10)
        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(textvariable=self.language_var, values=["Español", "English", "Français"])
        self.language_combobox.pack(padx=10,pady=(0,10))

        self.mp3file = ttk.Label(text="Insert name of the audio file:", background="lightgreen")
        self.mp3file.pack(padx=10,pady=10)
        self.input_mp3file = ttk.Entry()
        self.input_mp3file.pack(padx=10,pady=(0,10))

        self.filename = ttk.Label(text="Insert name of the file to save text:", background="lightgreen")
        self.filename.pack(padx=10,pady=10)
        self.input_filename = ttk.Entry()
        self.input_filename.pack(padx=10,pady=(0,10))

        self.convert_button = ttk.Button(text="Convert", command=self.app_funcionality)
        self.convert_button.pack(padx=10, pady=20)

    def app_funcionality(self):
        """
            Sets de funcionality of the application
        """
        if self.option_combobox.get() == "File name":
            filetxt = FileTextSource(self.input_text.get("1.0", "end").strip())
        elif self.option_combobox.get() == "URL":
            filetxt = UrlTextSource(self.input_text.get("1.0", "end").strip())
        elif self.option_combobox.get() == "Text":
            filetxt = HandmadeTextSource(self.input_text.get("1.0", "end").strip())
        else:
            messagebox.showerror(" ","Choose type of convert.")
        
        if self.input_mp3file.get():
            if self.language_combobox.get() == "Español":
                audio = Español()
            elif self.language_combobox.get() == "English":
                audio = English()
            elif self.language_combobox.get() == "Français":
                audio = Français()
            else:
                messagebox.showerror(" ","Insert audio language.")
                return
            audio.process_audio(self.input_mp3file.get(), filetxt.get_text())
            messagebox.showinfo("Success", "Audio created successfully!")
        else:
            messagebox.showerror(" ", "Insert audio file name.")
        
        if self.input_filename.get():
            save_text = TextSaveTXT()
            save_text.text_save(self.input_filename.get(), filetxt.get_text())
        

if __name__ == "__main__":
    app = AppTextSpeech()
    app.mainloop()