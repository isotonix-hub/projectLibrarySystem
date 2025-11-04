from email.utils import formataddr
import getpass
from PIL import Image, ImageTk
import tkinter as tk
import mysql as mysql
from mysql.connector import Error
import hashlib as hash
import threading
import tkinter as tk
from tkinter import BOTH, CENTER, Tk, Toplevel
from PIL import Image, ImageTk
import mysql.connector
import pygame  # type: ignore 
import io
from tkinter import DISABLED, NORMAL
from tkinter import messagebox
import re
import datetime as datetime
from tkinter import ttk


def update_image_for_id(path, row_id):
    # Connect to MySQL


    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="!@MCGi0702",
        database="sqlconnection"
    )
    cursor = conn.cursor()

    # Read the image as binary
    with open(path, "rb") as file:
        binary_data = file.read()

    # Update the existing row (id = row_id)
    query = "UPDATE math_books SET book_image = %s WHERE id = %s"
    cursor.execute(query, (binary_data, row_id))

    conn.commit()

    print(f"✅ Image updated for id {row_id}.")

    cursor.close()
    conn.close()

# Example usage: update image for id = 1
update_image_for_id(r"C:\Users\ADMIN\Downloads\newton.jpg",2)




def playSound():

   pygame.mixer.init()
   pygame.mixer.music.load(r"C:\Users\ADMIN\Downloads\sounds.wav")
   pygame.mixer.music.set_volume(0.3)  # 0.0 to 1.0
   pygame.mixer.music.play()

def playSoundAdmin():

   pygame.mixer.init()
   pygame.mixer.music.load(r"C:\Users\ADMIN\Downloads\sounds2.wav")
   pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0
   pygame.mixer.music.play()


def selectedBooks(n , listOfBooks ):
    
    listOfBooks.withdraw()

  

      
    match n:
        case "Math":
         listOfBooks.withdraw()
        
         mathBooksWindow = tk.Toplevel()
         mathBooksWindow.state("zoomed")
         mathBooksWindow.title("List of Books")

         original_bg = Image.open(r"C:\Users\ADMIN\Downloads\background_for_all.png")
         resized_bg = original_bg.resize((1920, 1080), Image.LANCZOS)
         bg_image = ImageTk.PhotoImage(resized_bg)
    
         bg_label = tk.Label(mathBooksWindow, image=bg_image)
         bg_label.image = bg_image 
         bg_label.place(x=0, y=0, relwidth=1, relheight=1)

  
         tk.Label(mathBooksWindow, text="Math books", font=("Times", 15, "bold"), bg="#955225").pack(pady=5)

   
         tk.Entry(mathBooksWindow, width=25, bg="#955225", font=("Times", 10, "bold")).pack(pady=5)
         tk.Button(mathBooksWindow, text="Search", font=("Times", 12, "bold"), bg="#955225").pack(pady=5)

         def back_button_books():
          mathBooksWindow.destroy()
          listOfBooks.deiconify()  

         tk.Button(mathBooksWindow, text="Back", font=("Times", 12, "bold"), bg="#955225", command=back_button_books).pack(side="bottom", pady=5)
       
         connection = mysql.connector.connect(
         host="localhost",
         user="root",
         password="!@MCGi0702",
         database="sqlconnection"
                                 )
         cursor = connection.cursor()
         cursor.execute("SELECT id, title, author, book_image, is_available FROM math_books")
         books = cursor.fetchall()
         cursor.close()
         connection.close()     

         book_frame = tk.Frame(mathBooksWindow, bg="#955225")
         book_frame.pack(side="top", anchor="nw", padx=30, pady=30)

         def get_information(input_student_number, input_name, input_lastname, book_id, btn , title ,  information_frame):

                    print(input_student_number.get())
                    connection = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="!@MCGi0702",
                        database="sqlconnection")

                    cursor = connection.cursor()

                    ## Etong logic nato kapag ang user nag enter ulit ng libro pero meron na tignan ulit sa database kuhain yung entry e get yung  value then kapag True ibigsabihin meron na siyang naborrow di dapat maulit
                    cursor.execute("SELECT studentNumber FROM student_information_borrow WHERE studentNumber = %s",(input_student_number.get().strip(),))
                    result = cursor.fetchone()


                    if result:
                        messagebox.showerror("Error" , "You already borrow a book")
                        input_student_number.delete(0,tk.END)
                        return




                    # Eto naman ay kapag yung isa sa mga value ng user ay nakalimutan mag type ng value
                    if not input_student_number.get()  or not input_name.get() or not input_lastname.get():
                        messagebox.showerror("Error" , "No empty value!")
                        return
                   
                    #Eto naman pattern para sa student number regex ang tawag para maiwasan ang pagkakamali ng magsusulat para hindi edit ang database kung sakaling nagkamali siya
                    # mag rereset lang ulit yung mga value kapag yung pattern hindi nag match sa value na isulat ng user
                    pattern_student_number = r'^[A-Z]{2}\d{9}$'
                    validation_student_number = re.match(pattern_student_number , input_student_number.get())
                    if not validation_student_number:
                        input_student_number.delete(0,tk.END)
                        messagebox.showerror("Validation Error", "Invalid student number format.")
                        return


             

                     #Eto naman pattern para sa student number regex ang tawag para maiwasan ang pagkakamali ng magsusulat para hindi edit ang database kung sakaling nagkamali siya
                    # mag rereset lang ulit yung mga value kapag yung pattern hindi nag match sa value na isulat ng user
                   
                    pattern_name = r'^[A-Z][a-zA-Z]{0,20}$'
                    validation_name = re.match(pattern_name , input_name.get())
                    if not validation_name:
                        input_name.delete(0, tk.END)
                        messagebox.showerror("Validation Error", "Invalid first name format. Should start with an uppercase letter and contain only letters (up to 20 characters).")
                        return

                     #Eto naman pattern para sa last name regex ang tawag para maiwasan ang pagkakamali ng magsusulat para hindi edit ang database kung sakaling nagkamali siya
                    # mag rereset lang ulit yung mga value kapag yung pattern hindi nag match sa value na isulat ng user
                    pattern_last_name = r'^[A-Z][a-zA-Z]{0,20}$'
                    validation_last_name = re.match(pattern_last_name , input_lastname.get())
                    if not validation_last_name:
                        input_lastname.delete(0, tk.END)
                        messagebox.showerror("Validation Error", "Invalid first name format. Should start with an uppercase letter and contain only letters (up to 20 haracters).")
                        return


                    #One week dapat mabalik eto logic
                    
                    returnDate = datetime.datetime.now() + datetime.timedelta(weeks=1)

                    status = "No penalty"

                    insert_query = """
                    INSERT INTO student_information_borrow (bookId , title, studentNumber, studentName, studentLastname, borrowDate , returnDate ,status)
                    VALUES (%s, %s, %s, %s, %s , NOW(), %s, %s)
                    """


                    try:

                        cursor.execute(insert_query, (book_id ,  title , input_student_number.get() , input_name.get() ,input_lastname.get(), returnDate, status))

                 

           
                   
             
                        #eto yung magigisng zero kasi kapag tapos ng user maginput ng information tapos ok yung availablity ng libro magiging i set mo ng zero =para maging false
                        cursor.execute("UPDATE math_books SET is_available = 0 WHERE id=%s" , (book_id ,))
                        connection.commit()
                        btn.config(state=DISABLED)
                        btn.config(text="Unavailable")
                        messagebox.showinfo("Success", "Book borrowed successfully!")
                        input_student_number.delete(0, tk.END)
                        information_frame.withdraw()
                     
                       
                   
         
                    except mysql.connector.Error as err:
                        messagebox.showinfo("Database error" , f"Error: {err}")
                    finally:
                        cursor.close()
                        connection.close()



                 
         def borrow_button_clicked(book_id , btn , title ):
            if hasattr(borrow_button_clicked, "window") and borrow_button_clicked.window.winfo_exists():
                     return 

            information_frame = tk.Toplevel()
            information_frame.geometry("400x200")
            information_frame.title("Information")
   
            borrow_button_clicked.window = information_frame


            tk.Label(information_frame, text="Student number", font=("Times", 12, "bold")).pack(pady=3)
            input_student_number = tk.Entry(information_frame)
            input_student_number.pack(pady=3)

            tk.Label(information_frame, text="Firstname", font=("Times", 12, "bold")).pack(pady=3)
            input_name = tk.Entry(information_frame)
            input_name.pack(pady=3)


            tk.Label(information_frame, text="Lastname", font=("Times", 12, "bold")).pack(pady=3)
            input_lastname = tk.Entry(information_frame)
            input_lastname.pack(pady=3)

    
            tk.Button(
             information_frame,
             text="Enter",
             command=lambda: get_information(input_student_number, input_name, input_lastname, book_id, btn , title , information_frame )
             ).pack(pady=5)

    
            def on_close():
              borrow_button_clicked.window.destroy()
              del borrow_button_clicked.window

              information_frame.protocol("WM_DELETE_WINDOW", on_close)




         for i, (book_id, title, author, book_image, is_available) in enumerate(books):
                individual_button_frame = tk.Frame(book_frame, bg="#955225")
                individual_button_frame.grid(row=0, column=i, sticky="w", padx=10, pady=10)
               


                individual_book_frame = tk.Frame(book_frame, bg="#955225")
                individual_book_frame.grid(row=0, column=i, sticky="w", padx=10, pady=10)
               

                id_label = tk.Label(individual_book_frame, text=f"ID: {book_id}", bg="#955225", font=("Times", 13, "bold"))
                id_label.grid(row=0, column=0, padx=20, pady=5)


                title_label = tk.Label(individual_book_frame, text=f"Title: {title}", bg="#955225", font=("Times", 13, "bold"))
                title_label.grid(row=1, column=0, padx=20, pady=5)

                author_label = tk.Label(individual_book_frame, text=f"Author: {author}", bg="#955225", font=("Times", 13, "bold"))
                author_label.grid(row=2, column=0, padx=20, pady=2)

                borrow_button = tk.Button(individual_book_frame, text="Borrow", bg="#955225", font=("Times", 13, "bold"))        
                borrow_button.grid(row=4, column=0, padx=20, pady=2)


                buttons_dict = {}

                borrow_button.config(command=lambda borrow_button=borrow_button, bookId=book_id ,title = title: borrow_button_clicked(bookId, borrow_button , title))

                #etong logic nato kapag ang user nag pili ng libro yung button sa database at sa GUI ma didisable at yung text mamapapalitan ng unavaible pero ito binuksan mo ulit yung app yung state ng button still remain as is kasi nakasaave sa database yung availability
                #kapag 0 it means = false , kapag 1  it means = True  ginawa kung boolean pero typeInt  
                borrow_button.config(
                text="Unavailable" if is_available == 0 else "Borrow",  # Set text
                state=DISABLED if is_available == 0 else NORMAL ) # Set state
                 
                buttons_dict[book_id] = borrow_button


                #Etong logic na to 2 hours kong sinulat ang hayop hahaha sa wakas gumana rin hahaha!!! 
                # Magrefresh yung button kapag yugn user nag sauli ng libro live !!
                def refresh_book_status():
                    try:
                     connection = mysql.connector.connect(
                     host="127.0.0.1",
                     user="root",
                     password="!@MCGi0702",
                     database="sqlconnection"
                        )
                     cursor = connection.cursor()
                     cursor.execute("SELECT id, is_available FROM math_books")
                     status_data = cursor.fetchall()
                     cursor.close()
                     connection.close()

                 

                     for book_id, is_available in status_data:
                      if book_id in buttons_dict:
                        print(f"This is the bookI{book_id}")
                        btn = buttons_dict[book_id]
                        print(btn)
                        if is_available == 1:
                          btn.config(text="Borrow", state=tk.NORMAL, bg="#955225")
                        else:
                          btn.config(text="Unavailable", state=tk.DISABLED, bg="gray")

                    except mysql.connector.Error as err:
                         print(f"Database refresh error: {err}")
                    
                    mathBooksWindow.after(2000, refresh_book_status)

                   
                refresh_book_status()

              
                if book_image:
                    image_data = Image.open(io.BytesIO(book_image))
                    image_data = image_data.resize((200, 200), Image.LANCZOS)  
                    image_tk = ImageTk.PhotoImage(image_data)
                    image_label = tk.Label(individual_book_frame, image=image_tk, bg="#955225")
                    image_label.image = image_tk  
                    image_label.grid(row=3, column=0, padx=5, pady=5)
                else:
                    no_image_label = tk.Label(individual_book_frame, text="No Image", bg="#955225", font=("Times", 12, "italic"))
                    no_image_label.grid(row=3, column=0, padx=5, pady=5)

                break

        case "Science":
         scienceBooksWindow = tk.Toplevel()
         scienceBooksWindow.state("zoomed")
         scienceBooksWindow.title("List of Books")

       

         original_background_image = Image.open(r"C:\Users\ADMIN\Downloads\background_for_all.png")
         original_background_image_resize = original_background_image.resize((1920, 1080), Image.LANCZOS)

       
         background_image_tk = ImageTk.PhotoImage(original_background_image_resize)

         
         background_label = tk.Label(scienceBooksWindow, image=background_image_tk)
   
         
         background_label.place(x=0, y=0, relheight=1, relwidth=1)

     
         label = tk.Label(scienceBooksWindow, text="Science books",font=("Times" , 15 ,"bold"),bg="#955225")
         label.pack(pady=5)

        
         entry = tk.Entry(scienceBooksWindow, width=25 , bg="#955225", font=("Times",10, "bold"))
         entry.pack(pady=5)

  
         search_button = tk.Button(scienceBooksWindow, text="Search",font=("Times",12, "bold") ,bg="#955225")
         search_button.pack(pady=5)

        
         def back_button_books():
            scienceBooksWindow.withdraw() 
            listOfBooks.state("zoomed")

         back_button_books = tk.Button(scienceBooksWindow , text="Back" , font=("Times" ,12 , "bold"), bg="#955225", command=back_button_books)
         back_button_books.pack(side="bottom" ,pady=5)



        case "English":
         englishBooksWindow = tk.Toplevel()
         englishBooksWindow.state("zoomed")
         englishBooksWindow.title("List of Books")  

         original_background_image = Image.open(r"C:\Users\ADMIN\Downloads\background_for_all.png")
         original_background_image_resize = original_background_image.resize((1920, 1080), Image.LANCZOS)

       
         background_image_tk = ImageTk.PhotoImage(original_background_image_resize)

         
         background_label = tk.Label(englishBooksWindow, image=background_image_tk)
   
         
         background_label.place(x=0, y=0, relheight=1, relwidth=1)

     
         label = tk.Label(englishBooksWindow, text="Science books",font=("Times" , 15 ,"bold"),bg="#955225")
         label.pack(pady=5)

        
         entry = tk.Entry(englishBooksWindow, width=25 , bg="#955225", font=("Times",10, "bold"))
         entry.pack(pady=5)

  
         search_button = tk.Button(englishBooksWindow, text="Search",font=("Times",12, "bold") ,bg="#955225")
         search_button.pack(pady=5)

        
         def back_button_books():
            englishBooksWindow.withdraw() 
            listOfBooks.state("zoomed")

         back_button_books = tk.Button(englishBooksWindow , text="Back" , font=("Times" ,12 , "bold"), bg="#955225", command=back_button_books)
         back_button_books.pack(side="bottom" ,pady=5)

        case "History":
         historyBooksWindow = tk.Toplevel()
         historyBooksWindow.state("zoomed")
         historyBooksWindow.title("List of Books")

         original_background_image = Image.open(r"C:\Users\ADMIN\Downloads\background_for_all.png")
         original_background_image_resize = original_background_image.resize((1920, 1080), Image.LANCZOS)

       
         background_image_tk = ImageTk.PhotoImage(original_background_image_resize)

         
         background_label = tk.Label(historyBooksWindow, image=background_image_tk)
   
         
         background_label.place(x=0, y=0, relheight=1, relwidth=1)

     
         label = tk.Label(historyBooksWindow, text="Science books",font=("Times" , 15 ,"bold"),bg="#955225")
         label.pack(pady=5)

        
         entry = tk.Entry(historyBooksWindow, width=25 , bg="#955225", font=("Times",10, "bold"))
         entry.pack(pady=5)

  
         search_button = tk.Button(historyBooksWindow, text="Search",font=("Times",12, "bold") ,bg="#955225")
         search_button.pack(pady=5)

        
         def back_button_books():
            historyBooksWindow.withdraw() 
            listOfBooks.state("zoomed")

         back_button_books = tk.Button(historyBooksWindow , text="Back" , font=("Times" ,12 , "bold"), bg="#955225", command=back_button_books)
         back_button_books.pack(side="bottom" ,pady=5)

        

        case "IT":
         itBooksWindow = tk.Toplevel()
         itBooksWindow.state("zoomed")
         itBooksWindow.title("List of Books")

         original_background_image = Image.open(r"C:\Users\ADMIN\Downloads\background_for_all.png")
         original_background_image_resize = original_background_image.resize((1920, 1080), Image.LANCZOS)

       
         background_image_tk = ImageTk.PhotoImage(original_background_image_resize)

         
         background_label = tk.Label(itBooksWindow, image=background_image_tk)
   
         
         background_label.place(x=0, y=0, relheight=1, relwidth=1)

     
         label = tk.Label(itBooksWindow, text="Science books",font=("Times" , 15 ,"bold"),bg="#955225")
         label.pack(pady=5)

        
         entry = tk.Entry(itBooksWindow, width=25 , bg="#955225", font=("Times",10, "bold"))
         entry.pack(pady=5)

  
         search_button = tk.Button(itBooksWindow, text="Search",font=("Times",12, "bold") ,bg="#955225")
         search_button.pack(pady=5)

        
         def back_button_books():
            itBooksWindow.withdraw() 
            listOfBooks.state("zoomed")

         back_button_books = tk.Button(itBooksWindow , text="Back" , font=("Times" ,12 , "bold"), bg="#955225", command=back_button_books)
         back_button_books.pack(side="bottom" ,pady=5)
         
        case _:
            print("hello world")




def list_of_books(books):
    books.withdraw() #hide

    listOfBooks = tk.Toplevel()
    listOfBooks.state("zoomed")
    listOfBooks.title("List of Books")

   
    screen_width = listOfBooks.winfo_screenwidth()
    screen_height = listOfBooks.winfo_screenheight()

  
    subjects = [
        ("Math", r"C:\Users\ADMIN\Downloads\Math.png", "#285042"),
        ("English", r"C:\Users\ADMIN\Downloads\English.png", "#032826"),
        ("Science", r"C:\Users\ADMIN\Downloads\Science.png", "#4e5b92"),
        ("History", r"C:\Users\ADMIN\Downloads\History.png", "#d8c894"),
        ("IT", r"C:\Users\ADMIN\Downloads\IT.png", "#21b9c4"),
        ("Back", r"C:\Users\ADMIN\Downloads\sad.png", "#21b9c4")
    ]


    container = tk.Frame(listOfBooks, bg="#f0f0f0")
    container.pack(fill="both", expand=True)

    banner_height = int(screen_height * 0.13)  
    for idx , ( name, img_path, color) in enumerate(subjects):
       
        subject_frame = tk.Frame(container)
        subject_frame.pack(fill="x", pady=5) 

        original_image = Image.open(img_path)
        resized_image = original_image.resize((screen_width, banner_height), Image.LANCZOS)
        background_image = ImageTk.PhotoImage(resized_image)

        img_label = tk.Label(subject_frame, image=background_image)
        img_label.image = background_image
        img_label.pack(fill="x", expand=True)
        

    
        button = tk.Button(
            subject_frame,
            text=name,
            font=("Times", 20, "bold"),
            bg=color,
            fg="white",
            width=10,
            height=1,
            relief="raised",
            command=lambda n=name: selectedBooks(n, listOfBooks) 
        )


     
                
        
            
      
        button.place(relx=0.5, rely=0.5, anchor=CENTER)

    listOfBooks.mainloop()





def logout(books ,login_window):

    books.withdraw()  
    
    login_window.state("zoomed")
   
   







def mainWindow():

 
    books = tk.Tk()
    books.state("zoomed")
    books.title("Library System")

  
    try:
        image = Image.open(r"C:\Users\ADMIN\Downloads\library_image.png") 
        background_image = ImageTk.PhotoImage(image) 
        background_label = tk.Label(books, image=background_image)
        background_label.place(x=0, y=0, relheight=1, relwidth=1)
        background_label.image = background_image
    except Exception as e:
        print(f"Error loading image: {e}")


    books.grid_rowconfigure(0, weight=1)
    books.grid_columnconfigure(0, weight=1)
    books.grid_columnconfigure(1, weight=1)
    books.grid_columnconfigure(2, weight=1)
    books.grid_columnconfigure(3, weight=1)

    buttonBooks = tk.Button(books, text="Books", font=("Times", 20, "bold"), bg="lightblue", width=10,
                         command=lambda: [playSound()  , list_of_books(books)])
    buttonBooks.grid(row=1, column=1, pady=20, padx=10 , sticky="e")

    buttonAbout = tk.Button(books, text="About", font=("Times", 20, "bold"), bg="lightblue", width=10,
                         command=lambda: [playSound() ,   list_of_books(books)])
    buttonAbout.grid(row=1, column=2, pady=20, padx=10 , sticky="w")

   

   

    books.mainloop()








def  adminMainWindow(loginWindow):
     loginWindow.withdraw()
     
     mainWindowAdmin = tk.Toplevel()
     mainWindowAdmin.state("zoomed")






     mainWindowAdmin.mainloop()
     










def adminMainWindow(loginWindow):
  
    loginWindow.withdraw()
    
 
    adminWindow = tk.Toplevel()
    adminWindow.state("zoomed")
    adminWindow.title("Admin Window")

    try:
        image = Image.open(r"C:\Users\ADMIN\Downloads\icct logo.png") 
        background_image = ImageTk.PhotoImage(image) 
        background_label = tk.Label(adminWindow, image=background_image)
        background_label.place(x=0, y=0, relheight=1, relwidth=1)
        background_label.image = background_image
    except Exception as e:
        print(f"Error loading image: {e}")


    adminWindow.grid_rowconfigure(0, weight=1)
    adminWindow.grid_columnconfigure(0, weight=1)
    adminWindow.grid_columnconfigure(1, weight=1)
    adminWindow.grid_columnconfigure(2, weight=1)
    adminWindow.grid_columnconfigure(3, weight=1)

    buttonBooks = tk.Button(adminWindow, text="Logs", font=("Times", 20, "bold"), bg="lightblue", width=10,
                         command=lambda: [playSoundAdmin ,  logsWindowButton(adminWindow)] )
    buttonBooks.grid(row=1, column=1, pady=20, padx=10 , sticky="e")

    buttonAbout = tk.Button(adminWindow, text="Logout", font=("Times", 20, "bold"), bg="lightblue", width=10,
                         command=lambda: logout(adminWindow, loginWindow) )
    buttonAbout.grid(row=1, column=2, pady=20, padx=10 , sticky="w")


    #Papunta sa logs list ng mga nanghiram 
    def logsWindowButton(adminMainWindow):

        adminMainWindow.withdraw() #Hide

        global logsWindow

        logsWindow = tk.Toplevel()
        logsWindow.state("zoomed")
        logsWindow.title("Logs")
        

        
        frame = tk.Frame(logsWindow, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        
       
        columns = ("Book id", "Title", "Student number", "Student name", "Student lastname", "Borrow date", "Return date", "status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

     
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

   
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="!@MCGi0702",
            database="sqlconnection"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT bookId, title, studentNumber, studentName ,studentLastname, borrowDate, returnDate, status FROM student_information_borrow")
        studentInformationBooks = cursor.fetchall()
        print(studentInformationBooks)
        cursor.close()
        connection.close()

        for row in studentInformationBooks:
            tree.insert("", "end", values=row)

        btnFrame = tk.Frame(logsWindow, pady=10)
        btnFrame.pack()
        tk.Button(btnFrame, text="Return Book", command=lambda:returnBook(tree), bg="lightgreen", width=15).pack(side="left", padx=10)
        
        logsWindow.after(1000 , autoRefresh(tree))
  
        
        def returnBook(tree):
            if hasattr(returnBook, "window") and returnBook.window.winfo_exists():
                     return 

            information_frame = tk.Toplevel()
            information_frame.geometry("400x200")
            information_frame.title("Information")
   
            returnBook.window = information_frame


            tk.Label(information_frame, text="Student number", font=("Times", 12, "bold")).pack(pady=3)
            input_student_number = tk.Entry(information_frame)
            input_student_number.pack(pady=3)

            
            tk.Label(information_frame, text="Book title", font=("Times", 12, "bold")).pack(pady=3)
            title = tk.Entry(information_frame)
            title.pack(pady=3)

    
            tk.Button(
             information_frame,
             text="Enter",
             command=lambda: get_information(input_student_number , title , tree)
             ).pack(pady=5)

            logsWindow.after(1000, lambda: autoRefresh(tree))

    
            def on_close():
              returnBook.window.destroy()
              del returnBook.window

              information_frame.protocol("WM_DELETE_WINDOW", on_close)

            def get_information(input_student_number , title , tree):

                if not title.get() or  not input_student_number.get():
                        messagebox.showerror("Warning" , "Empty value of title or student number")
                        return
                

                pattern_student_number = r'^[A-Z]{2}\d{9}$'
                validation_student_number = re.match(pattern_student_number , input_student_number.get())

                if not validation_student_number:
                        input_student_number.delete(0,tk.END)
                        messagebox.showerror("Validation Error", "Invalid student number format.")
                        return

                try:
    
                  connection = mysql.connector.connect(
                  host="127.0.0.1",
                  user="root",
                  password="!@MCGi0702",
                  database="sqlconnection"
                             )

                  cursor = connection.cursor()

                 
                  cursor.execute(
                  "SELECT * FROM student_information_borrow WHERE LOWER(title) = LOWER(%s) AND LOWER(studentNumber) = LOWER(%s)",
                  (title.get().strip(), input_student_number.get().strip())
)
                  result = cursor.fetchone()

                  if result:
                     
                    cursor.execute(
                   "DELETE FROM student_information_borrow WHERE studentNumber = %s AND title = %s",
                   (input_student_number.get().strip(), title.get().strip())
                    )


                    connection.commit()
                    messagebox.showinfo("Success", "✅ Record found and deleted successfully.")


                    titleGet = title.get().strip()
                    setAvailableAgain(titleGet)

                    logRefreshTable(tree)
        
                   
                  else:
                  
                   messagebox.showwarning("Not Found", "⚠️ Record not found, nothing to delete.")

                except mysql.connector.Error as err:
                  print("❌ Database error:", err)

                except Exception as e:
                     print("❗ Other error:", e)

                finally:
                      if 'cursor' in locals() and cursor:
                       cursor.close()
                if 'connection' in locals() and connection.is_connected():
                     connection.close()
                     print("🔒 Connection closed.")



               

        

        logsWindow.mainloop()



  

def logout(adminWindow, loginWindow):
    adminWindow.withdraw()
    loginWindow.state("zoomed")

def adminWindow():
    loginWindow = tk.Tk()
    loginWindow.title("Login Window") 
    loginWindow.state("zoomed")   
    
    tk.Label(loginWindow, text="Admin name").pack(pady=0)
    entryUsername = tk.Entry(loginWindow, width=30)
    entryUsername.pack(pady=5)

    tk.Label(loginWindow, text="Admin password").pack(pady=10)
    entryPassword = tk.Entry(loginWindow, width=30, show="*")
    entryPassword.pack(pady=15)

    def login():
        getUsername = entryUsername.get().strip()
        getPassword = entryPassword.get().strip()

        hashed_password = hash.sha256(getPassword.encode('utf-8')).hexdigest()
        
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='!@MCGi0702',
                database='sqlconnection'
            )
            cursor = connection.cursor()
            query = "SELECT * FROM admin WHERE admin = %s AND password = %s"
            cursor.execute(query, (getUsername, hashed_password))
            result = cursor.fetchone()
            
            if not getUsername or not getPassword:
                messagebox.showerror("Error", "Please enter your username or password")
                return

            if result:
                entryUsername.delete(0, tk.END)
                entryPassword.delete(0, tk.END) 
                adminMainWindow(loginWindow)
            else:
                messagebox.showerror("Error", "Wrong credentials")
                entryUsername.delete(0, tk.END)
                entryPassword.delete(0, tk.END)
                return

            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if connection.is_connected():
                connection.close()

    tk.Button(loginWindow, bg="lightblue", width=30, text="Login", command=login).pack(pady=20)

    loginWindow.mainloop()

# Function para ma reload ulit data mag refresh sa logs kapag na delete 

def logRefreshTable(tree):
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="!@MCGi0702",
            database="sqlconnection"
        )
        cursor = connection.cursor()
        cursor.execute("""
            SELECT bookId, title, studentNumber, studentName, studentLastname, borrowDate, returnDate, status
            FROM student_information_borrow
        """)
        studentInformationBooks = cursor.fetchall()

    
        for item in tree.get_children():
            tree.delete(item)

      
        for row in studentInformationBooks:
            tree.insert("", "end", values=row)

    except mysql.connector.Error as e:
        print("❌ Database error:", e)

    finally:
        cursor.close()
        connection.close()
        print("🔁 Logs table refreshed.")



        
 



#Eto update molang yung database na from 0 to 1 para yung gui doon haha maupdate try natin kung gagana haha
def setAvailableAgain(titleGet):


    try:
        
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="!@MCGi0702",
            database="sqlconnection"
        )
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE math_books
            SET is_available = 1
            WHERE title = %s
        """, (titleGet,))

        connection.commit()

     
        if cursor.rowcount > 0:
            print(f"✅ Book '{titleGet}' set to available again.")
        else:
            print(f"⚠️ No book found with title '{titleGet}'.")

    except mysql.connector.Error as e:
        print("❌ Database error:", e)

    except Exception as e:
        print("⚠️ Unexpected error:", e)

    finally:
      
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("🔒 Connection closed.")




#Implement naman tayo ng penalty kapag di siya nagbalik ontime :)


  
    

def check_penalties():
    try:
        # ✅ Connect to database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="!@MCGi0702",
            database="sqlconnection"
        )
        cursor = connection.cursor()

       
        current_date = datetime.date.today()

        print(f"📅 Current Date: {current_date}")

        
        cursor.execute("SELECT studentNumber, returnDate FROM student_information_borrow WHERE status = 'No penalty'")
        result = cursor.fetchall()

        print(f"📚 Books with 'No penalty': {result}")

        for (studentNumber, returnDate) in result:
            print(f"🔍 Checking Book ID: {studentNumber}, Return Date: {returnDate}")
            print(returnDate , current_date)

            if current_date > returnDate:
               
                cursor.execute(
                    "UPDATE student_information_borrow SET status = %s WHERE studentNumber = %s",
                    ("Penalty", studentNumber)
                )
                print(f"⚠️ Book ID {studentNumber} is overdue. Status updated to 'Penalty'.")
            else:
                print(f"✅ Book ID {studentNumber} is not overdue. No change.")

   
        connection.commit()
        print("💾 Database updated with penalty statuses.")

    except mysql.connector.Error as err:
        print("❌ Database error:", err)

    except Exception as e:
        print("⚠️ Unexpected error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        print("🔒 Connection closed.")
    

        
    


        


def autoRefresh(tree):
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="!@MCGi0702",
            database="sqlconnection"
        )
        cursor = connection.cursor()
        cursor.execute("""
            SELECT bookId, title, studentNumber, studentName, studentLastname, borrowDate, returnDate, status
            FROM student_information_borrow
        """)
        studentInformationBooks = cursor.fetchall()

    
        for item in tree.get_children():
            tree.delete(item)

      
        for row in studentInformationBooks:
            tree.insert("", "end", values=row)

    except mysql.connector.Error as e:
        print("❌ Database error:", e)

    finally:
        cursor.close()
        connection.close()
        print("🔁 Logs table refreshed.")

        tree.after(1000, lambda: autoRefresh(tree))





check_penalties()



window1 = threading.Thread(target=mainWindow)
window2 = threading.Thread(target=adminWindow)


window1.start()
window2.start()
  




