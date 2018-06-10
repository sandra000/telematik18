#here must to be startpoint of application
#something like this
import matplotlib
matplotlib.use("TkAgg")

from ui import SeaofBTCapp


app = SeaofBTCapp()

 # run animate every 2 seconds; beware: while the app is updating, the app becomes frozen

app.geometry("1280x720")
app.mainloop()

# run animate every 2 seconds; beware: while the app is updating, the app becomes frozen
