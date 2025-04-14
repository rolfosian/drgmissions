import json
from tkinter import Tk, Label, Button, Listbox, SINGLE, END, messagebox, Scrollbar, Text, HORIZONTAL, VERTICAL, RIGHT, Y, LEFT, BOTH, Frame, Checkbutton, IntVar, Canvas, font
from itertools import combinations
import os
import subprocess

# Searches given dataset of drgmissionsgod.json for possible mission configurations given by user

with open("drgmissionsgod.json", "r") as f:
    DRG = json.load(f)

def with_specials(base):
    return ["None", "All"] + base

valid_biomes = ['Glacial Strata', 'Crystalline Caverns', 'Salt Pits', 'Magma Core', 'Azure Weald', 
                'Sandblasted Corridors', 'Fungus Bogs', 'Radioactive Exclusion Zone', 'Dense Biozone', 'Hollow Bough']

valid_secondaries = sorted(['Dystrum', 'Glyphid Eggs', 'ApocaBlooms', 'Hollomite', 'Fossils',
                            'Ebonuts', 'Gunk Seeds', 'Boolo Caps', 'Fester Fleas', 'Bha Barnacles'], key=lambda x: (str.isdigit(x), x.lower()))

valid_primaries = sorted(['Deep Scan', 'Escort Duty', 'Elimination', 'Industrial Sabotage', 'Mining Expedition',
                          'Salvage Operation', 'On-Site Refining', 'Point Extraction', 'Egg Hunt'], key=lambda x: (str.isdigit(x), x.lower()))

valid_mutators = with_specials(sorted(['Gold Rush', 'Blood Sugar', 'Critical Weakness', 'Rich Atmosphere', 'Golden Bugs', 'Double XP',
                                       'Low Gravity', 'Secret Secondary', 'Volatile Guts', 'Mineral Mania'], key=lambda x: (str.isdigit(x), x.lower())))

valid_warnings = with_specials(sorted(['Cave Leech Cluster', 'Parasites', 'Mactera Plague', 'Low Oxygen', 'Exploder Infestation', 'Rival Presence', 
                                       'Shield Disruption', 'Lithophage Outbreak', 'Haunted Cave', 'Regenerative Bugs', 'Lethal Enemies', 'Swarmageddon', 
                                       'Elite Threat', 'Ebonite Outbreak', 'Duck and Cover'], key=lambda x: (str.isdigit(x), x.lower())))

valid_lengths = ["1", "2", "3"]
valid_complexities = ["1", "2", "3"]

class SoughtConfig(dict):
    def __init__(self):
        super().__init__()
        self["Wanted Biomes"] = []
        self["Wanted Primaries"] = []
        self["Wanted Secondaries"] = []
        self["Wanted Mutators"] = []
        self["Wanted Warnings"] = []
        self["Wanted Lengths"] = []
        self["Wanted Complexities"] = []

def match_field(value, field):
    if "All" in field:
        return True
    if "None" in field:
        if not value:
            return True
        else:
            return False
    return value in field

non = ['None']
def match_list_field(values, field):
    if "All" in field:
        return True
    if not values and field == non:
        return True
    if values:
        if "All" in field:
            return True
        if "None" in field:
            return False
        if len(field) == 2:
             target = set(values)
             return all(set(pair) == target for pair in combinations(field, 2))
        else:
            return any(v in values for v in field)

def find_mission(sought_config:dict, results:list, timestamp:str, dict:dict) -> None:
    for biome, missions in dict["Biomes"].items():
        if match_field(biome, sought_config["Wanted Biomes"]):
            for mission in missions:
                primary = mission.get("PrimaryObjective")
                secondary = mission.get("SecondaryObjective")
                complexity = mission.get("Complexity")
                length = mission.get("Length")
                mutator = mission.get("MissionMutator", None)
                warnings = mission.get("MissionWarnings", [])

                if not all([
                match_field(primary, sought_config["Wanted Primaries"]),
                match_field(secondary, sought_config["Wanted Secondaries"]),
                match_field(complexity, sought_config["Wanted Complexities"]),
                match_field(length, sought_config["Wanted Lengths"]),
                match_field(mutator, sought_config["Wanted Mutators"]),
                match_list_field(warnings, sought_config["Wanted Warnings"])
                ]):
                    # print("FAIL", mission)
                    # print(sought_config["Wanted Warnings"])
                    continue
                # else:
                    # print("PASS", timestamp, len(missions), mission)
                results.append([timestamp, biome, mission])
                # if len(results) > 200:
                #     quit()

def main():
    root = Tk()
    root.title("DRG Mission Finder")
    root.iconbitmap("./static/favicon.ico")

    master_canvas = Canvas(root)
    master_canvas.grid(row=0, column=0, sticky="nsew")

    v_scroll = Scrollbar(root, orient=VERTICAL, command=master_canvas.yview)
    v_scroll.grid(row=0, column=1, sticky="ns")

    h_scroll = Scrollbar(root, orient=HORIZONTAL, command=master_canvas.xview)
    h_scroll.grid(row=1, column=0, sticky="ew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    master_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    content_frame = Frame(master_canvas)
    master_canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_configure(event):
        master_canvas.configure(scrollregion=master_canvas.bbox("all"))

    content_frame.bind("<Configure>", on_configure)

    def _on_mousewheel(event):
        master_canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")

    def _on_shiftmousewheel(event):
        master_canvas.xview_scroll(int(-1 * (event.delta / 60)), "units")

    # content_frame.bind("<Enter>", lambda e: (
    #     root.bind_all("<MouseWheel>", _on_mousewheel),
    #     root.bind_all("<Shift-MouseWheel>", _on_shiftmousewheel)
    # ))
    # content_frame.bind("<Leave>", lambda e: (
    #     root.unbind_all("<MouseWheel>"),
    #     root.unbind_all("<Shift-MouseWheel>")
    # ))
    
    sought_configs = []
    current_config = SoughtConfig()

    combo_data = {
        "Biomes": valid_biomes,
        "Primaries": valid_primaries,
        "Secondaries": valid_secondaries,
        "Mutators": valid_mutators,
        "Warnings": valid_warnings,
        "Lengths": valid_lengths,
        "Complexities": valid_complexities
    }

    check_vars = {}

    left_frame = Frame(content_frame)
    left_frame.grid(row=0, column=0, rowspan=20, padx=5, sticky="ns")

    for idx, (label, values) in enumerate(combo_data.items()):
        Label(left_frame, text=label).pack(anchor="w", pady=5)
        subframe = Frame(left_frame)
        subframe.pack()
        canvas = Canvas(subframe, height=100)
        scrollbar = Scrollbar(subframe, orient=VERTICAL, command=canvas.yview)
        scroll_frame = Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH)
        scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event, c=canvas):
            c.yview_scroll(int(-1 * (event.delta / 60)), "units")

        canvas.bind("<Enter>", lambda e, c=canvas: c.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, c)))
        canvas.bind("<Leave>", lambda e, c=canvas: c.unbind_all("<MouseWheel>"))

        check_vars[label] = {}

        def make_toggle_handler(this_label, this_val):
            def toggle():
                vars_group = check_vars[this_label]
                if this_val in ("All", "None") and vars_group[this_val].get():
                    for other_val, var in vars_group.items():
                        if other_val != this_val:
                            var.set(0)
                elif this_val not in ("All", "None") and vars_group.get("All", vars_group.get("None")) and (vars_group.get("All", IntVar()).get() or vars_group.get("None", IntVar()).get()):
                    if "All" in vars_group:
                        vars_group["All"].set(0)
                    if "None" in vars_group:
                        vars_group["None"].set(0)
            return toggle

        all_label = "None" if "None" in values else "All"
        values = [v for v in values if v not in ("All", "None")]
        if "None" in values or all_label == "None":
            values = ["All", "None"] + values
        else:
            values = ["All"] + values
            
        for val in values:
            var = IntVar(value=1 if val == "All" else 0)
            cb = Checkbutton(scroll_frame, text=val, variable=var, command=make_toggle_handler(label, val))
            cb.pack(anchor="w")
            check_vars[label][val] = var

    def gather_current_config():
        for key in combo_data:
            current_config[f"Wanted {key}"] = [val for val, var in check_vars[key].items() if var.get() == 1]

    def add_current_config(insert=None):
        gather_current_config()
        copy_cfg = SoughtConfig()
        for key in current_config:
            copy_cfg[key] = list(current_config[key])
        sought_configs.append(copy_cfg) if not isinstance(insert, int) else sought_configs.insert(insert, copy_cfg)
        update_config_list()
        for group in check_vars.values():
            for i, var in enumerate(group.values()):
                var.set(1) if i == 0 else var.set(0)
        
        size = config_listbox.size()
        if size == 1:
            config_listbox.selection_set(0)
            display_selected_config(None)
        elif isinstance(insert, int):
            config_listbox.selection_set(insert)
            display_selected_config(None)
        else:
            config_listbox.selection_set(size-1)
            display_selected_config(None)

    def update_config_list():
        config_listbox.delete(0, END)
        for i, cfg in enumerate(sought_configs):
            config_listbox.insert(END, f"Config {i+1}")

    def remove_selected_config():
        selected = config_listbox.curselection()
        if selected:
            del sought_configs[selected[0]]
            update_config_list()
            config_listbox.selection_set(config_listbox.size()-1)
            display_selected_config(None)
    
    def edit_selected_config():
        selected = config_listbox.curselection()
        if selected:
            index = selected[0]
            gather_current_config()
            remove_selected_config()
            add_current_config(insert=index)
            

    def display_selected_config(evt):
        selected = config_listbox.curselection()
        if selected:
            cfg = sought_configs[selected[0]]
            config_text.config(state="normal")
            config_text.delete("1.0", END)
            config_text.insert(END, json.dumps(cfg, indent=4))
            config_text.config(state="disabled")
        else:
            config_text.config(state="normal")
            config_text.delete("1.0", END)
            config_text.config(state="disabled")
            
    add_button_frame = Frame(content_frame)
    add_button_frame.grid(row=0, column=1)
    
    Button(add_button_frame, text="Add New Mission Combinations to look for", command=add_current_config).grid(row=0, column=1)
    Button(add_button_frame, text="Edit Selected Mission Combinations", command=edit_selected_config).grid(row=0, column=0)

    config_listbox = Listbox(content_frame, height=10)
    config_listbox.grid(row=1, column=1)
    config_listbox.bind("<<ListboxSelect>>", display_selected_config)

    def clear_config_list():
        sought_configs.clear()
        update_config_list()
        config_text.config(state="normal")
        config_text.delete("1.0", END)
        config_text.config(state="disabled")

    removal_button_frame = Frame(content_frame)
    removal_button_frame.grid(row=2, column=1)

    Button(removal_button_frame, text="Remove Selected Config", command=remove_selected_config).pack(side=LEFT, padx=5)
    Button(removal_button_frame, text="Clear Config List", command=clear_config_list).pack(side=LEFT, padx=5)

    config_text = Text(content_frame, bg="black", fg="white", font=font.Font(family="Courier New", size=10, weight="bold"), cursor="arrow", height=30, width=60)
    config_text.grid(row=3, column=1, rowspan=10)
    config_text.config(state="disabled")

    config_text_scrollbar = Scrollbar(content_frame, orient=VERTICAL, command=config_text.yview)
    config_text_scrollbar.grid(row=3, column=2, rowspan=10, sticky='ns')
    config_text.config(yscrollcommand=config_text_scrollbar.set)

    class SearchButton(Button):
        def __init__(self, master, DRG, sought_configs, **kwargs):
            super().__init__(master, **kwargs)
            self.DRG = DRG
            self.sought_configs = sought_configs
            self.config(command=self._run_search)

        def _run_search(self):
            self.config(state="disabled")
            results = []
            results_ = {}

            for timestamp, dict in self.DRG.items():
                for cfg in self.sought_configs[:]:
                    find_mission(cfg, results, timestamp, dict)

            if results:
                for timestamp, biome, mission in results:
                    if timestamp not in results_:
                        results_[timestamp] = {}
                    if biome not in results_[timestamp].keys():
                        results_[timestamp][biome] = []
                    results_[timestamp][biome].append(mission)
                
                config_text.delete("1.0", END)

                with open("mission_finder_results.json", "w") as f:
                    f.write(json.dumps(results_, indent=2))
                    
                if os.name == "nt":
                    subprocess.Popen("notepad.exe mission_finder_results.json", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                else:
                    subprocess.Popen('TERMINAL=$(command -v x-terminal-emulator || command -v gnome-terminal || command -v konsole || command -v xfce4-terminal || command -v lxterminal || command -v xterm); [ -n "$TERMINAL" ] && "$TERMINAL" -e nano mission_finder_results.json', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                self.config(state="normal")
            
            else:
                messagebox.showerror("Uhhhh", "No missions found under parameters. Either they aren't possible combinations in the game, or the dataset isn't large enough and it's unlucky.")
                self.config(state="normal")

    search_button = SearchButton(content_frame, DRG, sought_configs, text="SEARCH")
    search_button.grid(row=13, column=1)
    
    root.geometry("1200x1000+0+0")
    root.mainloop()

if __name__ == "__main__":
    main()