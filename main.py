#!/usr/bin/python3
import pathlib
from tkinter import END

import pygubu
import ttkbootstrap as ttk
from PIL import ImageGrab
from ttkbootstrap import PRIMARY, Style, SUCCESS, INFO, SECONDARY, WARNING
from ttkbootstrap.toast import ToastNotification

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "main.ui"


class MainApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("main", master)
        builder.connect_callbacks(self)
        style = Style("cyborg")
        self.frequencies_tv = builder.get_object("frequencies_tv")
        self.scrollbar1 = builder.get_object("scrollbar1")
        self.scrollbar1.configure(command=self.frequencies_tv.yview, bootstyle=SUCCESS)
        self.frequencies_tv.configure(yscrollcommand=self.scrollbar1.set, bootstyle=SUCCESS)
        self.frequencies_tv.bind("<Double-1>", self.on_fx_click)
        self.frequencies_tv.tag_configure('-10', background='#224400')
        self.frequencies_tv.tag_configure('-20', background='#335500')
        self.frequencies_tv.tag_configure('-30', background='#446600')

        self.bandscan_tv = builder.get_object("bandscan_tv")
        self.scrollbar2 = builder.get_object("scrollbar2")
        self.scrollbar2.configure(command=self.bandscan_tv.yview, bootstyle=SUCCESS)
        self.bandscan_tv.configure(yscrollcommand=self.scrollbar2.set, bootstyle=SUCCESS)
        self.bandscan_tv.tag_configure('-10', background='#224400')
        self.bandscan_tv.tag_configure('-20', background='#335500')
        self.bandscan_tv.tag_configure('-30', background='#446600')

        self.fx_entry = builder.get_object("fx_entry")
        self.query_entry = builder.get_object("query_entry")
        self.query_entry.focus_set()
        self.query_entry.bind("<Return>", self.on_fx_search)
        self.nation_entry = builder.get_object("nation_entry")
        self.port_entry = builder.get_object("port_entry")
        self.prov_entry = builder.get_object("prov_entry")
        self.lat_entry = builder.get_object("lat_entry")
        self.long_entry = builder.get_object("long_entry")
        self.ps_entry = builder.get_object("ps_entry")
        self.pi_entry = builder.get_object("pi_entry")
        self.idx_progress = builder.get_object("idx_progress")
        self.idx_progress.configure(bootstyle=SUCCESS)
        self.add_btn = builder.get_object("add_btn")
        self.add_btn.configure(bootstyle=SUCCESS)
        self.dist_entry = builder.get_object("dist_entry")
        self.bandscan_tab = builder.get_object("bandscan_tab")
        self.main_notebook = builder.get_object("main_notebook")

        self.index = 0

        self.on_load()

    def run(self):
        self.mainwindow.mainloop()

    def on_load(self):
        self.frequencies_tv.delete(*self.frequencies_tv.get_children())
        with open("userlist1.csv", "r") as userlist:
            frequencies = userlist.read().splitlines()
            for fx in frequencies[9:]:
                fx = fx.split(",")
                try:
                    freq = float(fx[0])/1000
                    freq = "%.2f" % freq
                    if int(fx[13]) >= -10:
                        tag = '-10'
                    elif int(fx[13]) > -20 < -10:
                        tag = '-20'
                    else:
                        tag = '-30'
                    values = (freq, fx[1], fx[3], fx[5], fx[14], fx[15], fx[11], fx[13])
                    self.frequencies_tv.insert("", END, values=values, tag=tag)
                except IndexError:
                    pass
                except ValueError:
                    pass

    def on_fx_search(self, event=None):
        query = self.query_entry.get()
        if query != "":
            query = query.replace(",", ".")
            query = str(int(float(query) * 1000))
            self.frequencies_tv.delete(*self.frequencies_tv.get_children())
            self.frequencies_tv.yview_moveto(0)
            with open("userlist1.csv", "r") as userlist:
                frequencies = userlist.read().splitlines()
                for fx in frequencies[9:]:
                    fx = fx.split(",")
                    if fx[0] == query:
                        try:
                            freq = float(fx[0])/1000
                            freq = "%.2f" % freq
                            if int(fx[13]) >= -10:
                                tag = '-10'
                            elif int(fx[13]) > -20 < -10:
                                tag = '-20'
                            else:
                                tag = '-30'
                            values = (freq, fx[1], fx[3], fx[5], fx[14], fx[15], fx[11], fx[13])
                            self.frequencies_tv.insert("", END, values=values, tag=tag)
                        except IndexError:
                            pass
                        except ValueError:
                            pass
        else:
            self.on_load()

    def on_fx_click(self, event=None):
        self.fx_entry.delete(0, END)
        self.port_entry.delete(0, END)
        self.nation_entry.delete(0, END)
        self.prov_entry.delete(0, END)
        self.lat_entry.delete(0, END)
        self.long_entry.delete(0, END)
        self.ps_entry.delete(0, END)
        self.pi_entry.delete(0, END)
        self.dist_entry.delete(0, END)
        value = self.frequencies_tv.focus()
        query = self.frequencies_tv.item(value)['values'][0]
        port = self.frequencies_tv.item(value)['values'][2]
        prov = self.frequencies_tv.item(value)['values'][3]
        query = str(int(float(query) * 1000))
        with open("userlist1.csv", "r") as userlist:
            frequencies = userlist.read().splitlines()
            for fx in frequencies[9:]:
                fx = fx.split(",")
                if fx[0] == query and fx[3] == port and fx[5] == prov:
                    try:
                        freq = float(fx[0])/1000
                        freq = "%.2f" % freq
                        self.fx_entry.insert(0, freq)
                        self.port_entry.insert(0, fx[3])
                        self.nation_entry.insert(0, fx[1])
                        self.prov_entry.insert(0, fx[5])
                        self.lat_entry.insert(0, fx[6])
                        self.long_entry.insert(0, fx[7])
                        self.ps_entry.insert(0, fx[14])
                        self.pi_entry.insert(0, fx[15])
                        self.dist_entry.insert(0, fx[11])
                        idx = int(fx[13])+40
                        self.index = fx[13]
                        self.idx_progress.configure(value=idx)
                        self.main_notebook.select(0)

                    except IndexError:
                        pass
                    except ValueError:
                        pass

    def on_bs_add_press(self):
        fx = self.fx_entry.get()
        nation = self.nation_entry.get()
        port = self.port_entry.get()
        prov = self.prov_entry.get()
        ps = self.ps_entry.get()
        pi = self.pi_entry.get()
        dist = self.dist_entry.get()
        index = self.index
        if float(fx) < 100:
            fx = f"0{fx}"
        values = [fx, nation, port, prov, ps, str(pi), dist, str(index)]
        if int(index) >= -10:
            tag = '-10'
        elif int(index) > -20 < -10:
            tag = '-20'
        else:
            tag = '-30'
        check = self.search(values)
        if not check:
            self.bandscan_tv.insert("", END, values=values, tag=tag)
            self.sort()
            self.main_notebook.select(1)
        self.fx_entry.delete(0, END)
        self.port_entry.delete(0, END)
        self.nation_entry.delete(0, END)
        self.prov_entry.delete(0, END)
        self.lat_entry.delete(0, END)
        self.long_entry.delete(0, END)
        self.ps_entry.delete(0, END)
        self.pi_entry.delete(0, END)
        self.dist_entry.delete(0, END)

    def sort(self):
        rows = [(self.bandscan_tv.set(item, 'column9').lower(), item) for item in self.bandscan_tv.get_children('')]
        rows.sort()

        for index, (values, item) in enumerate(rows):
            self.bandscan_tv.move(item, '', index)

    def search(self, value):
        for child in self.bandscan_tv.get_children():
            if value[0] == self.bandscan_tv.item(child)['values'][0] \
                    and value[2] == self.bandscan_tv.item(child)['values'][2]\
                    and value[3] == self.bandscan_tv.item(child)['values'][3]:
                toast = ToastNotification(
                    title="Frequenza già censita",
                    message="La portante selezionata su questa frequenza è già stata registrata",
                    duration=5000,
                    icon="🤨",
                    bootstyle=SUCCESS
                )
                toast.show_toast()
                return True
            else:
                return False

    def on_close_press(self):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.run()
