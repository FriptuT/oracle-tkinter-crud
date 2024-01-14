import tkinter as tk
from tkinter import messagebox
import cx_Oracle

# Establish a connection to the Oracle database
conn = cx_Oracle.connect('c##teodor/001010@localhost:1521/xe')
cursor = conn.cursor()

class TelecomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ABONATI")

        self.create_widgets()
        self.display_abonat_entries()

    def create_widgets(self):
        # Labels and Entry widgets for adding/modifying data
        tk.Label(self.root, text="Abonat ID:").grid(row=0, column=0)
        self.abonat_id_entry = tk.Entry(self.root)
        self.abonat_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Nume:").grid(row=1, column=0)
        self.nume_entry = tk.Entry(self.root)
        self.nume_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Prenume:").grid(row=2, column=0)
        self.prenume_entry = tk.Entry(self.root)
        self.prenume_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Adresa:").grid(row=3, column=0)
        self.adresa_entry = tk.Entry(self.root)
        self.adresa_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Telefon:").grid(row=4, column=0)
        self.telefon_entry = tk.Entry(self.root)
        self.telefon_entry.grid(row=4, column=1)

        tk.Label(self.root, text="CNP:").grid(row=5, column=0)
        self.cnp_entry = tk.Entry(self.root)
        self.cnp_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Abonament ID:").grid(row=6, column=0)
        self.abonament_id_entry = tk.Entry(self.root)
        self.abonament_id_entry.grid(row=6, column=1)

        # Buttons for actions
        tk.Button(self.root, text="Add Abonat", command=self.add_abonat).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Modify Abonat", command=self.modify_abonat).grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Delete Abonat", command=self.delete_abonat).grid(row=9, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Refresh Abonati", command=self.refresh_entries).grid(row=10, column=0, columnspan=2, pady=10)

    def refresh_entries(self):
        # Clear existing labels
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and widget.grid_info()['row'] >= 10:
                widget.destroy()

        # Refresh the displayed entries
        self.display_abonat_entries()    

    def display_abonat_entries(self):
        # Display all entries from the 'abonat' table
        query = "SELECT * FROM abonat"
        cursor.execute(query)
        abonat_entries = cursor.fetchall()

        # Display the entries in the Tkinter window
        for i, entry in enumerate(abonat_entries):
            display_text = f"ID: {entry[0]}, Nume: {entry[1]}, Prenume: {entry[2]}, Adresa: {entry[3]}, Telefon: {entry[4]}, CNP: {entry[5]}, Abonament ID: {entry[6]}"
            tk.Label(self.root, text=display_text).grid(row=11 + i, column=0, columnspan=2)


    def execute_query(self, query, params=None):
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
        except cx_Oracle.Error as error:
            messagebox.showerror("Error", f"Database Error: {error}")
            conn.rollback()

    def add_abonat(self):
        # Retrieve data from entry widgets
        abonat_id = int(self.abonat_id_entry.get())
        nume = self.nume_entry.get()
        prenume = self.prenume_entry.get()
        adresa = self.adresa_entry.get()
        telefon = self.telefon_entry.get()
        cnp = self.cnp_entry.get()
        abonament_id = int(self.abonament_id_entry.get())

        # Add the data to the Oracle database tables
        query = "INSERT INTO abonat VALUES (:abonat_id, :nume, :prenume, :adresa, :telefon, :cnp, :abonament_id)"
        params = {'abonat_id': abonat_id, 'nume': nume, 'prenume': prenume, 'adresa': adresa,
                  'telefon': telefon, 'cnp': cnp, 'abonament_id': abonament_id}
        self.execute_query(query, params)

        # Clear the entry widgets
        self.clear_entries()

        # Refresh the displayed entries
        self.display_abonat_entries()

        # Update the Tkinter window
        self.root.update_idletasks()

        messagebox.showinfo("Success", "Abonat added successfully!")

    def modify_abonat(self):
        # Retrieve data from entry widgets
        abonat_id = int(self.abonat_id_entry.get())
        nume = self.nume_entry.get()
        prenume = self.prenume_entry.get()
        adresa = self.adresa_entry.get()
        telefon = self.telefon_entry.get()
        cnp = self.cnp_entry.get()
        abonament_id = int(self.abonament_id_entry.get())

        # Modify the data in the Oracle database tables
        query = "UPDATE abonat SET nume=:nume, prenume=:prenume, adresa=:adresa, telefon=:telefon, cnp=:cnp, codabonament=:abonament_id WHERE idabonat=:abonat_id"
        params = {'abonat_id': abonat_id, 'nume': nume, 'prenume': prenume, 'adresa': adresa,
                'telefon': telefon, 'cnp': cnp, 'abonament_id': abonament_id}
        self.execute_query(query, params)

        # Clear the entry widgets
        self.clear_entries()

        # Refresh the cursor
        cursor.close()
        cursor = conn.cursor()

        # Refresh the displayed entries
        self.display_abonat_entries()

        # Update the Tkinter window
        self.root.update_idletasks()

        messagebox.showinfo("Success", "Abonat modified successfully!")


    def delete_abonat(self):
        # Retrieve data from entry widgets
        abonat_id = int(self.abonat_id_entry.get())

        # Delete the data from the Oracle database tables
        query = "DELETE FROM abonat WHERE idabonat=:abonat_id"
        params = {'abonat_id': abonat_id}
        self.execute_query(query, params)

        # Clear the entry widgets
        self.clear_entries()

        # Refresh the displayed entries
        self.display_abonat_entries()

        messagebox.showinfo("Success", "Abonat deleted successfully!")

    def clear_entries(self):
        # Clear all entry widgets
        self.abonat_id_entry.delete(0, tk.END)
        self.nume_entry.delete(0, tk.END)
        self.prenume_entry.delete(0, tk.END)
        self.adresa_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)
        self.cnp_entry.delete(0, tk.END)
        self.abonament_id_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TelecomApp(root)
    root.mainloop()

# Close the cursor and connection when the application is closed
cursor.close()
conn.close()