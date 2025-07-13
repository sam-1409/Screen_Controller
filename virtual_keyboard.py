import tkinter as tk
from tkinter import *
import pyautogui as pg

start_x, start_y = 0, 0

def on_button_press(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def on_mouse_drag(event):
    global start_x, start_y
    new_x = root.winfo_x() + (event.x - start_x)
    new_y = root.winfo_y() + (event.y - start_y)
    root.geometry(f"+{new_x}+{new_y}")
    

def press_key(key):
    global modifier_state
    if key in modifier_state:
        modifier_state[key] = True
        return
    elif key == 'backspace':
        pg.press('backspace')
    elif key == ' ':
        pg.press('space')
    elif key == 'enter':
        pg.press('enter')
    elif key == 'tab':
        pg.press('tab')
    elif key == 'capslock':
        pg.press('capslock')
    else:
        # Check if any modifier is active
        modifiers = [k for k, v in modifier_state.items() if v]
        if modifiers:
            pg.hotkey(*modifiers, key)
            # Reset all modifiers after use
            for k in modifier_state:
                modifier_state[k] = False
        else:
            pg.typewrite(key)
    return key

def on_background_click(event):
    root.focus_force()
    
def get_window_position():
    return root.winfo_x(), root.winfo_y()

root = tk.Tk()
root.geometry("100x70+0+100")
root.overrideredirect(True)
root.attributes("-alpha", 0.7)
root.attributes("-topmost", True)
root.resizable(False, False)

page1 = Frame(root, bg="White")
page2 = Frame(root, bg="white")

for page in (page1, page2):
    page.place(relx=0, rely=0, relwidth=1, relheight=1)

start = Button(page1, text="Virtual\nKeyboard", command=lambda: show_page2(), font="Arial 10 bold", fg="DarkMagenta")
start.pack(anchor="w", pady=10, ipadx=20, ipady=5)

back = Button(page2, text="←", command=lambda: show_page1(), bg="black", font="Arial 17 bold", fg="white")
back.grid(row=0, column=0, padx=2, pady=2, sticky="w")


keys = [
    ['tab', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['capslock', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['shift', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'backspace'],
    ['ctrl', 'alt', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'space', 'enter']
]

modifier_state = {
    'shift': False,
    'ctrl': False,
    'alt': False
}

for row_idx, row in enumerate(keys, start=1):
    col_idx = 0
    for key in row:
        if key == 'space':
            btn = Button(page2, text="Space", bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key(' '))
            btn.grid(row=row_idx, column=col_idx, padx=1, pady=2, sticky="we")
            col_idx += 1
        elif key == 'enter':
            btn = Button(page2, text="↵", bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key('enter'))
            btn.grid(row=row_idx, column=col_idx, padx=1, pady=2, sticky="we")
            col_idx += 1
        elif key == 'capslock':
            btn = Button(page2, text="Caps", bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key('capslock'))
            btn.grid(row=row_idx, column=col_idx, padx=1, pady=2, sticky="we")
            col_idx += 1
        elif key == 'tab':
            btn = Button(page2, text="Tab", bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key('tab'))
            btn.grid(row=row_idx, column=col_idx, padx=1, pady=2, sticky="we")
            col_idx += 1
        elif key == 'backspace':
            btn = Button(page2, text="⌫", bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key('backspace'))
            btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            col_idx += 1
        elif key in ['shift', 'ctrl', 'alt']:
            btn = Button(page2, text=key.capitalize(), bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key(k))
            btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            col_idx += 1
        else:
            btn = Button(page2, text=key.upper(), bg="black", font="Arial 15 bold", fg="white", width=8, command=lambda k=key: press_key(k))
            btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            col_idx += 1

page1_pos = (0, 100)

def show_page2():
    global page1_pos
    page1_pos = (root.winfo_x(), root.winfo_y())
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    keyboard_width, keyboard_height = 1500, 300
    x = (screen_width - keyboard_width) // 2
    y = screen_height - keyboard_height -50
    root.geometry(f"{keyboard_width}x{keyboard_height}+{x}+{y}")
    root.focus_force()
    page2.tkraise()

def show_page1():
    root.geometry(f"100x70+{page1_pos[0]}+{page1_pos[1]}")
    root.focus_force()
    page1.tkraise()

root.bind("<ButtonPress-1>", on_button_press)
root.bind("<B1-Motion>", on_mouse_drag)
page2.bind("<Button-1>", on_background_click)

page1.tkraise()

if __name__ == "__main__":
    root.mainloop()