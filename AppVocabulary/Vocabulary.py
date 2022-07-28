import sqlite3
from tkinter import *
conn = sqlite3.connect('Vocabularies.db')
 
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS my_vocabularies(
		russian text,
		english text,
		tajik text)""")
conn.commit()
conn.close()

def add():
    conn = sqlite3.connect('Vocabularies.db')
    c = conn.cursor()
    c.execute("""INSERT INTO my_vocabularies 
    	VALUES (:russian_dict, :english_dict, :tajik_dict)""",   
            {
                "russian_dict":russian_enter.get(),
                "english_dict":english_enter.get(),
                "tajik_dict":tajik_enter.get(),
            })
    conn.commit()
    conn.close()

    # Clear the text Boxes
    russian_enter.delete(0,END)
    english_enter.delete(0,END)
    tajik_enter.delete(0,END)
def remove():
	# Create connection
    conn = sqlite3.connect('Vocabularies.db')
    # Create a cursor 
    c = conn.cursor()

    c.execute("DELETE FROM my_vocabularies WHERE oid = " + remove_vocabulary_enter.get())
    # Commit our command
    conn.commit()

    # Close connection
    conn.close()
    # Close main window

def query():
	# Create connection
    conn = sqlite3.connect('Vocabularies.db')
    # Create a cursor 
    c = conn.cursor()
    # Create Query DataBase
    c.execute("SELECT *,oid FROM my_vocabularies")

    records = c.fetchall()
    print_record =""
    for record in records:
    	#print_record += str(record[0]) + " " +"\t" + str(record[3]) + "\n"
    	list_box.insert(END,(str(record[3])+"."+str(record[0]) +"- "+ str(record[2])))
    	lbl_quantity = Label(text=record[3],bg="yellow",font=("vardana 10 bold"))
    	lbl_quantity.place(x=420,y=10)
    # Commit our command
    conn.commit()

    # Close connection
    conn.close()
def update():
	 # Create a DataBase or connect to one 
    conn = sqlite3.connect('Vocabularies.db')
    # Create a cursor 
    c = conn.cursor()

    record_id = remove_vocabulary_enter.get()
    
    c.execute("""UPDATE my_vocabularies SET
		russian  = :RUSSIAN,
		english = :ENGLISH,
		tajik = :TAJIK

		WHERE oid = :oid""",
		{
        'RUSSIAN': russian_editor.get(),
        'ENGLISH': english_editor.get(),
        'TAJIK':tajik_editor.get(),
        'oid': record_id    
        })
    conn.commit()
    conn.close()
    editor.destroy()
def edit():
	global editor
	editor = Tk()	
	editor.title('Vocabulary')
	editor.geometry('270x180')
	editor["bg"] = "orange"
    
    # Create connection
	conn = sqlite3.connect('Vocabularies.db')
    # Create a cursor 
	c = conn.cursor()
    
	record_id = remove_vocabulary_enter.get()
    # Create Query DataBase
	c.execute("SELECT * FROM  my_vocabularies WHERE oid = " + record_id)
    
    # Create Global Variables for text box names
	global russian_editor
	global english_editor
	global tajik_editor
   
	russian_editor = Entry(editor,width = 30,bg = 'pink')
	russian_editor.grid(row = 0,column = 1,padx=20,pady = (10,0))
	english_editor = Entry(editor,width = 30,bg = 'pink')
	english_editor.grid(row = 1,column = 1)
	tajik_editor = Entry(editor,width = 30,bg = 'pink')
	tajik_editor.grid(row = 2,column = 1)
    
    # Create Text Boxe labels
	russian_lbl_editor = Label(editor,text='Русский:',bg = "orange")
	russian_lbl_editor.grid(row = 0,column = 0, pady = (10,0))
	english_lbl_editor = Label(editor,text='Английский:',bg = "orange")
	english_lbl_editor.grid(row = 1,column = 0)
	tajik_genre_lbl_editor = Label(editor,text='Таджикиский:',bg = "orange")
	tajik_genre_lbl_editor.grid(row = 2,column = 0)
    
    # Loop thru Results
	records = c.fetchall()
	for record in records:
		russian_editor.insert(0,record[0])
		english_editor.insert(0,record[1])
		tajik_editor.insert(0,record[2])


    # Create a Save Button to recird Button
	editor_btn = Button(editor,text = 'Save Record',borderwidth =3,command = update,bg="azure4")
	editor_btn.grid(row = 6, column = 0, columnspan = 2, ipadx = 80, pady = 10)

def remove_all_texts():
	list_box.delete(0,END)
	russian_enter.delete(0,END)
	english_enter.delete(0,END)
	tajik_enter.delete(0,END)
	search_enter.delete(0,END)
	remove_vocabulary_enter.delete(0,END)

def update_list(data):
	list_box.delete(0,END)
	for item in data:
		list_box.insert(END,item)

def fillout(event):
	search_enter.delete(0,END)
	search_enter.insert(0,list_box.get(ACTIVE))

def chek(event):
	typed = search_enter.get()
	list_get = list_box.get(0,END)
	if typed =="":
		data = list_get
	else:
		data = []
		for item in list_get:
			if typed.lower() in item.lower():
				data.append(item)
	update_list(data)

root = Tk()
root.title('Data Base')
root.geometry('460x400')
root["bg"] = "OliveDrab2"

russian_enter = Entry(root,width = 30,bg = 'pink',font = "Halvetica 10 bold")
russian_enter.grid(row = 0,column = 1,padx=20,pady = (10,0))
english_enter = Entry(root,width = 30,bg = 'pink',font = "Halvetica 10 bold")
english_enter.grid(row = 1,column = 1)
tajik_enter = Entry(root,width = 30,bg = 'pink',font = "Halvetica 10 bold")
tajik_enter.grid(row = 2,column = 1)
remove_vocabulary_enter = Entry(root,width = 5,borderwidth =2,bg = 'yellow',
	font = ("Halvetica",15))
remove_vocabulary_enter.place(x = 130, y =356)
search_enter = Entry(root,width = 25,bg = 'pink',font = "Halvetica 10 bold")
search_enter.place(x = 260,y = 356)

remove_vocabulary_lbl = Label(root,text='ID:',bg="OliveDrab2",font = ("Halvetica",15))
remove_vocabulary_lbl.place(x = 100, y =356)
russian_lbl = Label(root,text='Русский:',bg = "OliveDrab2",font = "Halvetica 10 bold")
russian_lbl.grid(row = 0,column = 0, pady = (10,0))
english_lbl = Label(root,text='Английский:',bg = "OliveDrab2",font = "Halvetica 10 bold")
english_lbl.grid(row = 1,column = 0)
tajik_lbl = Label(root,text='Таджикиский',bg = "OliveDrab2",font = "Halvetica 10 bold")
tajik_lbl.grid(row = 2,column = 0)
search_lbl = Label(root,text='Поиск:',bg = "OliveDrab2",font = "Halvetica 10 bold")
search_lbl.place(x = 200,y = 356)
colichestva_lbl = Label(root,text='Количество:',bg = "OliveDrab2",font = "Vardana 10 bold")
colichestva_lbl.place(x = 330,y = 10)


# Create Submit Button 
add_btn = Button(root,text = 'Добавить',width =14,command = add,borderwidth =3,bg="azure4")
add_btn.place(x =2, y =80)

# # Create Delete Button
remove_btn = Button(root,text = 'Удалить',width =14,borderwidth =3,command =remove,bg="azure4")
remove_btn.place(x = 112, y =80)

# Create a Quaery Button
query_showList_btn = Button(root,text = 'Показать',borderwidth =3,width =14,command = query,bg="azure4")
query_showList_btn.place(x=222,y=80)

remove_alltexts_btn = Button(root,text = 'Удалить Тексты',width =14,borderwidth =3,command =remove_all_texts,bg="azure4")
remove_alltexts_btn .place(x = 332, y =80)

list_box = Listbox(selectmode =EXTENDED,bg="bisque",
	width=55,height=12,font="vardana 11 bold")
list_box.place(x=2,y=110)

#Create an Update Button 
edit_btn = Button(root,text = 'Редактировать',borderwidth =3,command = edit,bg="azure4" )
edit_btn.place(x = 2, y =356)

update_list((list_box.get(0,END)))


list_box.bind("<<ListboxSelect>>",fillout)

search_enter.bind("<KeyRelease>",chek)


root.mainloop()