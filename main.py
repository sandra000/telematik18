#here must to be startpoint of application
#something like this
import matplotlib
matplotlib.use("TkAgg")

from ui.mainForm import SeaofBTCapp

app = SeaofBTCapp()
app.geometry("1280x720")
app.mainloop()
