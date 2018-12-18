from tkinter import Tk, Label, Button
root = Tk()

# Create a button with a custom callback
def my_callback():
    print("The button was clicked!")  # Prints to console not the GUI
    
# Make window 600x800 and place at position (50,50)
root.geometry("600x800+50+50")

# Create a button that will destroy the main window when clicked
exit_button = Button(root, text='Exit Program', command=root.destroy).grid(row=0, column=0)
print_button = Button(root, text='Click me!', command=my_callback).grid(row=0, column=1)

jstext = Label(root, text='FirstName: RADOMIR\nLastName: RADOMIR').grid(row=1)

root.mainloop()