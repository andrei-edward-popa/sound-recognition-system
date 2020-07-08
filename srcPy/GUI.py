import tkinter as tk
import os
import RecognitionGUI
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageTk, Image

os.chdir('/home/apopa/Facultate/Licenta/srcPy')
os.system('gnome-terminal -- bash -c "sudo minicom -b 921600 -D /dev/ttyACM0 -C /home/apopa/Desktop/test; exec bash"')
classification_algorithm = None

def plot_MAD():
    window = tk.Toplevel(root)
    window.geometry('1400x700+200+100')
    window.title('Music Activity')
    window.resizable(False,False)
    window.state('normal')
    window.config(background='#fafafa')
                  
    RecognitionGUI.m_MAD = []
    xar = []
    yar = []
    index = [0]
                  
    style.use('ggplot')
    fig = plt.figure(figsize=(14, 4.5), dpi=100)
    plt.close(fig)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylim(0, 17)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Music Activity')
    
    line, = ax1.plot(xar, yar, 'r', marker='x', label='value > 4 => speech\nvalue <= 4 => instrument')
    line2, = ax1.plot(xar, yar, 'k')
    
    def animate(i):
        y = RecognitionGUI.m_MAD
        x = list(np.linspace(index[0], index[0] + len(y) * 0.48, len(y)))
        if len(y) == 105:
            index[0] += 0.48
            RecognitionGUI.m_MAD.pop(0)
        line.set_data(np.array(x), np.array(y))
        if len(x) == 0:
            ax1.set_xlim(0, 1)
        else:
            ax1.set_xlim(index[0], x[-1] + 0.5)
            line2.set_data([index[0], x[-1] + 0.5], [4,4])
        ax1.legend()

    plotcanvas = FigureCanvasTkAgg(fig, window)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
    
    window.mainloop()
    
def plot_energy_entropy():
    window = tk.Toplevel(root)
    window.geometry('1400x700+200+100')
    window.title('Energy Entropy')
    window.resizable(False,False)
    window.state('normal')
    window.config(background='#fafafa')
                  
    RecognitionGUI.m_EE = []
    xar = []
    yar = []
    index = [0]
                  
    style.use('ggplot')
    fig = plt.figure(figsize=(14, 4.5), dpi=100)
    plt.close(fig)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylim(2.8, 3.7)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Energy Entropy')
    line, = ax1.plot(xar, yar, 'r', marker='x', label='value > 3.35 => female\nvalue <= 3.35 => male\nvalue >=3.5 => instrument')
    line2, = ax1.plot(xar, yar, 'k')
    
    def animate(i):
        y = RecognitionGUI.m_EE
        x = list(np.linspace(index[0], index[0] + len(y) * 0.48, len(y)))
        if len(y) == 105:
            index[0] += 0.48
            RecognitionGUI.m_EE.pop(0)
        line.set_data(np.array(x), np.array(y))
        if len(x) == 0:
            ax1.set_xlim(0, 1)
        else:
            ax1.set_xlim(index[0], x[-1] + 0.5)
            line2.set_data([index[0], x[-1] + 0.5], [3.35,3.35])
        ax1.legend()

    plotcanvas = FigureCanvasTkAgg(fig, window)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
    
    window.mainloop()
    
def plot_F0():
    window = tk.Toplevel(root)
    window.geometry('1400x700+200+100')
    window.title('Fundamental Frequency')
    window.resizable(False,False)
    window.state('normal')
    window.config(background='#fafafa')
                  
    RecognitionGUI.m_F0 = []
    xar = []
    yar = []
    index = [0]
                  
    style.use('ggplot')
    fig = plt.figure(figsize=(14, 4.5), dpi=100)
    plt.close(fig)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylim(50, 300)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Fundamental Frequency')
    line, = ax1.plot(xar, yar, 'r', marker='x', label='value >= 170 => female\nvalue < 170 => male')
    line2, = ax1.plot(xar, yar, 'k')
    
    def animate(i):
        y = RecognitionGUI.m_F0
        x = list(np.linspace(index[0], index[0] + len(y) * 0.48, len(y)))
        if len(y) == 105:
            index[0] += 0.48
            RecognitionGUI.m_F0.pop(0)
        line.set_data(np.array(x), np.array(y))
        if len(x) == 0:
            ax1.set_xlim(0, 1)
        else:
            ax1.set_xlim(index[0], x[-1] + 0.5)
            line2.set_data([index[0], x[-1] + 0.5], [170, 170])
        ax1.legend()

    plotcanvas = FigureCanvasTkAgg(fig, window)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
    
    window.mainloop()

def plot_SAD():
    window = tk.Toplevel(root)
    window.geometry('1400x700+200+100')
    window.title('Sound Activity')
    window.resizable(False,False)
    window.state('normal')
    window.config(background='#fafafa')
                  
    RecognitionGUI.m_SAD = []
    xar = []
    yar = []
    index = [0]
                  
    style.use('ggplot')
    fig = plt.figure(figsize=(14, 4.5), dpi=100)
    plt.close(fig)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylim(-0.5, 1.5)
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Sound Activity')
    line, = ax1.plot(xar, yar, 'r', marker='x', label='value == 1 => sound\nvalue == 0 => no sound')
    
    def animate(i):
        y = RecognitionGUI.m_SAD
        x = list(np.linspace(index[0], index[0] + len(y) * 0.48, len(y)))
        if len(y) == 105:
            index[0] += 0.48
            RecognitionGUI.m_SAD.pop(0)
        line.set_data(np.array(x), np.array(y))
        if len(x) == 0:
            ax1.set_xlim(0, 1)
        else:
            ax1.set_xlim(index[0], x[-1] + 0.5)
        ax1.legend()

    plotcanvas = FigureCanvasTkAgg(fig, window)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
    
    window.mainloop()

root = tk.Tk()
root.title('Real-Time Sound Recognition')
root.resizable(False,False)

root_menu = tk.Menu(root)
root.config(menu=root_menu)

file_menu = tk.Menu(root_menu)
plot_menu = tk.Menu(root_menu)
root_menu.add_cascade(label='File', menu=file_menu)
root_menu.add_cascade(label='Plot', menu=plot_menu)
file_menu.add_command(label='Exit', command=root.destroy)
plot_menu.add_command(label='Energy Entropy', command=plot_energy_entropy)
plot_menu.add_command(label='Fundamental Frequency', command=plot_F0)
plot_menu.add_command(label='Sound Activity', command=plot_SAD)
plot_menu.add_command(label='Music Activity', command=plot_MAD)

var = tk.IntVar()

def startRecognition():
    if RecognitionGUI.thr != None and RecognitionGUI.thr.is_alive():
        RecognitionGUI.thr.cancel()
    global var
    if var.get() == 1:
        classification_algorithm = 'kNN'
    elif var.get() == 2:
        classification_algorithm = 'RF'
    RecognitionGUI.getData(classification_algorithm)
       
def stopRecognition():
    RecognitionGUI.result = 'Wait for start recognition'
    RecognitionGUI.thr.cancel()  

def on_closing():
    if RecognitionGUI.thr != None and RecognitionGUI.thr.is_alive():
        RecognitionGUI.thr.cancel()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

canvas = tk.Canvas(root, height=700, width=700, bg='#CCCCFF')
canvas.pack()
frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.6, relheight=0.45, relx=0.22, rely=0.2)

startButton = tk.Button(root, text='Start Recognition', padx=10, pady=5, fg='white', bg='black', command=startRecognition)
startButton.pack(side='left', padx=70, pady=20)

stopButton = tk.Button(root, text='Stop Recognition', padx=10, pady=5, fg='white', bg='black', command=stopRecognition)
stopButton.pack(side='right', padx=70, pady=20)

label = tk.Label(root, text='Choose classifier:')
label.pack()

knn_cb = tk.Radiobutton(root, text='k-Nearest Neighbour', variable=var, value=1)
knn_cb.pack()

rf_cb = tk.Radiobutton(root, text='Random Forest', variable=var, value=2)
rf_cb.pack()

label2 = tk.Label(frame, text='Wait for start recognition', bg='#FFFFFF')
label2.config(font=("Courier", 16))
label2.pack()

label3 = tk.Label(frame)
label3.pack()

RecognitionGUI.result = 'Wait for start recognition'

def set_label():
    global label2
    label2['text'] = RecognitionGUI.result
    if RecognitionGUI.result == 'silence':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/silence.jpg'))
        label3.configure(image=img)
        label3.image = img
    elif RecognitionGUI.result == 'speech male':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/male.jpg'))
        label3.configure(image=img)
        label3.image = img
    elif RecognitionGUI.result == 'speech female':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/female.jpg'))
        label3.configure(image=img)
        label3.image = img
    elif RecognitionGUI.result == 'musical_instruments string':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/string.jpg'))
        label3.configure(image=img)
        label3.image = img
    elif RecognitionGUI.result == 'musical_instruments brass':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/brass.jpg'))
        label3.configure(image=img)
        label3.image = img
    elif RecognitionGUI.result == 'musical_instruments woodwind':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/woodwind.jpg'))
        label3.configure(image=img)
        label3.image = img
    elif RecognitionGUI.result == 'unknown':
        img = ImageTk.PhotoImage(Image.open('/home/apopa/Facultate/Licenta/images/unknown.jpg'))
        label3.configure(image=img)
        label3.image = img
    root.after(1, set_label)
    
set_label()

root.mainloop()
