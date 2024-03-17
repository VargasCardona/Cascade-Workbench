import dearpygui.dearpygui as dpg
import src.vision as vp

dpg.create_context()
dpg.setup_dearpygui()
dpg.create_viewport(title='Cascade Workbench',height = 750, width = 540)

def callback(sender, app_data):
    global model_path
    global model_name
    
    if sender == "file_dialog_id":
        path = app_data['selections']
        model_name = app_data['file_name']
        model_path = path[app_data['file_name']]
        dpg.set_value("selected_model", app_data['file_name'])
    elif sender == "view_model":
        dpg.configure_item("model_selection", show = False)
        dpg.configure_item("main_viewport", show = True)
        renderer_thread = vp.ViewportRendererThread(update_viewport, model_path)
        renderer_thread.start()
        dpg.set_value("model_name", model_name)

def update_viewport(frame):
  dpg.set_value("viewport", frame)

width, height, channels, data = dpg.load_image("media/haar.png")
model_path = ""
model_name = ""
texture_data = []
for i in range(0, 100 * 100):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)
    texture_data.append(255 / 255)

with dpg.texture_registry(show=False):
   dpg.add_raw_texture(640, 480, texture_data, tag="viewport", format=dpg.mvFormat_Float_rgb)
   dpg.add_raw_texture(260, 53, data, tag="logo")

with dpg.window(tag="main_viewport", label="Main Viewport", width=645, height=540, pos=(650,200), show=False):
       dpg.add_image("viewport")
       with dpg.group(horizontal=True):
           dpg.add_text("Current Model: ")
           dpg.add_text("", tag = "model_name")

with dpg.window(tag="model_selection", label="Model Selection", no_close=True, no_collapse=True, no_resize=True, width=284, height=170, pos=(820, 420)):
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=65)
        dpg.add_text("Cascade Workbench")
    dpg.add_spacer(width=4)
    with dpg.group(horizontal=True):
        dpg.add_image("logo")
    dpg.add_spacer(width=4)
    with dpg.group(horizontal=True):
        dpg.add_text("Selected Model: ")
        dpg.add_text("", tag="selected_model")
    dpg.add_spacer(width=4)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Browse Trained Model", callback=lambda : dpg.show_item("file_dialog_id"))
        dpg.add_spacer(width=22)
        dpg.add_button(label="Visualize", tag="view_model", callback=callback)

with dpg.file_dialog(show=False, tag="file_dialog_id", width=700 ,height=400, callback=callback):
    dpg.add_file_extension(".xml", color=(255, 255, 0, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="header")
    dpg.add_file_extension("Python(.py){.py}", color=(0, 255, 0, 255))

dpg.create_viewport(title='Cascade Workbench', width=1000, height=1000)
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
