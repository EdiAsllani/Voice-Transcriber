import customtkinter as ctk
import tkinter
import os
from main import transcribe_audio, initialize_model, select_audio_file, record_audio

# Global variables
model = None
selected_file = None

# Initialize main window
root = ctk.CTk()
root.title("Transcriber")
root.geometry("800x350")  # Made wider to accommodate both panels
ctk.set_appearance_mode("dark")

# Define fonts - Consolas for text, Segoe UI for UI elements
button_font = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
label_font = ctk.CTkFont(family="Segoe UI", size=13)
text_font = ctk.CTkFont(family="Consolas", size=13)  # Consolas for transcription text
title_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
status_font = ctk.CTkFont(family="Segoe UI", size=13)

input_frame = ctk.CTkFrame(root, width=200)  # Set fixed width
input_frame.pack(side="left", padx=(20, 10), pady=20)
input_frame.pack_propagate(False)  # Prevent frame from shrinking to fit contents

# Create transcription display frame (right side)
display_frame = ctk.CTkFrame(root)
display_frame.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

# Add title label for transcription area
transcription_title = ctk.CTkLabel(display_frame, text="Transcription Results", font=title_font)
transcription_title.pack(pady=(10, 5))

# Create the large text area for transcriptions
transcription_textbox = ctk.CTkTextbox(
    display_frame, 
    width=400, 
    height=300,
    font=text_font,
    wrap="word"
)
transcription_textbox.pack(fill="both", expand=True, padx=10, pady=5)

# Clear button for transcription area
clear_btn = ctk.CTkButton(
    display_frame,
    text="Clear Text",
    text_color="#FFECCC",
    fg_color="#511D43",
    font=button_font,
    command=lambda: transcription_textbox.delete("1.0", "end")
)
clear_btn.pack(pady=(5, 10))

# Record button with functionality
def record_and_transcribe():
    global model
    
    # Initialize model if not already done
    if model is None:
        update_loading_animation()
        root.update()
        
        try:
            model = initialize_model()
            stop_loading_animation()
            
            if model is None:
                status_label.configure(text="❌ Failed to load model")
                return
        except Exception as e:
            stop_loading_animation()
            status_label.configure(text=f"❌ Model error: {str(e)[:20]}...")
            return
    
    # Get recording duration from combobox
    duration_text = combobox.get()
    duration = int(duration_text.split()[0])  # Extract number from "5 seconds"
    
    status_label.configure(text=f"🎤 Recording for {duration}s...")
    root.update()
    
    try:
        # Record audio
        audio_file = record_audio(duration)
        if not audio_file:
            status_label.configure(text="❌ Recording failed")
            return
        
        status_label.configure(text="🔄 Transcribing...")
        root.update()
        
        # Transcribe audio
        text, language = transcribe_audio(model, audio_file)
        
        # Clean up temporary file
        try:
            os.unlink(audio_file)
        except:
            pass
        
        if text:
            # Display transcription in textbox
            transcription_textbox.insert("end", f"[Recording - {language}]\n{text}\n\n")
            transcription_textbox.see("end")  # Scroll to bottom
            status_label.configure(text="✅ Recording transcribed")
        else:
            status_label.configure(text="❌ Transcription failed")
            
    except Exception as e:
        status_label.configure(text=f"❌ Error: {str(e)[:15]}...")

rec_btn = ctk.CTkButton(
    input_frame, 
    text="Record", 
    text_color="#FFECCC", 
    fg_color="#511D43",
    width=160, height=40,
    font=button_font,
    command=record_and_transcribe
)
rec_btn.grid(row=0, column=0, padx=10, pady=10)

# Combobox for recording duration
def combobox_callback(choice):
    print("combobox dropdown clicked", choice)

combobox = ctk.CTkComboBox(
    input_frame, 
    values=["5 seconds", "15 seconds", "30 seconds", "60 seconds"],
    width=160, height=40,
    font=label_font,
    command=combobox_callback
)
combobox.set("5 seconds")
combobox.grid(row=0, column=1, padx=10, pady=10)

input_frame.grid_rowconfigure(1, minsize=15)

# Status label
status_label = ctk.CTkLabel(input_frame, text="Ready", width=160, height=40, font=status_font)
status_label.grid(row=2, column=1, padx=10, pady=10)

# Loading animation variables
loading_dots = 0
loading_timer = None

def update_loading_animation():
    global loading_dots, loading_timer
    loading_dots = (loading_dots % 3) + 1
    dots = "." * loading_dots
    status_label.configure(text=f"Loading model{dots}")
    loading_timer = root.after(200, update_loading_animation)

def stop_loading_animation():
    global loading_timer
    if loading_timer:
        root.after_cancel(loading_timer)
        loading_timer = None

# Updated file selection and transcription function
def select_and_transcribe():
    global model
    
    # Initialize model if not already done
    if model is None:
        update_loading_animation()
        root.update()
        
        try:
            model = initialize_model()
            stop_loading_animation()
            
            if model is None:
                status_label.configure(text="❌ Failed to load model")
                return
        except Exception as e:
            stop_loading_animation()
            status_label.configure(text=f"❌ Model error: {str(e)[:20]}...")
            return
    
    # Select file
    file_path = select_audio_file()
    
    if file_path:
        filename = os.path.basename(file_path)
        status_label.configure(text=f"Transcribing: {filename[:15]}...")
        root.update()
        
        try:
            # Use transcribe_audio instead of transcribe_file to get the text
            text, language = transcribe_audio(model, file_path)
            
            if text:
                # Display transcription in textbox
                transcription_textbox.insert("end", f"[{filename} - {language}]\n{text}\n\n")
                transcription_textbox.see("end")  # Scroll to bottom
                status_label.configure(text=f"✅ Done: {filename[:15]}...")
            else:
                status_label.configure(text=f"❌ Failed: {filename[:15]}...")
                
        except Exception as e:
            status_label.configure(text=f"❌ Error: {str(e)[:15]}...")
    else:
        status_label.configure(text="No file selected")

# Import file button
file_btn = ctk.CTkButton(
    input_frame, 
    text="Import File", 
    text_color="#FFECCC", 
    fg_color="#511D43",
    width=160, height=40,
    font=button_font,
    command=select_and_transcribe
)
file_btn.grid(row=2, column=0, padx=10, pady=10)

# Display button (optional - you can remove this if not needed)
def show_transcription_area():
    # This could toggle visibility or do something else
    pass

# Run the app
def main():
    """Main function to start the GUI application"""
    root.mainloop()

if __name__ == "__main__":
    main()
