import customtkinter
import tkinter as tk
from tkinter import filedialog
import os
import json
from A3S3_Decompilers import A3S3_Decompilers
from classes.ListWithPaths import ListWithPaths
from classes.AuditBuffer import AuditBuffer
from A3S3_FeaturesExtractor import A3S3_FeaturesExtractor
from A3S3_Auditor import A3S3_Auditor

#colors
hover_menu_color = "#999999"
text_menu_color = "white"
button_menu_color = "#333333"
sidebar_frame_color ="#333333"
content_frame_color ="#DDDDDD"
new_button_color="#43a82f"

button_audit_color = "#FFFFFF"
text_audit_color = "black"

#font_sizes
button_menu_size = 15
logo_size = 25

class PipelineLayout(customtkinter.CTkFrame):
    def __init__(self, parent):
        self.decompiler = A3S3_Decompilers()

        for widget in parent.content_frame.winfo_children():
            widget.destroy()

        self.content_frame = customtkinter.CTkFrame(parent.content_frame, fg_color=content_frame_color,corner_radius=0,width=1000,height=600)
        self.content_frame.grid(row=0, column=0, sticky='nsew', pady=40)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=0)

        #choice 1 - Decompilers
        self.decompiler_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color=content_frame_color)
        self.decompiler_frame.columnconfigure(0, weight=1)
        self.decompiler_frame.columnconfigure(1, weight=0)
        self.decompiler_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=0)

        self.decompiler_frame_label = customtkinter.CTkLabel(self.decompiler_frame, fg_color=content_frame_color, text="Decompiler")
        self.decompiler_frame_label.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        self.decompiler_frame_option = customtkinter.CTkOptionMenu(self.decompiler_frame, fg_color="white", values=self.decompiler.get_options(), text_color="black")
        self.decompiler_frame_option.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)

        #choice 2 - Sign Extractors
        extractors_options = ["A3S3"]
        self.extractor_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color=content_frame_color)
        self.extractor_frame.columnconfigure(0, weight=1)
        self.extractor_frame.columnconfigure(1, weight=0)
        self.extractor_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=0)

        self.extractor_frame_label = customtkinter.CTkLabel(self.extractor_frame, fg_color=content_frame_color, text="Feature extractor")
        self.extractor_frame_label.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        self.extractor_frame_option = customtkinter.CTkOptionMenu(self.extractor_frame, fg_color="white",
                                                                   values=extractors_options, text_color="black")
        self.extractor_frame_option.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)

        #Choice 3 - Audit File
        self.audit_file_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color=content_frame_color)
        self.audit_file_frame.columnconfigure(0, weight=1)
        self.audit_file_frame.columnconfigure(1, weight=0)

        self.audit_file_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=0)

        self.audit_file_frame_label = customtkinter.CTkLabel(self.audit_file_frame, fg_color=content_frame_color,
                                                            text="Audit file")
        self.audit_file_frame_label.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        self.audit_file_frame_button = customtkinter.CTkButton(self.audit_file_frame, fg_color="white", text="Select file", text_color="black", command=lambda title="Select a file",filetypes=[("json files", "*.json")]: self.open_file_explorer(self.audit_file_frame_file,title, filetypes))
        self.audit_file_frame_button.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)
        self.audit_file_frame_file = customtkinter.CTkLabel(self.content_frame, fg_color=content_frame_color, text="Choose an audit file")
        self.audit_file_frame_file.grid(row=2, column=1, sticky='nsew', padx=20, pady=10)

        #Choice 4 - Options, batch vs APK file
        self.apk_file_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color=content_frame_color)
        self.apk_file_frame.columnconfigure(0, weight=1)
        self.apk_file_frame.columnconfigure(1, weight=0)

        self.apk_file_frame.grid(row=3, column=0, sticky='nsew', padx=20, pady=0)

        self.apk_file_frame_choice = customtkinter.CTkSegmentedButton(self.apk_file_frame, values=["Batch","File"], command=self.selected_option)
        self.apk_file_frame_choice.set("File")
        self.apk_file_frame_choice.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)

        self.apk_file_frame_button = customtkinter.CTkButton(self.apk_file_frame,
                                                             fg_color="white",
                                                             text="Select file",
                                                             text_color="black",
                                                             command=lambda title="Select a file", filetypes=[("apk files", "*.apk"), ("xapk files", "*.xapk")]: self.open_file_explorer(self.apk_file_frame_file, title, filetypes))
        self.apk_file_frame_button.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)
        self.apk_file_frame_file = customtkinter.CTkLabel(self.content_frame, fg_color=content_frame_color,
                                                            text="Choose a file")
        self.apk_file_frame_file.grid(row=3, column=1, sticky='nsew', padx=20, pady=10)

        #Choice 5 - Output Directory
        self.output_file_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color=content_frame_color)
        self.output_file_frame.columnconfigure(0, weight=1)
        self.output_file_frame.columnconfigure(1, weight=0)
        self.output_file_frame.grid(row=4, column=0, sticky='nsew', padx=20, pady=0)

        self.output_file_frame_label = customtkinter.CTkLabel(self.output_file_frame, fg_color=content_frame_color,
                                                             text="Output directory")
        self.output_file_frame_label.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        self.output_file_frame_button = customtkinter.CTkButton(self.output_file_frame, fg_color="white",
                                                               text="Select directory", text_color="black",
                                                               command=lambda title="Select a directory": self.open_file_explorer(
                                                                   self.output_file_frame_file, title))
        self.output_file_frame_button.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)
        self.output_file_frame_file = customtkinter.CTkLabel(self.content_frame, fg_color=content_frame_color,
                                                            text="Choose an output directory")
        self.output_file_frame_file.grid(row=4, column=1, sticky='nsew', padx=20, pady=10)

        #Options
        self.options_frame = customtkinter.CTkFrame(self.content_frame, corner_radius=0, fg_color=content_frame_color)
        self.options_frame.columnconfigure(0, weight=1)
        self.options_frame.columnconfigure(1, weight=0)
        self.options_frame.grid(row=5, column=0, sticky='nsew', padx=20, pady=0)

        self.options_frame_label = customtkinter.CTkLabel(self.options_frame, fg_color=content_frame_color, text="Export Options")
        self.options_frame_label.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        self.options_frame_opt1 = customtkinter.CTkCheckBox(self.options_frame, fg_color=content_frame_color, text=".csv files for each source", checkmark_color="black", border_color="black")
        self.options_frame_opt1.grid(row=0, column=1, sticky='nsew', padx=20, pady=10)
        self.options_frame_opt2 = customtkinter.CTkCheckBox(self.options_frame, fg_color=content_frame_color, text=".xls file with all sources", checkmark_color="black", border_color="black")
        self.options_frame_opt2.grid(row=1, column=1, sticky='nsew', padx=20, pady=10)


        #Buttons
        self.audit_start_button = customtkinter.CTkButton(self.content_frame, fg_color=new_button_color,
                                                               text="Start Audit", text_color="white", command=self.start_audit)
        self.audit_start_button.grid(row=8, column=1, sticky='s', padx=20, pady=10)



    def open_file_explorer(self, label, title, filetypes=None):
        if filetypes:
            file_path = filedialog.askopenfilename(
                title=title,
                filetypes=filetypes
            )
        else:
            file_path = filedialog.askdirectory()

        if file_path:
            label.configure(text=file_path)
        else:
            print("Aucun fichier sélectionné")

    def selected_option(self, value):
        match value:
            case "File":
                self.apk_file_frame_button.configure(text="Select file",command=lambda title="Select a file", filetypes=[("apk files", "*.apk"), ("xapk files", "*.xapk")]: self.open_file_explorer(self.apk_file_frame_file, title, filetypes))
                self.apk_file_frame_file.configure(text="Choose a file")
            case "Batch":
                self.apk_file_frame_button.configure(text="Select directory", command=lambda title="Select a directory": self.open_file_explorer(self.apk_file_frame_file, title))
                self.apk_file_frame_file.configure(text="Choose a directory")

    def start_audit(self):
        blank = ["Choose a directory", "Choose a file", "Choose an output directory"]
        decompiler = self.decompiler_frame_option.get()
        extractor = self.extractor_frame_option.get()
        audit_file = self.audit_file_frame_file.cget(attribute_name="text")
        audit_option = self.apk_file_frame_choice.get()
        path_to_apk = self.apk_file_frame_file.cget(attribute_name="text")
        output_directory = self.output_file_frame_file.cget(attribute_name="text")
        csv_export = self.options_frame_opt1.get()
        xls_export = self.options_frame_opt2.get()

        if (audit_file in blank or path_to_apk in blank or output_directory in blank) :
            self.error_message("Please complete the missing fields.")
        elif audit_option == "File":
            if path_to_apk.endswith(".xapk"):
                file_name = path_to_apk.split("/")[-1][:-5]
            else:
                file_name = path_to_apk.split("/")[-1][:-4]
            temp_output_directory = output_directory + f"/{file_name}"
            self.audit_pipe(file_name, temp_output_directory, decompiler, path_to_apk, extractor, audit_file, csv_export, xls_export)
        elif audit_option == "Batch":
            json_batch = []
            for file in os.listdir(path_to_apk):
                if file.endswith(".apk") or file.endswith(".xapk"):
                    if file.endswith(".xapk"):
                        file_name = file[:-5]
                    else:
                        file_name = file[:-4]
                    file_path = f"{path_to_apk}/{file}"
                    temp_output_directory = output_directory + f"/{file_name}"
                    self.audit_pipe(file_name, temp_output_directory, decompiler, file_path, extractor, audit_file, csv_export, xls_export)
                    json_batch.append(self.auditor.get_audited_data())
            self.auditor.excel_export(json_batch, None, True, output_directory)



    def audit_pipe(self, file_name, output_directory, decompiler, path_to_apk, extractor, audit_file, csv_export, xls_export):

        self.extractor = A3S3_FeaturesExtractor()
        # Decompile
        print("Decompiling " + file_name + " ...")
        self.decompiler.set_option(decompiler, output_directory, path_to_apk)
        self.decompiler.decompile_apk(True)

        # Extract from code
        print('Searching ' + file_name + " ...")
        self.audit_buffer = self.extractor.extract_features(output_directory, extractor, False)

        # Audit
        print('Auditing ' + file_name + " ...")
        self.auditor = A3S3_Auditor(audit_file, output_directory, file_name)
        self.auditor.start_auditing(self.audit_buffer)
        self.auditor.export_audit_data(csv_export, xls_export, self.audit_buffer)

        print("Finished auditing " + file_name)

    def error_message(self, message):
        error_frame = customtkinter.CTkToplevel()
        error_frame.title("A3S3 - Error")
        error_frame.geometry("300x150")

        error_label = customtkinter.CTkLabel(master=error_frame, text=message)
        error_label.pack(pady=20, padx=20)

        close_bouton = customtkinter.CTkButton(master=error_frame, text="Close", command=error_frame.destroy)
        close_bouton.pack(pady=10)


