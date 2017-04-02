# -*- coding: utf-8 -*-

from tkinter import *
import sqlite3
import os
from tkinter import messagebox as msg

currdir = os.getcwd()
bdd = currdir+"/bdd_chrono_650.sq3"
conn = sqlite3.connect(bdd)
cur = conn.cursor()





def deleteB():
    fenD = Tk()
    fenD.columnconfigure(0, weight=1)
    fenD.rowconfigure(0, weight=1)
    fenD.title('Bateaux')
    fenD.geometry("600x720+0+0")
    def suppr(boat_number):
        if msg.askokcancel('Attention', "Êtes-vous sûr(e) de vouloir supprimer le bateau n° " + boat_number + "?"):
            cur.execute("DELETE FROM bateaux WHERE boat_number=?", (boat_number,))
            cur.execute("DELETE FROM classement WHERE boat_number=?", (boat_number,))
            conn.commit()
            msg.showinfo('Réussi', "Le bateau n°" + boat_number +"a bien été supprimé.")
            fenD.destroy()
            deleteB()

    class Interface(Frame):
        

        def __init__(self, fenetre, **kwargs):
            Frame.__init__(self, fenetre, **kwargs)
            self.grid(sticky=N+S+E+W, padx=4)

            self.message1 = Label(self, text="Numéro du bateau")
            self.message1.grid(column=0, row=0, sticky='EW')
            self.message2 = Label(self, text="Nom Officiel")
            self.message2.grid(column=1, row=0, sticky='EW')
            self.message3 = Label(self, text="Prototype")
            self.message3.grid(column=2, row=0, sticky='EW')

            self.num_bateau = Listbox(self)
            self.num_bateau.grid(column=0, row=1, sticky=N+S+E+W)
            self.nom_off = Listbox(self)
            self.nom_off.grid(column=1, row=1, sticky=N+S+E+W)
            self.proto = Listbox(self)
            self.proto.grid(column=2, row=1, sticky=N+S+E+W)
            cur.execute('SELECT * FROM bateaux')
            bateaux = cur.fetchall()
            bouton_quitter = Button(self, text = "Retour", command = fenD.destroy)
            bouton_quitter.grid(column=3, row=3)
            self.rowconfigure(1,weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=3)
            
            
            def fill(event):
                index = self.num_bateau.curselection()[0]
                num = self.num_bateau.get(index)
                self.numero.delete(0, END)
                self.numero.insert(0, num)

            self.num_bateau.bind('<ButtonRelease-1>', fill)
            bgcouleur=''
            compteur = 0
            for item in bateaux:
                if compteur%2 == 0:
                    bgcouleur = 'white'
                else:
                    bgcouleur = '#BBBBBB'
                    self.num_bateau.insert(END, item[0])
                    self.num_bateau.insert(END)
                    self.num_bateau.itemconfig(compteur, bg=bgcouleur)
                    self.nom_off.insert(END, item[1])
                    self.nom_off.insert(END)
                    self.nom_off.itemconfig(compteur, bg=bgcouleur)
                    if item[4] == 0:
                        self.proto.insert(END, "Série")
                        self.proto.insert(END)
                        self.proto.itemconfig(compteur, bg=bgcouleur)
                    else:
                        self.proto.insert(END, "Prototype")
                        self.proto.insert(END)
                        self.proto.itemconfig(compteur, bg=bgcouleur)
                    compteur += 1

                
            self.caption = Label(self, text ="Supprimer le bateau n°:")
            self.caption.grid(column=0, row=2)
            self.numero = Entry(self)
            self.numero.grid(column=1, row=2)
            self.supprimer = Button(self, text = "Supprimer", command = lambda:suppr(self.numero.get()))
            self.supprimer.grid(column=2, row=2)

    interface = Interface(fenD)
    interface.mainloop()
    interface.destroy()

