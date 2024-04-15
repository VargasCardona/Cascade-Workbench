import dearpygui.dearpygui as dpg
import src.vision as vp

dpg.create_context()
dpg.setup_dearpygui()
dpg.create_viewport(title='Cascade Workbench',height = 750, width = 540)


def create_dialog(text: str):
       with dpg.window(label="Error", modal=True, show=True, tag="dialog", pos=((dpg.get_viewport_width() - 50) //2 - 20, dpg.get_viewport_height() - 50 //2), height=50):
           dpg.add_text(text)
           dpg.add_separator()
           with dpg.group(horizontal=True):
              dpg.add_button(label="OK", width=90, callback=lambda: dpg.delete_item("dialog"))

def callback(sender, app_data):
    global model_path
    global model_name
    global media_path
    global media_name
    global input_method
    
    if sender == "model_browser":
        path = app_data['selections']
        model_name = app_data['file_name']
        model_path = path[app_data['file_name']]
        dpg.set_value("selected_model", app_data['file_name'])

    elif sender == "media_browser":
        path = app_data['selections']
        media_name = app_data['file_name']
        media_path = path[app_data['file_name']]
        dpg.set_value("selected_media", app_data['file_name'])

    elif sender == "input_combo":
        input_method = app_data
        if input_method == "Webcam":
            dpg.configure_item("selected_media", show=False)
            dpg.configure_item("selected_media_text", show=False)
            dpg.configure_item("media_button_group", show=False)
            dpg.configure_item("model_selection", height=210)
        elif input_method == "Media":
            dpg.configure_item("selected_media", show=True)
            dpg.configure_item("selected_media_text", show=True)
            dpg.configure_item("media_button_group", show=True)
            dpg.configure_item("model_selection", height=251)

    elif sender == "view_model":
        if model_path == "":
            create_dialog("Missing Model Path")
            return
        if input_method == "":
            create_dialog("Missing Input method")
            return
        if input_method == "Media" and media_path == "":
            create_dialog("Missing Media Path")
            return

        renderer_thread = vp.ViewportRendererThread(update_viewport, get_viewport_dimentions, input_method, media_path, model_path)
        renderer_thread.start()
        dpg.configure_item("model_selection", show = False)
               
def update_viewport(frame):
  dpg.set_value("viewport", frame)

def get_viewport_dimentions(height, width):
    global viewport_height, viewport_width
    viewport_height = height
    viewport_width = width
    dpg.add_raw_texture(width, height, texture_data, tag="viewport", format=dpg.mvFormat_Float_rgb, parent="registry")

    with dpg.window(tag="main_viewport", label="Main Viewport", width=width+15, height=height+60, pos=(650,200), show=True):
           dpg.add_image("viewport")
           with dpg.group(horizontal=True):
               dpg.add_text("Current Model: ")
               dpg.add_text(model_name)

width, height, channels, data = dpg.load_image("media/haar.png")
model_path, model_name = "", ""
media_path, media_name = "", ""
viewport_height, viewport_width = 0, 0
input_method = ""
texture_data = []
for i in range(0, 100 * 100):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)
    texture_data.append(255 / 255)

with dpg.texture_registry(show=False, tag="registry"):
   dpg.add_raw_texture(260, 53, data, tag="logo")

with dpg.window(tag="model_selection", label="Cascade Workbench", no_close=True, no_collapse=True, no_resize=True, width=276, height=210, pos=(820, 420)):
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=75)
        dpg.add_text("Cascade Model")
    with dpg.group(horizontal=True):
        dpg.add_text("Selected Model: ")
        dpg.add_text("None", tag="selected_model")
    dpg.add_spacer(width=4)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=50)
        dpg.add_button(label="Browse Trained Model", callback=lambda : dpg.show_item("model_browser"))
    dpg.add_spacer(width=4)
    dpg.add_separator()
    dpg.add_spacer(width=4)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=65)
        dpg.add_text("Input Properties")
    with dpg.group(horizontal=True):
        dpg.add_text("Input Method: ")
        dpg.add_combo(label="None", tag="input_combo", default_value="None", items=["Media", "Webcam"], callback=callback)
    with dpg.group(horizontal=True):
        dpg.add_text("Selected Media: ", tag="selected_media_text", show=False)
        dpg.add_text("None", tag="selected_media", show=False)
    dpg.add_spacer(width=4, tag="media_spacer_1", show=False)
    with dpg.group(horizontal=True, tag="media_button_group", show=False):
        dpg.add_spacer(width=75)
        dpg.add_button(label="Browse Media", tag="media_button", callback=lambda : dpg.show_item("media_browser"))
    dpg.add_spacer(width=4, tag="media_spacer_2", show=False)
    dpg.add_separator()
    dpg.add_spacer(width=4)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=64)
        dpg.add_button(label="Visualize Model", tag="view_model", callback=callback)
    dpg.add_spacer(width=4)

with dpg.file_dialog(show=False, tag="model_browser", width=700 ,height=400, callback=callback):
    dpg.add_file_extension(".xml", color=(255, 255, 0, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="header")
    dpg.add_file_extension("Python(.py){.py}", color=(0, 255, 0, 255))

with dpg.file_dialog(show=False, tag="media_browser", width=700 ,height=400, callback=callback):
    dpg.add_file_extension(".mp4", color=(255, 255, 0, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="header")
    dpg.add_file_extension("Python(.py){.py}", color=(0, 255, 0, 255))

dpg.create_viewport(title='Cascade Workbench', width=1000, height=1000)
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
