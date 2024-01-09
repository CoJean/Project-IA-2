import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import random
import time


class Clock:
    def __init__(self, master):
        self.master = master
        self.time_label = tk.Label(master, font=("Arial", 20), text="")
        self.time_label.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="e")
        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)

class TemperatureDisplay:
    def __init__(self, master):
        self.master = master
        self.temperature_label = ttk.Label(self.master, text="Temperatura: ", font=("Helvetica", 14))
        self.temperature_label.grid(row=0, column=0, pady=5)

        self.temperature = 20
        self.update_temperature()

    def update_temperature(self):
        self.temperature += random.uniform(-0.5, 0.5)
        self.temperature_label["text"] = f"Temperatura: {self.temperature:.2f} °C"
        self.master.after(5000, self.update_temperature)


class HomeAssistantSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Assistant Simulator")


        self.root.geometry("1024x960")

        #  afișarea stării alarmei
        self.status_panel = ttk.Label(self.root, text="Status: Disarmed", font=("Helvetica", 16))
        self.status_panel.grid(row=0, column=0, columnspan=3, pady=10)

        # Buton armare în mod "away"
        self.arm_away_button = ttk.Button(self.root, text="Arm Away", command=self.arm_away)
        self.arm_away_button.grid(row=1, column=0, pady=10)


        # Buton armare în mod "home"
        self.arm_home_button = ttk.Button(self.root, text="Arm Home", command=self.arm_home)
        self.arm_home_button.grid(row=1, column=1, pady=5)

        # Buton dezarmare
        self.disarm_button = ttk.Button(self.root, text="Disarm", command=self.disarm)
        self.disarm_button.grid(row=1, column=2, pady=5)

        # Buton deschiderea paginii cu lumini
        self.lumini_button = ttk.Button(self.root, text="Lumini", command=self.open_lumini_page)
        self.lumini_button.grid(row=2, column=0, columnspan=1, pady=5)

        # Buton Aspirator
        self.aspirator_button = ttk.Button(self.root, text="Aspirator", command=self.open_aspirator_page)
        self.aspirator_button.grid(row=2, column=1, pady=5)

        # Caseta de text pentru mesaje
        self.message_text = tk.Text(self.root, height=50, width=170)
        self.message_text.grid(row=3, column=0, columnspan=3, pady=10)

        # Variabile pentru a ține evidența stării aspiratorului
        self.aspirator_running = False
        self.current_aspirator_location = None
        self.aspirator_location_update_id = None

        # Dicționar pentru a ține evidența stării luminilor în fiecare cameră
        self.lights_status = {
            "Bucatarie": False,
            "Dormitor": False,
            "Living": False,
            "Baie": False
        }

        # Create clock instance
        self.clock = Clock(self.root)

        # Instanțierea și plasarea obiectului TemperatureDisplay
        self.temperature_display = TemperatureDisplay(self.root)
        self.temperature_display.temperature_label.grid(row=0, column=0, pady=5)



    def arm_away(self):
        self.status_panel["text"] = "Status: Armed Away"
        self.log_message("Armed Away")

    def arm_home(self):
        self.status_panel["text"] = "Status: Armed Home"
        self.log_message("Armed Home")

    def disarm(self):
        self.status_panel["text"] = "Status: Disarmed"
        self.log_message("Disarmed")

    def open_lumini_page(self):
        lumini_window = tk.Toplevel(self.root)
        lumini_window.title("Lumini Control")

        # Adaugă butoane pentru controlul luminilor în diverse camere
        lumina_camera1_button = ttk.Button(lumini_window, text="Bucatarie", command=lambda: self.control_lights("Bucatarie"))
        lumina_camera1_button.grid(row=0, column=0, pady=5)
        self.create_lights_status_labels(lumini_window, "Bucatarie", row=0, column=1)

        lumina_camera2_button = ttk.Button(lumini_window, text="Dormitor", command=lambda: self.control_lights("Dormitor"))
        lumina_camera2_button.grid(row=1, column=0, pady=5)
        self.create_lights_status_labels(lumini_window, "Dormitor", row=1, column=1)

        lumina_camera3_button = ttk.Button(lumini_window, text="Living", command=lambda: self.control_lights("Living"))
        lumina_camera3_button.grid(row=2, column=0, pady=5)
        self.create_lights_status_labels(lumini_window, "Living", row=2, column=1)

        lumina_camera4_button = ttk.Button(lumini_window, text="Baie", command=lambda: self.control_lights("Baie"))
        lumina_camera4_button.grid(row=3, column=0, pady=5)
        self.create_lights_status_labels(lumini_window, "Baie", row=3, column=1)

    def create_lights_status_labels(self, window, room, row, column):
        # Etichetă pentru afișarea stării luminilor într-o cameră
        label_text = f"Stare lumină: {'Pornită' if self.lights_status[room] else 'Oprită'}"
        lights_status_label = ttk.Label(window, text=label_text)
        lights_status_label.grid(row=row, column=column, pady=5)

        # Buton pentru a afișa starea luminilor în cameră
        show_status_button = ttk.Button(window, text="Afișează Stare", command=lambda: self.show_lights_status(room, lights_status_label))
        show_status_button.grid(row=row, column=column + 1, pady=5)

    def show_lights_status(self, room, label):
        label["text"] = f"Stare lumină: {'Pornită' if self.lights_status[room] else 'Oprită'}"

    def open_aspirator_page(self):
        aspirator_window = tk.Toplevel(self.root)
        aspirator_window.title("Aspirator Control")


        # Buton pentru pornirea aspiratorului
        self.aspirator_on_button = ttk.Button(aspirator_window, text="ON", command=self.start_aspirator)
        self.aspirator_on_button.pack(pady=10)

        # Buton pentru oprirea aspiratorului
        self.aspirator_off_button = ttk.Button(aspirator_window, text="OFF", command=self.stop_aspirator)
        self.aspirator_off_button.pack(pady=10)

        # Buton pentru schimbarea locației aspiratorului
        self.aspirator_location_button = ttk.Button(aspirator_window, text="Afla Locație", command=self.change_aspirator_location)
        self.aspirator_location_button.pack(pady=10)

        # Etichetă pentru afișarea locației curente a aspiratorului
        self.aspirator_location_label = ttk.Label(aspirator_window, text="")
        self.aspirator_location_label.pack(pady=10)

    def start_aspirator(self):
        self.aspirator_running = True
        self.log_message("Aspirator pornit")
        # Porneste schimbarea automata a locatiei
        self.change_aspirator_location()

    def stop_aspirator(self):
        self.aspirator_running = False
        self.log_message("Aspirator oprit")
        # Anuleaza programarea schimbarii automate a locatiei
        if self.aspirator_location_update_id is not None:
            self.root.after_cancel(self.aspirator_location_update_id)

    def change_aspirator_location(self):
        if self.aspirator_running:
            locations = ["Living", "Bucătărie", "Dormitor", "Baie"]
            random_location = random.choice(locations)
            self.current_aspirator_location = random_location
            self.aspirator_location_label["text"] = f"Locație curentă: {self.current_aspirator_location}"
            self.log_message(f"Locație curentă a aspiratorului: {self.current_aspirator_location}")
            # Programam urmatoarea schimbare dupa 5 secunde
            self.aspirator_location_update_id = self.root.after(5000, self.change_aspirator_location)

    def control_lights(self, room):
        # Invert the lights status for the room
        self.lights_status[room] = not self.lights_status[room]
        self.log_message(f"Starea luminilor în {room}: {'Pornită' if self.lights_status[room] else 'Oprită'}")

    def log_message(self, message):
        self.message_text.insert(tk.END, message + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeAssistantSimulator(root)
    root.mainloop()
