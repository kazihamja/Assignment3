import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Import classes from our other files
from image_lib import ImageHandler
from logic import GameTracker

# Main GUI class
# Person 1 worked on this file
class MyGameApp:
    def __init__(self, win):
        self.win = win
        self.win.title("Spot the Difference - Student Team Project")
        self.win.geometry("1100x800")
        
        self.bg_color = "#e8e8e8"
        self.win.configure(bg=self.bg_color)
        
        self.handler = ImageHandler()
        self.tracker = GameTracker()
        self.zoom = 1.0 # To fit big images on screen
        
        self.build_ui()

    def build_ui(self):
        # Top title area
        top = tk.Frame(self.win, bg=self.bg_color, pady=10)
        top.pack(fill=tk.X)
        
        tk.Label(top, text="Difference Finding Game", font=("Arial", 18, "bold"), 
                 bg=self.bg_color).pack()

        # Control buttons and info
        ctrl = tk.Frame(self.win, bg="#d0d0d0", bd=1, relief="ridge", padx=10, pady=5)
        ctrl.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Button(ctrl, text="Choose Image", command=self.on_load).pack(side=tk.LEFT, padx=5)
        self.giveup_btn = tk.Button(ctrl, text="Reveal All", command=self.show_all, state=tk.DISABLED)
        self.giveup_btn.pack(side=tk.LEFT, padx=5)

        self.info_lbl = tk.Label(ctrl, text="Score: 0 | Misses: 0/3", font=("Arial", 11), bg="#d0d0d0")
        self.info_lbl.pack(side=tk.RIGHT, padx=10)

        # Main message area
        self.msg = tk.Label(self.win, text="Click 'Choose Image' to start playing", font=("Arial", 10), bg=self.bg_color)
        self.msg.pack(pady=5)

        # The area where images go
        self.draw_space = tk.Canvas(self.win, bg="white", bd=2, relief="sunken")
        self.draw_space.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        self.draw_space.bind("<Button-1>", self.on_click)

    def on_load(self):
        f = filedialog.askopenfilename()
        if not f:
            return
        
        if self.handler.open_file(f):
            if self.handler.make_diffs(5):
                self.tracker.reset_game()
                self.redraw()
                self.giveup_btn.config(state=tk.NORMAL)
                self.refresh_text()
                self.msg.config(text="Find the 5 changes on the right side!", fg="blue")
            else:
                messagebox.showinfo("Wait", "Could not make 5 changes, try a different picture.")
        else:
            messagebox.showerror("Error", "Could not open that file.")

    def redraw(self):
        self.draw_space.delete("all")
        real_w = self.handler.original.shape[1]
        real_h = self.handler.original.shape[0]
        
        self.draw_space.update()
        cw = self.draw_space.winfo_width()
        ch = self.draw_space.winfo_height()
        
        limit_w = (cw - 60) // 2
        limit_h = ch - 50
        
        z_w = limit_w / real_w
        z_h = limit_h / real_h
        self.zoom = min(z_w, z_h, 1.0)
        
        new_w = int(real_w * self.zoom)
        new_h = int(real_h * self.zoom)
        
        left_img = Image.fromarray(self.handler.original).resize((new_w, new_h))
        right_img = Image.fromarray(self.handler.modified).resize((new_w, new_h))
        
        self.tk_left = ImageTk.PhotoImage(left_img)
        self.tk_right = ImageTk.PhotoImage(right_img)
        
        gap = 30
        self.x1 = (cw - (new_w * 2 + gap)) // 2
        self.y = (ch - new_h) // 2
        self.x2 = self.x1 + new_w + gap
        
        self.draw_space.create_image(self.x1, self.y, anchor=tk.NW, image=self.tk_left)
        self.draw_space.create_image(self.x2, self.y, anchor=tk.NW, image=self.tk_right)
        
        self.draw_space.create_text(self.x1 + new_w//2, self.y - 15, text="Original", font=("Arial", 10))
        self.draw_space.create_text(self.x2 + new_w//2, self.y - 15, text="Modified Side", font=("Arial", 10))
        
        for idx in self.tracker.found:
            self.circle_it(idx, "red")

    def circle_it(self, num, col):
        x, y, w, h = self.handler.diff_list[num]
        scr_x = (x + w//2) * self.zoom
        scr_y = (y + h//2) * self.zoom
        size = 14 * self.zoom
        if size < 5: size = 5
        
        self.draw_space.create_oval(self.x1 + scr_x - size, self.y + scr_y - size, 
                                     self.x1 + scr_x + size, self.y + scr_y + size, outline=col, width=2)
        self.draw_space.create_oval(self.x2 + scr_x - size, self.y + scr_y - size, 
                                     self.x2 + scr_x + size, self.y + scr_y + size, outline=col, width=2)

    def on_click(self, ev):
        if self.handler.original is None or self.tracker.is_over:
            return

        click_x = ev.x - self.x2
        click_y = ev.y - self.y
        real_click_x = click_x / self.zoom
        real_click_y = click_y / self.zoom
        
        if 0 <= click_x <= (self.handler.original.shape[1] * self.zoom) and \
           0 <= click_y <= (self.handler.original.shape[0] * self.zoom):
            
            idx, is_hit = self.tracker.check_hit(real_click_x, real_click_y, self.handler.diff_list)
            
            if is_hit:
                self.circle_it(idx, "red")
                self.refresh_text()
                self.msg.config(text="Got one! Nice.", fg="green")
                if len(self.tracker.found) == 5:
                    messagebox.showinfo("Finished", "All differences found! Good job.")
                    self.giveup_btn.config(state=tk.DISABLED)
            else:
                self.refresh_text()
                self.msg.config(text="Missed! Look closer.", fg="red")
                if self.tracker.is_over:
                    messagebox.showwarning("Game Over", "Too many misses.")
                    self.show_all()

    def refresh_text(self):
        rem = 5 - len(self.tracker.found)
        self.info_lbl.config(text=f"Score: {self.tracker.score} | Misses: {self.tracker.misses}/3 | Left: {rem}")

    def show_all(self):
        self.tracker.is_over = True
        for i in range(len(self.handler.diff_list)):
            if i not in self.tracker.found:
                self.circle_it(i, "blue")
        self.giveup_btn.config(state=tk.DISABLED)
        self.msg.config(text="Revealing missed spots...", fg="darkblue")

if __name__ == "__main__":
    root = tk.Tk()
    myapp = MyGameApp(root)
    root.mainloop()
