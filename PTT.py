import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time
import csv
import random  

def extract_number(s):
    """Extracts the number from a string."""
    match = re.search(r'\d+', s)
    return int(match.group()) if match else 0

class SingleImageRatingApp:
    def __init__(self, root, main_folder):
        self.root = root
        self.main_folder = main_folder
        self.responses = []
        # Create a list of image files and then shuffle it
        self.files = [os.path.join(main_folder, f) for f in os.listdir(main_folder) if f.endswith('.png')]
        random.shuffle(self.files)  # Shuffle the list
        self.current_image_path = None
        self.rating_frame = None

    def start_test(self):
        self.load_next_image()

    def load_next_image(self):
        if not self.files:
            self.save_responses()
            return

        self.start_time = time.time()
        self.current_image_path = self.files.pop()

        for widget in self.root.winfo_children():
            widget.destroy()

        img = Image.open(self.current_image_path)
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.root, image=img)
        img_label.image = img
        img_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.get_rating()

    def get_rating(self):
        self.rating_frame = tk.Frame(self.root)
        self.rating_frame.pack(side=tk.RIGHT, padx=10)

        rating_var = tk.IntVar(value=0)

        # Radio buttons for rating
        for i in range(5, 0, -1):
            # Adjust the text logic for 5 choices
            if i == 5:
                confidence = 'extremely'
                image_type = 'generated'
            elif i == 4:
                confidence = 'moderately'
                image_type = 'generated'
            elif i == 3:
                confidence = 'neither'
                image_type = 'generated or real'
            elif i == 2:
                confidence = 'moderately'
                image_type = 'real'
            else:  # i == 1
                confidence = 'extremely'
                image_type = 'real'

            text = f" ({i})  I am {confidence} confident that the image is {image_type}."
            tk.Radiobutton(self.rating_frame, text=text, variable=rating_var, value=i).pack(anchor=tk.W)

        def submit_rating():
            total_elapsed_time = time.time() - self.start_time
            rating = rating_var.get()
            if rating == 0:
                messagebox.showwarning("Warning", "Please select a rating before submitting.")
                return

            self.responses.append((os.path.basename(self.current_image_path), total_elapsed_time, rating))

            self.rating_frame.destroy()
            self.load_next_image()

        submit_button = tk.Button(self.rating_frame, text="Submit", command=submit_rating)
        submit_button.pack(pady=10)

    def save_responses(self):
        if not self.responses:
            messagebox.showinfo("No Responses", "No responses to save.")
            self.end_test()
            return

        filename = simpledialog.askstring("Input", "Enter your name to save responses:", parent=self.root)
        if filename:
            with open(f"{filename}_responses.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["image_name", "time_taken", "rating"])
                for response in self.responses:
                    writer.writerow(response)
            self.end_test()

    def end_test(self):
        messagebox.showinfo("Done", "Test finished. Responses saved.")
        self.root.quit()

def show_start_screen(root, app):
    start_frame = tk.Frame(root)
    start_frame.pack(pady=50)

    welcome_label = tk.Label(start_frame, text="Welcome to the Image Rating Test", font=("Helvetica", 16))
    welcome_label.pack(pady=10)

    start_button = tk.Button(start_frame, text="Start", command=lambda: start_test(app, start_frame))
    start_button.pack()

def start_test(app, start_frame):
    start_frame.destroy()
    app.start_test()

if __name__ == "__main__":
    IMAGE_FOLDER_PATH = '/Users/tr0028/Desktop/SINGLE/SMALL/'  # Replace with your folder path

    root = tk.Tk()
    root.title("Single Image Rating Test")
    root.geometry("1000x600")

    app = SingleImageRatingApp(root, IMAGE_FOLDER_PATH)

    show_start_screen(root, app)

    root.mainloop()
