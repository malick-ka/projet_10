import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from turtle import width
from PIL import Image, ImageTk
import os
from projet import plates_reader, clean_plates, normalize

class PlateDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Detection System")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Header Section
        self.create_header(main_frame)
        
        # Input Section
        self.create_input_section(main_frame)
        
        # Control Section
        self.create_control_section(main_frame)
        
        # Results Section
        self.create_results_section(main_frame)
        
        # Status Bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create the header with project information and AIMS logo"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # AIMS Logo - First element, centered
        try:
            if os.path.exists('AIMS-image.jpg'):
                # Load and resize the AIMS logo
                logo_image = Image.open('AIMS-image.jpg')
                logo_image = logo_image.resize((700, 90), Image.Resampling.LANCZOS)
                self.aims_logo = ImageTk.PhotoImage(logo_image)
                
                logo_label = ttk.Label(header_frame, image=self.aims_logo)
                logo_label.pack(pady=(0, 15))
            else:
                # Fallback if image not found
                logo_label = ttk.Label(header_frame, text="🏛️ AIMS Senegal", font=('Arial', 40))
                logo_label.pack(pady=(0, 15))
        except Exception as e:
            # Fallback if PIL not available or image loading fails
            logo_label = ttk.Label(header_frame, text="🏛️ AIMS Senegal", font=('Arial', 40))
            logo_label.pack(pady=(0, 15))
        
        # Title - Second element
        title_label = ttk.Label(header_frame, text="License Plate Detection System", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 5))
        
        # Subtitle - Third element
        subtitle_label = ttk.Label(header_frame, text="AIMS Senegal - Python Project", 
                                  font=('Arial', 12))
        subtitle_label.pack(pady=(0, 5))
        
        # Group info - Fourth element
        group_label = ttk.Label(header_frame, text="Group 10", 
                               font=('Arial', 10, 'italic'))
        group_label.pack(pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
    
    def create_input_section(self, parent):
        """Create the text input section"""
        # Input label
        input_label = ttk.Label(parent, text="Enter text to analyze:", font=('Arial', 10, 'bold'))
        input_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(parent, height=8, width=70, 
                                                   font=('Arial', 10), wrap=tk.WORD)
        self.text_input.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                            pady=(0, 10))
        
        # Placeholder text
        placeholder = "Enter your text here to detect license plates...\n\nExample:\nI saw a car with plate DK-2394-T on the road.\nAnother vehicle had AB 1234 ZT as its registration."
        self.text_input.insert('1.0', placeholder)
        self.text_input.bind('<FocusIn>', self.clear_placeholder)
    
    def create_control_section(self, parent):
        """Create the control buttons section"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # Analyze button
        self.analyze_button = ttk.Button(control_frame, text="🔍 Analyze Text", 
                                        command=self.start_analysis, style='Accent.TButton')
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(control_frame, text="🗑️ Clear All", 
                                 command=self.clear_all)
        clear_button.pack(side=tk.LEFT)
        
        # Progress bar (initially hidden)
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, padx=(20, 0))
        self.progress.pack_forget()  # Hide initially
    
    def create_results_section(self, parent):
        """Create the results display section"""
        # Results label
        results_label = ttk.Label(parent, text="Analysis Results:", font=('Arial', 10, 'bold'))
        results_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(parent, height=12, width=70, 
                                                     font=('Arial', 10), wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.results_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to analyze")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, 
                              anchor=tk.W, font=('Arial', 9))
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def clear_placeholder(self, event):
        """Clear placeholder text when user clicks on input"""
        if self.text_input.get('1.0', tk.END).strip() == "Enter your text here to detect license plates...\n\nExample:\nI saw a car with plate DK-2394-T on the road.\nAnother vehicle had AB 1234 ZT as its registration.":
            self.text_input.delete('1.0', tk.END)
    
    def start_analysis(self):
        """Start the analysis in a separate thread"""
        text = self.text_input.get('1.0', tk.END).strip()
        
        if not text or text == "Enter your text here to detect license plates...\n\nExample:\nI saw a car with plate DK-2394-T on the road.\nAnother vehicle had AB 1234 ZT as its registration.":
            messagebox.showwarning("Warning", "Please enter some text to analyze!")
            return
        
        # Disable button and show progress
        self.analyze_button.config(state='disabled')
        self.progress.pack(side=tk.LEFT, padx=(20, 0))
        self.progress.start()
        self.status_var.set("Analyzing text...")
        
        # Start analysis in separate thread
        thread = threading.Thread(target=self.analyze_text, args=(text,))
        thread.daemon = True
        thread.start()
    
    def analyze_text(self, text):
        """Analyze the text for license plates"""
        try:
            # Simulate some processing time for the loader
            time.sleep(1)
            
            # Run the analysis
            plates = plates_reader(text)
            cleaned_plates = clean_plates(plates)
            normalized_plates = normalize(cleaned_plates)
            
            # Update UI in main thread
            self.root.after(0, self.display_results, plates, cleaned_plates, normalized_plates)
            
        except Exception as e:
            # Handle errors in main thread
            self.root.after(0, self.show_error, str(e))
    
    def display_results(self, original_plates, cleaned_plates, normalized_plates):
        """Display the analysis results"""
        # Stop progress and re-enable button
        self.progress.stop()
        self.progress.pack_forget()
        self.analyze_button.config(state='normal')
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        
        # Format results - Only show normalized plates
        if normalized_plates:
            results = "DETECTED LICENSE PLATES:\n\n"
            for i, plate in enumerate(normalized_plates, 1):
                results += f"{i}. {plate}\n"
        else:
            results = "No license plates found in the text.\n"
        
        # Display results
        self.results_text.insert('1.0', results)
        self.results_text.config(state=tk.DISABLED)
        
        # Update status
        self.status_var.set(f"Analysis complete - {len(normalized_plates)} plates found")
    
    def show_error(self, error_message):
        """Show error message"""
        self.progress.stop()
        self.progress.pack_forget()
        self.analyze_button.config(state='normal')
        self.status_var.set("Error occurred during analysis")
        messagebox.showerror("Error", f"An error occurred:\n{error_message}")
    
    def clear_all(self):
        """Clear all inputs and results"""
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', "Enter your text here to detect license plates...\n\nExample:\nI saw a car with plate DK-2394-T on the road.\nAnother vehicle had AB 1234 ZT as its registration.")
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        self.status_var.set("Ready to analyze")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create and run the application
    app = PlateDetectorGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
