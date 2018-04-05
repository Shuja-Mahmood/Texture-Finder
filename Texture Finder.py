__version__ = "1.0.0"

import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as message
from tkinter import filedialog


TEXTURE_LOCATION = "C:\\Textures"


class App(tk.Frame):

    def __init__(self):
        super().__init__()
        self.texture_list = App.get_texture_names()
        self.master.title("Texture Finder")

        if len(self.texture_list) == 0:
            message.showerror("No Texture Files Found", "There are no folders in {0}.\n"
                              "Check folder location and try again".format(TEXTURE_LOCATION))
            self.exit()

        self.texture_type = tk.StringVar()
        self.search_type = tk.IntVar()

        self.seamless = tk.IntVar()
        self.hdr = tk.IntVar()
        self.hires = tk.IntVar()
        self.pbr = tk.IntVar()
        self.game_ready = tk.IntVar()

        self.resolution_labels = []
        self.maps_radio_buttons = []

        self.make_widgets()

    def make_widgets(self):
        self.task_bar()
        self.make_name_field()
        self.display_image(self.texture_list[0], "Sphere")
        self.make_search_box()
        self.make_key_words_entry()
        self.make_info_text()
        self.make_seamless_checkbox()
        self.make_hdr_checkbox()
        self.make_hires_checkbox()
        self.make_pbr_checkbox()
        self.make_game_ready_checkbox()
        self.make_radio_type_flat()
        self.make_radio_type_cube()
        self.make_radio_type_sphere()
        self.make_radio_search_or()
        self.make_radio_search_and()
        App.make_grid_stable()

    def task_bar(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="Exit", command=self.quit)

        tags_menu = tk.Menu(menu_bar)
        tags_menu.add_command(label="Modify Tags", command=self.modify_tags)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Tags", menu=tags_menu)

    # region Tags Modifier
    def modify_tags(self):
        pop_up = tk.Toplevel()
        pop_up.geometry("435x150+400+250")
        pop_up.grab_set()
        pop_up.title("Modify Tags")

        with open(TEXTURE_LOCATION + '\\' + self.combo.get() + '\\' + "tags.meta", "a+") as file:
            file.seek(0)
            tags = file.read().split('\n')

        #region Widgets
        label = tk.Label(pop_up, text="Check the tags you want this texture to have", justify="center",
                         font=("TkinterDefault", 12))
        label.grid(row=0, column=0, columnspan=5, sticky='N', ipady=10, pady=5)

        s = tk.StringVar()
        h = tk.StringVar()
        hi = tk.StringVar()
        p = tk.StringVar()
        g = tk.StringVar()
        values = [s, h, hi, p, g]

        checkbox_seamless = tk.Checkbutton(pop_up, text="Seamless", var=s, onvalue="Seamless")
        checkbox_seamless.grid(row=1, column=0, ipadx=10)
        if "Seamless" in tags:
            checkbox_seamless.select()
        else:
            checkbox_seamless.deselect()

        checkbox_hdr = tk.Checkbutton(pop_up, text="HDR", var=h, onvalue="HDR")
        checkbox_hdr.grid(row=1, column=1, ipadx=10)
        if "HDR" in tags:
            checkbox_hdr.select()
        else:
            checkbox_hdr.deselect()

        checkbox_hires = tk.Checkbutton(pop_up, text="Hi-res", var=hi, onvalue="Hi-res")
        checkbox_hires.grid(row=1, column=2, ipadx=10)
        if "Hi-res" in tags:
            checkbox_hires.select()
        else:
            checkbox_hires.deselect()

        checkbox_pbr = tk.Checkbutton(pop_up, text="PBR", var=p, onvalue="PBR")
        checkbox_pbr.grid(row=1, column=3, ipadx=10)
        if "PBR" in tags:
            checkbox_pbr.select()
        else:
            checkbox_pbr.deselect()

        checkbox_game_ready = tk.Checkbutton(pop_up, text="Game Ready", var=g, onvalue="Game ready")
        checkbox_game_ready.grid(row=1, column=4, ipadx=10)
        if "Game ready" in tags:
            checkbox_game_ready.select()
        else:
            checkbox_game_ready.deselect()
        # endregion
        
        ok_button = tk.Button(pop_up, text="Ok", width=15, command=lambda: self.pop_up_widgets(values, pop_up))
        ok_button.grid(row=2, column=1, columnspan=3, pady=25)

    def pop_up_widgets(self, tag_values, pop_up_root):
        tags = [x.get() for x in tag_values if x.get() != '0']
        with open(TEXTURE_LOCATION + '\\' + self.combo.get() + "\\tags.meta", 'w') as file:
            for i in tags:
                file.write(i + '\n')
        pop_up_root.destroy()
    # endregion

    # region Widgets
    def make_name_field(self):
        self.texture_name = tk.Label(text="Texture Name")
        self.texture_name.grid(row=0, column=1, sticky='N')

    def make_radio_type_flat(self):
        self.radio_flat = tk.Radiobutton(text="Flat", variable=self.texture_type,
                                         value="Flat", command=self.change_texture_type)
        self.radio_flat.grid(row=1, column=0, sticky='E')

    def make_radio_type_cube(self):
        self.radio_cube = tk.Radiobutton(text="Cube", variable=self.texture_type,
                                         value="Cube", command=self.change_texture_type)
        self.radio_cube.grid(row=1, column=1)

    def make_radio_type_sphere(self):
        self.radio_sphere = tk.Radiobutton(text="Sphere", variable=self.texture_type,
                                           value="Sphere", command=self.change_texture_type)
        self.radio_sphere.grid(row=1, column=2, sticky='W')
        self.radio_sphere.select()

    def make_radio_search_or(self):
        self.radio_search_or = tk.Radiobutton(text="OR", variable=self.search_type,
                                              value=1)
        self.radio_search_or.grid(row=5, column=8)

    def make_radio_search_and(self):
        self.radio_search_and = tk.Radiobutton(text="AND", variable=self.search_type,
                                               value=0)
        self.radio_search_and.grid(row=5, column=9)
        self.radio_search_and.select()

    def make_search_box(self):
        self.combo = ttk.Combobox(text="Select Texture", width=30, values=self.texture_list, state="readonly")
        self.combo.grid(row=6, column=5, columnspan=3)
        self.combo.set(self.texture_list[0])
        self.combo.bind("<<ComboboxSelected>>", self.change_texture_type)
        self.combo.bind("<Return>", self.change_texture_type)
        self.combo.bind("<Enter>", self.search)
        self.combo.bind("<FocusIn>", self.search)

    def make_info_text(self):
        self.info = tk.Label(text="To add or remove tags from a texture go to tags, modify tags")
        self.info.grid(row=2, column=4, columnspan=6, sticky='W', ipadx=10)
        self.info = tk.Label(text="Search in the entry box below and separate words using spaces")
        self.info.grid(row=4, column=4, columnspan=6, sticky='W', ipadx=10)
        self.info = tk.Label(text="Search", justify="left")
        self.info.grid(row=5, column=4, sticky='W', ipadx=10)

    def make_key_words_entry(self):
        self.entry = tk.Entry(width=30)
        self.entry.grid(row=5, column=5, columnspan=3)
    
    def make_seamless_checkbox(self):
        self.checkbox = tk.Checkbutton(text="Seamless", variable=self.seamless, onvalue=1, offvalue=0)
        self.checkbox.grid(row=3, column=4)
        
    def make_hdr_checkbox(self):
        self.checkbox = tk.Checkbutton(text="HDR", variable=self.hdr, onvalue=1, offvalue=0)
        self.checkbox.grid(row=3, column=5, sticky='W', ipadx=10)

    def make_hires_checkbox(self):
        self.checkbox = tk.Checkbutton(text="Hi-res", variable=self.hires, onvalue=1, offvalue=0)
        self.checkbox.grid(row=3, column=6)

    def make_pbr_checkbox(self):
        self.checkbox = tk.Checkbutton(text="PBR", variable=self.pbr, onvalue=1, offvalue=0)
        self.checkbox.grid(row=3, column=7)

    def make_game_ready_checkbox(self):
        self.checkbox = tk.Checkbutton(text="Game ready", variable=self.game_ready, onvalue=1, offvalue=0)
        self.checkbox.grid(row=3, column=8, columnspan=2)
    # endregion

    # region Methods
    def display_image(self, image_name, texture_type):
        self.display_name(image_name)
        self.show_available_resolutions(image_name)
        self.show_available_maps(image_name)
        image_file = App.get_image_location(image_name, texture_type)

        canvas = tk.Canvas(width=512, height=512, bg="white")
        canvas.grid(row=2, column=0, rowspan=13, columnspan=3)

        self.texture = Image.open(image_file)
        if App.resize_image(self.texture) is None:
            print("Image: %s\nMap: %s\n" % (image_name, texture_type))
            self.texture = ImageTk.PhotoImage(self.texture)
        else:
            self.texture = ImageTk.PhotoImage(App.resize_image(self.texture))
        canvas.create_image(256, 256, image=self.texture)

    def display_name(self, name):
        self.texture_name.config(text=App.undo_camel_case(name), font=("TkDefaultFont", 18))

    def change_texture_type(self, event=None):
        t = self.texture_type.get()
        if event and (t != "Sphere" and t != "Cube" and t != "Flat"):
            self.texture_type.set("Sphere")
        self.display_image(self.combo.get(), self.texture_type.get())

    def search(self, event):
        if self.search_type.get() == 1:
            refined_textures = self.or_search(self.texture_list, self.entry.get())
        else:
            refined_textures = self.and_search(self.texture_list, self.entry.get())

        final_textures = self.tags_search(refined_textures)
        self.combo.config(values=final_textures)

    def tags_search(self, refined_textures):
        tags = []
        final_textures = []
        if self.seamless.get() == 1:
            tags.append("Seamless")
        if self.hdr.get() == 1:
            tags.append("HDR")
        if self.hires.get() == 1:
            tags.append("Hi-res")
        if self.pbr.get() == 1:
            tags.append("PBR")
        if self.game_ready.get() == 1:
            tags.append("Game ready")

        if len(tags) == 0:
            return refined_textures

        for i in refined_textures:
            with open(TEXTURE_LOCATION + '\\' + i + "\\tags.meta", "a+") as file:
                file.seek(0)
                data = file.read()
                for j in tags:
                    if j in data and i not in final_textures:
                        final_textures.append(i)

        return final_textures

    def show_available_resolutions(self, name):
        if len(self.resolution_labels) != 0:
            for i in self.resolution_labels:
                i.destroy()
            self.resolution_labels.clear()
        resolutions = App.get_resolutions(TEXTURE_LOCATION + '\\' + name)

        for i in range(len(resolutions)):
            text = tk.Label(text=resolutions[i])
            text.grid(row=i+7, column=8, columnspan=2, sticky='W')
            self.resolution_labels.append(text)

    def show_available_maps(self, name):
        if len(self.maps_radio_buttons) != 0:
            for i in self.maps_radio_buttons:
                i.destroy()
            self.maps_radio_buttons.clear()
        maps = App.get_map_names(TEXTURE_LOCATION + '\\' + name)

        for i in range(len(maps)):
            radio = tk.Radiobutton(text=maps[i], variable=self.texture_type,
                                   value=maps[i], command=self.change_texture_type)

            if i % 2 == 0:
                radio.grid(row=int(7+(i/2)), column=4, columnspan=2, sticky='W', ipadx=10)
            else:
                radio.grid(row=int(7+((i-1)/2)), column=6, columnspan=2, sticky='W', ipadx=10)
            self.maps_radio_buttons.append(radio)

    def exit(self):
        self.destroy()
        sys.exit(1)
    # endregion

    # region Static Methods
    @staticmethod
    def get_texture_names():
        return [x for x in os.listdir(TEXTURE_LOCATION) if '.' not in x]

    @staticmethod
    def get_image_location(image_name, texture_type):
        loc = TEXTURE_LOCATION + '\\' + image_name
        if texture_type == "Flat" or texture_type == "Cube" or texture_type == "Sphere":
            t = os.listdir(loc + "\\Previews")
            for i in t:
                if texture_type in i:
                    return loc + "\\Previews\\" + i
        else:
            k = os.listdir(loc)
            if "tags.meta" in k:
                k.remove("tags.meta")
            k = k[0]
            t = os.listdir(loc + '\\' + k)
            for i in t:
                if texture_type in i:
                    return loc + '\\' + k + '\\' + i

    @staticmethod
    def get_resolutions(texture_location):
        resolutions = []
        k = os.listdir(texture_location)
        k.remove("Previews")
        if "tags.meta" in k:
            k.remove("tags.meta")
        for i in k:
            x, y = Image.open(texture_location + '\\' + i + '\\' + os.listdir(texture_location + '\\' + i)[0]).size
            resolutions.append(str(x) + 'x' + str(y))
        return resolutions

    @staticmethod
    def get_map_names(texture_location):
        maps = []
        k = os.listdir(texture_location)
        k.remove("Previews")
        if "tags.meta" in k:
            k.remove("tags.meta")
        k = os.listdir(texture_location + '\\' + k[0])
        for i in k:
            s = i.split('_')
            if "VAR" in s[-2]:
                maps.append(s[-3] + '_' + s[-2])
            else:
                maps.append(s[-2])
        return maps

    @staticmethod
    def resize_image(image):
        width, height = image.size

        if width > height:
            ratio = 512 / height
        else:
            ratio = 512 / width
        width, height = round(width * ratio), round(height * ratio)
        try:
            return image.resize((width, height), Image.ANTIALIAS)
        except ValueError:
            print("Info: {0}".format(image))
            print("ValueError: Image mode is wrong")
            return None

    @staticmethod
    def or_search(textures, key_words):
        key_words = key_words.strip().split(' ')
        refined_textures = []
        for i in textures:
            for j in key_words:
                if j.lower() in i.lower() and i not in refined_textures:
                    refined_textures.append(i)
        return refined_textures

    @staticmethod
    def and_search(textures, key_words):
        key_words = key_words.strip().split(' ')
        refined_textures = []
        flag = True
        for i in textures:
            for j in key_words:
                if not j.lower() in i.lower():
                    flag = False
            if flag:
                refined_textures.append(i)
            flag = True
        return refined_textures

    @staticmethod
    def undo_camel_case(string):
        if len(string) == 0:
            return ''

        new_string = ''
        word = ''
        number_start = False

        for i in string:
            if i != string[0] and i.isupper():
                new_string += word
                word = ' '
                word += i
                number_start = False

            elif i.isdigit() and not number_start:
                new_string += word
                word = ' '
                if i != '0':
                    word += i
                number_start = True

            elif i != '0':
                word += i

        return new_string + word

    @staticmethod
    def make_grid_stable():
        for i in range(15):
            tk.Label(text=' ').grid(row=i, column=15)
    # endregion


def main():
    root = tk.Tk()
    root.geometry("950x600+100+50")
    App()
    root.mainloop()


if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
        Image.MAX_IMAGE_PIXELS = 150000000
        main()
    except ImportError:
        print("Please Download pillow for python")
        print("Windows:\nGo to command prompt and type 'py -m install Pillow'")
