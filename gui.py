import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cycle_tracking import get_today_info, get_questions, save_entry

today_info = get_today_info()
questions = get_questions(today_info["moon_desc"])

root = tk.Tk()
root.title("Menstrual Cycle Tracker")
root.geometry("900x600")
# root.attributes("-fullscreen", True)  # Uncomment to go fullscreen

canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

try:
    bg_image = Image.open(r"C:\Users\Srilalitha M S\Documents\Bakchodi\cycle_track\nina zenik aesthetic • six of crows.jpeg")
    print("Background image loaded successfully.")
except Exception as e:
    print(f"Error loading image: {e}")

bg_photo = ImageTk.PhotoImage(bg_image)
bg_img_id = canvas.create_image(0, 0, anchor="nw", image=bg_photo)
canvas.tag_lower(bg_img_id)  # Send background image behind everything

scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

style = ttk.Style()
style.configure("Content.TFrame", background="#f8f0fc")  # light background for readability
style.configure("TLabel", background="#f8f0fc")
style.configure("TLabelframe", background="#f8f0fc")
style.configure("TLabelframe.Label", background="#f8f0fc")

content_frame = ttk.Frame(canvas, padding=20, style="Content.TFrame")
content_window = canvas.create_window(0, 0, anchor="nw", window=content_frame)

# Populate content_frame with labels and entry widgets
ttk.Label(content_frame, text="🌸 Menstrual Cycle Tracker 🌸",
          font=("Segoe UI", 18, "bold")).pack(pady=10)

frame_info = ttk.LabelFrame(content_frame, text="Today’s Info", style="TLabelframe")
frame_info.pack(fill="x", pady=10)

ttk.Label(frame_info, text=f"Date: {today_info['date'].split(' ')[0]}").pack(anchor="w", padx=10, pady=2)
ttk.Label(frame_info, text=f"Cycle Day: {today_info['cycle_day']} — {today_info['phase']}").pack(anchor="w", padx=10, pady=2)
ttk.Label(frame_info, text=today_info['moon_desc']).pack(anchor="w", padx=10, pady=2)

entries = {}
for q_text, col_name in questions:
    frame = ttk.LabelFrame(content_frame, text=q_text, style="TLabelframe")
    frame.pack(fill="x", pady=5)
    entry = tk.Text(frame, height=3, wrap="word")
    entry.pack(fill="x", padx=10, pady=5)
    entries[col_name] = entry

def save_data():
    entry_data = {
        "Date": today_info["date"].split(" ")[0],
        "Cycle Day": today_info["cycle_day"],
        "Phase": today_info["phase"],
        "Delay Days": today_info["delay_days"]
    }
    for col_name, widget in entries.items():
        entry_data[col_name] = widget.get("1.0", "end").strip()
    save_entry(entry_data)
    messagebox.showinfo("Saved", "Your entry has been saved!")
    root.destroy()

ttk.Button(content_frame, text="💾 Save Entry & Exit", command=save_data).pack(pady=20)
ttk.Button(content_frame, text="❌ Close", command=root.destroy).pack(pady=10)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    new_width, new_height = event.width, event.height
    global bg_photo
    resized = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized)
    canvas.itemconfig(bg_img_id, image=bg_photo)
    canvas.itemconfig(content_window, width=new_width)
    canvas.tag_lower(bg_img_id)

canvas.bind("<Configure>", on_configure)

def on_mousewheel(event):
    # Cross-platform scroll: event.delta negative means scroll down
    if event.delta:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    else:
        # For Linux systems (event.num = 4 or 5)
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)
canvas.bind_all("<Button-4>", on_mousewheel)  # Linux scroll up
canvas.bind_all("<Button-5>", on_mousewheel)  # Linux scroll down

root.mainloop()
