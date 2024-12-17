import numpy as np
import pandas as pd
import streamlit as st
from streamlit_cropperjs import st_cropperjs
import easyocr
import os
from streamlit_option_menu import option_menu
from datetime import datetime
import json
import time
import shutil
import cv2
import ast
import re

# Set initial session values
if 'processed_index' not in st.session_state:
    st.session_state['processed_index'] = 0
if 'now' not in st.session_state:
    st.session_state['now'] = datetime.now()
if 'button_ocr_start' not in st.session_state:
    st.session_state.button_ocr_start_disabled = True
if 'button_back_disabled' not in st.session_state:
    st.session_state.button_back_disabled = True
if 'button_forward_disabled' not in st.session_state:
    st.session_state.button_forward_disabled = False


# Load settings
# set input and output folders
input_folder = ""
output_folder = ""
csv_folder = ""
processed_folder = ""
validated_prefix = ""

# Read settings file with input, output, processing folders
settingsFile = open('settings.json',"r")
settings=json.load(settingsFile)

# Closing file
settingsFile.close()

# Reading setting values and checking if folders exist and create in case they do not access
def check_settings_directories(settings):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)



# read settings json values
input_folder = settings["Input"]
output_folder= settings["Output"]
processed_folder= settings["Processed"]
validated_prefix = settings["Validated_Prefix"]
supported_image_types = settings["Supported Image Types"]

# check all directories
check_settings_directories(settings)


# Funktion zum Filtern von Texten definieren
def filter_text(text):
    if re.match(r'^\d+[a-zA-Z0-9\-\/]*$', text):
        return False
    if text.lower() in ['klingel', 'licht','sss siedle','sss', 'siedle','werbung','klingeln','kräftig','bitte','einen','eingang','weiter','zu','video','überwachung','videoüberwachung','werbung!','keine','oder','zeitungen','einwerfen','danke','oder zeitungen einwerfen!danke', 'hier wohnt','hier','wohnt','familie','fam', 'fam.', 'fa', 'fa.','elcom']:
        return False
    return True


# OCR fuction
def ocr(image_path, image_name):
    reader = easyocr.Reader(['de'], gpu=True, recog_network='latin_g2') # recog fuer bessere Genauigkeit
    ocr_results = reader.readtext(image_path, contrast_ths=0.05, adjust_contrast=0.7, text_threshold=0.8, low_text=0.4)
    dfOCRResults = pd.DataFrame(ocr_results, columns=['bbox', 'Namen', 'Confidence Level'])
    dfOCRResults['Bildname'] = image_name

    return dfOCRResults

def open_image(image_path):
    if os.name == 'nt':  # Für Windows
        os.startfile(image_path)
    elif os.name == 'posix':  # Für macOS und Linux
        subprocess.call(('open', image_path))
    else:
        st.error("Unsupported OS")


def names_on_image(dfnames, image):
    listnames = dfnames[['Namen','bbox']].values.tolist()

    for (Namen, bbox) in listnames:
        if isinstance(Namen, str) and isinstance(bbox, str) and len(Namen) > 0 and len(bbox) > 0:
            try:
                # Konvertieren der bbox-Zeichenkette in ein Tuple von Tuples
                bbox_tuple = ast.literal_eval(bbox)
                if len(bbox_tuple) == 4 and all(isinstance(point, (list, tuple)) and len(point) == 2 for point in bbox_tuple):
                    # Konvertieren von Punkten in Integer, falls nötig
                    tl = tuple(map(int, bbox_tuple[0]))
                    br = tuple(map(int, bbox_tuple[2]))

                    # Zeichnen des umgebenden Rechtecks auf dem Bild
                    cv2.rectangle(image, tl, br, (229, 83, 0), 5)
                    cv2.putText(image, Namen, (tl[0], br[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (229, 83, 0), 2)
                else:
                    raise ValueError("bbox format is incorrect")
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing bbox for name '{Namen}': {e}")
                #  Weitere Fehlerbehandlung hier
        else:
            # Behandlung von Fällen, in denen Namen oder bbox nicht den erwarteten Typen/Formaten entsprechen
            continue

    return image

# def names_on_image(dfnames, image):
#
#     listnames=dfnames[['Namen','bbox']].values.tolist()
#
#     for (Namen, bbox) in listnames:
#
#         if (len(Namen)>0 and len(bbox)>0):
#
#             bbox=bbox.replace("[[","(")
#             bbox=bbox.replace("]]",")")
#             bbox=bbox.replace("[","(")
#             bbox=bbox.replace("]",")")
#
#             bbox_tuple=ast.literal_eval(bbox)
#
#             (tl, tr, br, bl) = bbox_tuple
#             br_text = (br[0] + 20, br[1] + 50)
#
#             # Draw the bounding box on the image
#             try:
#                 cv2.rectangle(image, tl, br, (229, 83, 0), 5)
#                 cv2.putText(image, Namen, br_text, cv2.FONT_HERSHEY_SIMPLEX, 2, (229, 83, 0), 10)
#             except:
#                 st.toast("Rechteck oder Namen können auf dem Bild nicht richtig dargestellt werden")
#
#     return image

# disable "OCR starten" button in case the input folder is empty
def disable_button_empty_dir (filesInInputFolder):
    if len(filesInInputFolder) < 1:
        st.session_state.button_ocr_start_disabled = True
    else:
        st.session_state.button_ocr_start_disabled = False

# Funktion zum Formatieren der Namen
def format_names(name):
    # Konvertiere die Eingabe in einen String, falls sie keine ist
    name = str(name)

    # Teile den Namen am Komma
    parts = name.split(',')

    # Kapitalisiere das erste Wort und setze nach dem Komma alles klein
    formatted_parts = [part.strip().capitalize() for part in parts]
    return ', '.join(formatted_parts)

    # Use the full page instead of a narrow central column
st.set_page_config(layout="wide")
st.markdown("`©️ Eine Entwicklung der Gebietsentwicklung und des Portfoliomanagements`")

#Title, Header and Sidebar
logo_url = "https://deutsche-giganetz.de/images/dgn/corporate/branding/wort-bildmarke/DGN_Wort-Bildmarke_rgb.svg"
#st.title('DGN Dizitizer')
#st.divider()
st.sidebar.image(logo_url)
with st.sidebar:
    st.write("##")
    selected = option_menu("Menu", ["OCR", "Validierung", "Settings"],
                           icons=["robot",'keyboard', 'gear'], default_index=1, styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "DarkOrange"},
        })

if selected=="OCR":
    conOCR = st.container(border=True)
    ocr_input_option = conOCR.radio("OCR Option",['Verzeichnis','Einzelnes Bild'],horizontal=True)

    # And within an expander
    if ocr_input_option == "Verzeichnis":
        my_expander_folders = conOCR.expander("Verzeichnisse", expanded=True)
        with my_expander_folders:
            st.write("Input Verzeichnis:", input_folder)
            st.write("Output Verzeichnis:",output_folder)
        # And within an expander
        my_expander_image = conOCR.expander("Bild auswählen", expanded=False)
        with my_expander_image:
            #Image uploader and saver
            input_image=st.file_uploader(label='Wähle hier das einzelne Bild für die Erkennung',type=['png','jpeg','jpg'],)
            if input_image:
                pic = input_image.read()
                cropped_pic = st_cropperjs(pic=pic, btn_text="Bildauschnitt festlegen", key="foo")
                if cropped_pic:
                    st.image(cropped_pic, output_format="PNG")
                    st.button("Bild sichern",help="Speiche das Bild im Input Verzeichnis")
    else:
        st.session_state.button_ocr_start_disabled

        my_expander_folders = conOCR.expander("Verzeichnisse", expanded=False)
        with my_expander_folders:
            st.write("Input Verzeichnis:", input_folder)
            st.write("Output Verzeichnis:",output_folder)
            # And within an expander
        my_expander_image = conOCR.expander("Bild auswählen", expanded=True)
        with my_expander_image:
            #Image uploader and saver
            input_image=st.file_uploader(label='Wähle hier das einzelne Bild für die Erkennung',type=['png','jpeg','jpg'],)
            if input_image:
                pic = input_image.read()
                cropped_pic = st_cropperjs(pic=pic, btn_text="Bildauschnitt festlegen", key="foo")
                if cropped_pic:
                    st.image(cropped_pic, output_format="PNG")
                    if st.button("Bild sichern",help="Speiche das Bild im Input Verzeichnis"):

                        while True:
                            try:
                                with open(os.path.join(input_folder,input_image.name),"wb") as f:
                                    f.write(cropped_pic)
                                break
                            except:
                                if os.path.isdir (input_folder) == False:
                                    os.mkdir(input_folder)
                                    with open(os.path.join(input_folder,input_image.name),"wb") as f:
                                        f.write(cropped_pic)
                        st.success(str(input_image.name) +' hochgeladen')
                single_file_name = input_folder + input_image.name

    conOCR.write("##")
    colOCRButton, colProgress = conOCR.columns((1,4))

    filesInInputFolder = os.listdir(input_folder)

    disable_button_empty_dir(filesInInputFolder)

    if colOCRButton.button("OCR starten", help="Starte die Texterkennung mit dem ausgewählten Input", disabled=st.session_state.button_ocr_start_disabled):
        if ocr_input_option == 'Verzeichnis':
            progress_text = "OCR läuft"
            progressbar_ocr = colProgress.progress(0, text=progress_text)
            filesInInputFolder = os.listdir(input_folder)
            if len(filesInInputFolder) > 0:
                progressbar_step = 1 / len(filesInInputFolder)
            iteration = 1

            for image in filesInInputFolder:
                image_input_path = os.path.join(input_folder, image)  # Korrekt definierter Pfad
                image_name = image.split('.')[0]  # Annahme, dass der Dateiname vor dem ersten Punkt der Bildname ist

                # OCR durchführen
                dfImage = ocr(image_input_path, image_name)
                # Filtern basierend auf Confidence Level und spezifischen Textinhalten
                dfImage = dfImage[dfImage['Confidence Level'] >= 0.5]
                dfImage = dfImage[dfImage['Namen'].apply(filter_text)]

                # Ergebnisse speichern
                csv_path = os.path.join(output_folder, f"{image_name}.csv")
                dfImage.to_csv(path_or_buf=csv_path)

                # Verschieben der Datei vom Eingabe- zum Verarbeitungsordner
                image_processed_path = os.path.join(processed_folder, image)
                shutil.move(image_input_path, image_processed_path)

                progress = progressbar_step * iteration
                progressbar_ocr.progress(progress, text=progress_text)
                iteration += 1

            st.toast('OCR erfolgreich durchgeführt, bitte output Verzeichnis prüfen.')
            disable_button_empty_dir(os.listdir(input_folder))
            time.sleep(5)
            progressbar_ocr.empty()


        elif ocr_input_option == 'Einzelnes Bild':
            if input_image is not None:  # input_image sollte vorher definiert sein, als das vom Benutzer hochgeladene Bild
                progress_text = "OCR läuft"
                progressbar_ocr = colProgress.progress(0, text=progress_text)

                image_input_path = os.path.join(input_folder, input_image.name)  # Korrekt definierter Pfad
                image_name = input_image.name.split('.')[0]

                # OCR durchführen
                dfImage = ocr(image_input_path, image_name)
                # Filtern basierend auf Confidence Level und spezifischen Textinhalten
                dfImage = dfImage[dfImage['Confidence Level'] >= 0.5]
                dfImage = dfImage[dfImage['Namen'].apply(filter_text)]

                # Ergebnisse speichern
                csv_path = os.path.join(output_folder, f"{image_name}.csv")
                dfImage.to_csv(path_or_buf=csv_path)

                # Verschieben der Datei vom Eingabe- zum Verarbeitungsordner
                image_processed_path = os.path.join(processed_folder, input_image.name)
                shutil.move(image_input_path, image_processed_path)

                progressbar_ocr.progress(100, text=progress_text)
                st.toast('OCR erfolgreich durchgeführt, bitte output Verzeichnis prüfen.')
                disable_button_empty_dir(os.listdir(input_folder))
                time.sleep(5)
                progressbar_ocr.empty()

            # successful execution of OCR
            st.toast('OCR erfolgreich durchgeführt, bitte output Verzeichnis prüfen.')

elif selected=="Validierung":

    # two columns design
    st.subheader("Bilder")
    conValidation = st.container(border=True)
    colVal1,colVal2 = conValidation.columns((2,1))

    expander_images = colVal1.expander("Liste der Bilder", expanded=True)
    with expander_images:
        # image picker
        filesInFolders = os.listdir(processed_folder)
        dffilesInFolders = pd.DataFrame(filesInFolders,columns=['Datei'])
        dffilesInFolders["Name"]=dffilesInFolders["Datei"].str.split(".").str[0]
        dffilesInFolders["Typ"]=dffilesInFolders["Datei"].str.rsplit(".").str[-1]
        st.dataframe(dffilesInFolders["Name"],use_container_width=100)

    colVal2Button1, colVal2Button2 = colVal2.columns((2))

    if colVal2Button1.button("Zurück",use_container_width=15):
        if st.session_state['processed_index'] > 0:
            st.session_state['processed_index'] = st.session_state['processed_index'] - 1
        elif st.session_state['processed_index'] == 0:
            st.session_state['processed_index'] = 0
            st.toast("Anfang der Liste erreicht")
        else:
            st.session_state['processed_index'] = st.session_state['processed_index'] + 1
    if colVal2Button2.button("Vor",use_container_width=15):
        if st.session_state['processed_index'] == (len(dffilesInFolders) - 1):
            st.session_state['processed_index'] = (len(dffilesInFolders) - 1)

            st.toast("Ende der Liste erreicht")
        else:
            st.session_state['processed_index']=st.session_state['processed_index'] + 1



    #st.write(len(dffilesInFolders))
    # two column layout
    colImages, colNames = st.columns((2))
    colImages.subheader("Ausgewähltes Bild")
    conImages=colImages.container(border=True)
    #image_files = [f for f in os.listdir(processed_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    #selected_image = st.selectbox('Select an image:', image_files)
    #image_path = os.path.join(processed_folder, selected_image)
    # Anzeige des Bildes
    conImages.image(processed_folder, caption=processed_folder, use_column_width=True)

    # Get Names Data Frame
    if len(filesInFolders) > 0:

        # get values for validated and non validated csvs
        csv_name_validated = output_folder + validated_prefix
        if os.path.isfile(csv_name_validated):
            df_validated_names = pd.read_csv(csv_name_validated)
        else:
            df_validated_names = pd.DataFrame(columns=['Namen','Confidence Level','Bildname','bbox'])
            df_validated_names.to_csv(output_folder + validated_prefix,index=False)

        csv_name_non_validated = output_folder + filesInFolders[st.session_state['processed_index']].split(".")[0] + ".csv"
        if os.path.isfile(csv_name_non_validated):
            df_validated_non_validated_names = pd.read_csv(csv_name_non_validated)
        else:
            # Hier könnte eine Initialisierung fehlen, falls die Datei nicht existiert.
            df_validated_non_validated_names = pd.DataFrame(columns=['Namen','Confidence Level','Bildname','bbox'])

        # set image name to be checked
        image_name = filesInFolders[st.session_state['processed_index']].split(".")[0]

        # check if validated values exist, if yes take values fron validated csv else fron non validated

        # Überprüfung, ob 'Bildname' Spalte existiert
        if 'Bildname' in df_validated_names.columns and image_name in df_validated_names['Bildname'].values:
            image_name_list = [image_name]  # Direkte Nutzung des image_name ohne Split, es sei denn, Sie haben spezifische Gründe für den Split.
            df_selected_names = df_validated_names[df_validated_names['Bildname'].isin(image_name_list)]
            validated_values_exist = True
        else:
            df_selected_names = df_validated_non_validated_names
            validated_values_exist = False

        # if image_name in df_validated_names['Bildname'].values:
        #     image_name_list = image_name.split()
        #     df_selected_names = df_validated_names[df_validated_names.isin(image_name_list).any(axis=1)]
        #     validated_values_exist = True
        #
        # else:
        #     df_selected_names = df_validated_non_validated_names
        #     validated_values_exist = False


        # Get Image and enrich with rectagle and Name on image
        image = cv2.imread(processed_folder + filesInFolders[st.session_state['processed_index']])
        image_show = names_on_image(df_selected_names, image)
        conImages.image(image_show)

        selected_image = st.selectbox('Select an image:', filesInFolders, index=st.session_state['processed_index'])
        image_path = os.path.join(processed_folder, selected_image)
        # Button zum Öffnen des Bildes in der Windows-Bilderanzeige
        if st.button('Open in Windows Photo Viewer'):
            open_image(image_path)

        conImages.caption(filesInFolders[st.session_state['processed_index']])

        #conImages.image(processed_folder + filesInFolders[st.session_state['processed_index']], caption=filesInFolders[st.session_state['processed_index']])

        colNames.subheader("Namen")
        conNames=colNames.container(border=True)






        # transform capitalize words, e.g. first latter as capital folowing as lower case
        df_selected_names['Namen'] = df_selected_names['Namen'].apply(format_names)

        # change the final order of the columns
        df_for_update_names=conNames.data_editor(data=df_selected_names[['Namen','Confidence Level','Bildname','bbox']], num_rows='dynamic')

        if conNames.button("Validierte Namen speichern/updaten"):
            #print(image_name)
            if validated_values_exist:

                #image_name_list = list(filesInFolders[st.session_state['processed_index']])
                df_without_current_image = df_validated_names.loc[~df_validated_names.isin(image_name_list).any(axis=1)]

                df_final = pd.concat([df_without_current_image, df_for_update_names], ignore_index=True)
                df_final.to_csv(output_folder + image_name + '.csv',index=False)

            else:
                df_for_update_names.to_csv(output_folder + image_name + '.csv',index=False)

    else:
        st.toast("Keine Bilder im processed Verzeichnis für die Validierung")

elif selected=="Spende":
    st.write("##")
    donation=st.number_input(label='Spendenbeitrag', min_value=10)
    if st.button("Spende an Johann 🙃 😤 "):
        if donation < 15:
            st.toast('Oh wow: ' + str(donation) + '€, lieb von dir!',icon='😘')
        else:
            st.toast('Das ist stark, Mensch ' + str(donation) + '€, sehr sehr lieb von dir!',icon='😘')
            st.balloons()

elif selected=="Dynamics":
    st.write("##")
    agree = st.checkbox('Ist es schwer Checkboxen zu nutzen?')

    if agree:
        st.toast('Ne du, komm schon du kannst es auch. Ich glaube an dich 💪')

elif selected=="Settings":
    st.write("##")
    st.subheader("Verzeichnisse")

    colFolders, colSpace, colDescription = st.columns((6,1,4))

    user_input_input_folder = colFolders.text_input("Input", value=input_folder)
    user_input_output_folder = colFolders.text_input("Output", value=output_folder)
    user_input_processed_folder = colFolders.text_input("Processed", value=processed_folder)
    user_validated_prefix = colFolders.text_input("Validated File Prefix", value=validated_prefix)

    colDescription.caption("Verzeichnisse für den Prozess. Input für die Bilddateien. \
                 Im Output Verzeichnis landen die CSV Datein mit den Namen\
                 im Processed die prozessierten Bilddateien")

    st.write("##")
    if st.button("Settings speichern"):

        settingsFile = open('settings.json',"r")
        settings=json.load(settingsFile)

        # Open the JSON file for reading
        settings["Input"] = user_input_input_folder
        settings["Output"] = user_input_output_folder
        settings["Processed"] = user_input_processed_folder
        settings["Validated_Prefix"] = user_validated_prefix

        check_settings_directories(settings)

        # Write the updated data back to the JSON file
        with open('settings.json', 'w') as settingsFile:
            json.dump(settings, settingsFile)

        # Closing file
        settingsFile.close()