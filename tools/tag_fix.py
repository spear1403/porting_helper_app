import tkinter as tk
import os, shutil
from tkinter.filedialog import askdirectory

class TagFix(object):

    def __init__(self):
        self.search_terms = ["screen", "tag", ":"]


    def fixxer(self, file):
        #backup orig file
        self.bak_file = file +'.bak'
        shutil.copy(file, self.bak_file)
        self.temp_file = file +'.temp'
        #setting counter back to zero
        self.counter = 0

        with open(file, 'r',encoding="utf8") as self.in_file:
            with open(self.temp_file, 'w',encoding="utf8") as self.out_file:
                for self.line in self.in_file:
                    if all(self.x in self.line for self.x in self.search_terms):
                        self.counter += 1
                        print("Found a line for fixing...")
                        # see if line is indented
                        self.indent = len(self.line) - len(self.line.lstrip())
                        # Now strip the leading whitespaces
                        self.line = self.line.lstrip()
                        if self.line.startswith("#"):
                            print('Commented out')
                            continue

                        self.line_parts = self.line.split(" tag ")
                        print(self.line_parts)
                        self.new_line = f"{self.indent*' '}{self.line_parts[0]}:\n{self.indent*' '}    tag {self.line_parts[1].replace(':','')}"
                        self.out_file.write(self.new_line)
                        continue
                    self.out_file.write(self.line)
        if self.counter == 0:
            os.remove(self.temp_file )
            os.remove(self.bak_file )
            print ("#################################     Nothing changed...")
        else:
            shutil.copyfile(self.temp_file, file)
            os.remove(self.temp_file )
        print ("#################################     End of file reached...   #######################################")



if __name__ == '__main__':
    app = TagFix()

    def open_file():
        count = 0
        file_dir = askdirectory()
        for r,d,f in os.walk(file_dir):
            for file in f:
                if file.endswith(".rpy"):
                    count += 1
                    filename = os.path.join(r,file)
                    print(f"####################     Opening {filename}...")
                    app.fixxer(filename)
        print ("#################################     All done !... :-)")
        print (f"#################################     {count} Files processed...")

    root = tk.Tk()
    root.title('Cool App')

    button_open = tk.Button(root, text='Open Dir', width=25, command=open_file)
    button_open.pack()
    button_edit = tk.Button(root, text='Quit', width=25, command=root.destroy)
    button_edit.pack()

    root.mainloop()
