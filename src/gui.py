import dearpygui.dearpygui as dpg
import src.vision as vp

dpg.create_context()
dpg.setup_dearpygui()
dpg.create_viewport(title='Inversion Final',height = 750, width = 540)

def update_viewport(frame):
  dpg.set_value("texture_tag", frame)

def _log(sender, app_data, user_data):
    pass

texture_data = []
for i in range(0, 100 * 100):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)
    texture_data.append(255 / 255)

with dpg.texture_registry(show=False):
   dpg.add_raw_texture(640, 480, texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)

with dpg.window(label="Main Viewport", width=525, height=518, pos=(500,100)):
     dpg.add_image("texture_tag")

renderer_thread = vp.ViewportRendererThread(update_viewport, "cascade")
renderer_thread.start()

dpg.create_viewport(title='Cascade Workbench', width=1000, height=1000)
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
