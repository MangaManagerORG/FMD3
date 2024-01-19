import io
import tkinter
from urllib import request
from PIL import Image, ImageTk
from FMD3.Sources import extesion_factory, ISource, list_extension, get_extension
from FMD3.Models.MangaInfo import MangaInfo


def load_data():
    url = var.get()
    sel_ext = clicked.get()

    ext: ISource = get_extension(sel_ext)
    mi: MangaInfo = ext.on_get_info(url)

    res = f"""
    Series name: {mi.title}
    Num of chapters: {len(mi.chapters)}
    genres: {mi.genres}
    authors: {mi.authors}
    artists: {mi.artists}
    description: {mi.description}
    """

    raw_data = request.urlopen(mi.cover_url).read()
    im = Image.open(io.BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    image_lbl = tkinter.Label(root, image=image)
    image_lbl.image = image

    image_lbl.pack()

    result.set(res)


root = tkinter.Tk()

extensions = list_extension()

clicked = tkinter.StringVar()
drop = tkinter.OptionMenu(root, clicked, *extensions)
drop.pack()
result = tkinter.StringVar()
tkinter.Label(root, textvariable=clicked).pack()
var = tkinter.StringVar()
tkinter.Label(root, text="Insert URL").pack()
tkinter.Entry(root, textvariable=var).pack()

tkinter.Button(root, command=load_data, text="Download series").pack()

tkinter.Label(root, textvariable=result, justify="left").pack()

root.mainloop()
