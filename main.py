import matplotlib
matplotlib.use("TkAgg")
from ui import MainForm


app = MainForm()
app.geometry("1300x720")
app.resizable(width='false', height='true')
app.mainloop()
