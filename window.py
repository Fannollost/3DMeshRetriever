import tkinter as tk
from tkinter import filedialog
import threading
import polyscope as ps

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("3D MeshReviewer")
        self.root.geometry("400x200")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        #Create a canvas object
        canvas= tk.Canvas(self.frame, width= 400, height= 30)

        #Add a text in Canvas
        canvas.create_text(200, 10, text="Choose your action", fill="black", font=('Helvetica 15 bold'))
        canvas.pack()

        self.button_new_window_render = tk.Button(self.frame, text="Render", command=self.open_Render_window, width = 5)
        self.button_new_window_render.pack(pady=10)

        self.button_new_window_query = tk.Button(self.frame, text="Query", command=self.open_Query_window, width = 5)
        self.button_new_window_query.pack(pady=10)

    def open_Render_window(self):
        new_window = tk.Toplevel(self.root)
        self.root.withdraw()
        RenderWindow(new_window, self)

    def open_Query_window(self):
        new_window = tk.Toplevel(self.root)
        self.root.withdraw()
        QueryWindow(new_window, self)

class RenderWindow:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.root.title("Render Meshes")
        self.root.geometry("400x200")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.selected_files = []
        scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.file_listbox = tk.Listbox(self.frame, width=50, height=5, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.button_select_files = tk.Button(self.root, text="Select Files", command=self.open_file_dialog, width = 10)
        self.button_select_files.pack(pady=10)

        self.file_listbox.pack(side=tk.LEFT,fill="both", expand=True)

        self.button_render = tk.Button(self.root, text="Start Render", command=self.open_file_render, width = 10)
        self.button_render.pack(pady=5)
        #self.button_render.place(x = self.root.winfo_width()/2, y = 150)

        left_arrow = '\u2190'
        self.button_back = tk.Button(self.root, text=left_arrow, font=("Arial", 15), command=self.back_to_main)
        self.button_back.place(x = 0, y = 0)

    def open_file_render(self):
        # TODO link to renderer
        for file_path in self.selected_files:
            print(file_path)


    def open_file_dialog(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            self.selected_files.append(file_path)
            self.file_listbox.insert(tk.END, file_path)

    def back_to_main(self):
        self.root.destroy()
        self.main_app.root.deiconify()

class QueryWindow:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.root.title("Query Mesh")
        self.root.geometry("400x100")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.selected_files = []

        self.button_select_files = tk.Button(self.frame, text="Select Files", command=self.select_files)
        self.button_select_files.pack()

        left_arrow = '\u2190'
        self.button_back = tk.Button(self.root, text=left_arrow, font=("Arial", 15), command=self.back_to_main)
        self.button_back.place(x = 0, y = 0)

    def select_files(self):
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            self.selected_files.append(file_path)

        if len(self.selected_files) > 1:
            self.open_Error_window()
            self.selected_files = []
        elif self.selected_files:
            # TODO link to querying
            print("One selected : " + self.selected_files[0])

    def open_Error_window(self):
        new_window = tk.Toplevel(self.root)
        ErrorWindow(new_window, self)

    def open_polyscope(self):
        for file_path in self.selected_files:
            def open_polyscope():
                ps.init()
                ps.show_mesh(file_path)
                ps.show()

            thread = threading.Thread(target=open_polyscope)
            thread.start()

    def back_to_main(self):
        self.root.destroy()
        self.main_app.root.deiconify()

class ErrorWindow:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        self.root.title("ERROR")
        self.root.geometry("400x100")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        canvas= tk.Canvas(self.frame, width= 400, height= 30)
        canvas.create_text(200, 10, text="Please only choose one file to query", fill="black", font=('Helvetica 15 bold'))
        canvas.pack()

        self.button_select_files = tk.Button(self.frame, text="Ok", command=self.destroy)
        self.button_select_files.pack()

    def destroy(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()