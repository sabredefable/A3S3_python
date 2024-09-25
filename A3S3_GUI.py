import sys

from layouts.pipeline_layout.PipelineLayout import PipelineLayout

import os
import tkinter
import tkinter.messagebox
import customtkinter
import json
from PIL import Image

workdir = os.getcwd()

#colors
hover_menu_color = "#999999"
text_menu_color = "white"
button_menu_color = "#333333"
sidebar_frame_color ="#333333"
content_frame_color ="#DDDDDD"

button_audit_color = "#FFFFFF"
text_audit_color = "black"

#font_sizes
button_menu_size = 15
logo_size = 25

class SideBarButton(customtkinter.CTkButton):
    def __init__(self, parent, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            corner_radius=0,
            fg_color=button_menu_color,
            text_color=text_menu_color,
            hover_color=hover_menu_color,
            font=customtkinter.CTkFont(size=button_menu_size)
        )

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #pycharm failsafe
        workdir = os.getcwd()
        if workdir.endswith(".venv"):
            workdir = workdir[:-6]
        # configure window
        self.title("A3S3.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (2x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0, fg_color=sidebar_frame_color)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="A3S3",
                                                 font=customtkinter.CTkFont(size=logo_size, weight="bold"), text_color=text_menu_color)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Menu buttons
        sidebar_button_data = [
            ("Audits", self.show_audit),
            ("Pipeline", self.show_pipeline),
            ("Results", self.show_results)
        ]

        self.create_sidebar_buttons(sidebar_button_data)

        # Menu Settings button
        self.settings_image = customtkinter.CTkImage(Image.open(f"{workdir}/icons/settings_white.png"))
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="", image=self.settings_image, command=self.show_settings,
                                                  width=40, height=40, corner_radius=20, fg_color=button_menu_color,
                                                  hover_color=hover_menu_color)
        self.settings_button.grid(row=4, column=0, padx=10, pady=20, sticky="s")

        # Main content
        self.content_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=content_frame_color)
        self.content_frame.grid(row=0, column=1, sticky="nswe")

        self.content_label = customtkinter.CTkLabel(self.content_frame, text="This is definitely the droïd you're looking for...",
                                                    font=customtkinter.CTkFont(size=20))
        self.content_label.pack(pady=20, padx=20, expand=True, fill=tkinter.BOTH)

    def show_audit(self):
        print("Audit clicked")

    def show_pipeline(self):
        self.pipeline_layout = PipelineLayout(self)

    def show_results(self):
        print("Results clicked")

    def show_settings(self):
        print("Settings clicked")

    def create_sidebar_buttons(self, button_data):
        for row, (text, command) in enumerate(button_data, start=1):
            button = SideBarButton(self.sidebar_frame, text=text, command=command)
            button.grid(row=row, column=0, sticky="ew")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    app = App()
    app.mainloop()