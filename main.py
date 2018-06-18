import matplotlib
matplotlib.use("TkAgg")
from ui import MainForm


app = MainForm()
app.geometry("1280x720")
app.mainloop()
