import sys, os

# Key-Value DataBase

# To initialize the DataBase, you need to specify the path that you want it to be in, and give it a name.
# It will automatically create/load it, depending on whether it's created or not.
# To add keys and values to your database, simply call add(key, value) method.
# To override an existing key, use change(key, new_value) method.
# To delete a key from the database, call delete(key) method.
# To view the keys and values pf your database, use display() method.
# To get the value of a certain key, use get(key) method.
# To check if a key is found in database or not, use isfound(key) method.
# To clear all the rows in the database, use clear_all().
# To delete the database you are working with, call delete_this_database() method.
# To delete another database, use deleteDataBase(directory, name) function, where directory is where you store the database, and name is its name
# Finally, don't forget to save the database using save() method, if you forget to save it, all the changes
# won't be saved and you need to work again, so be careful.
# However, you can enable autosaving by calling enable_autosave(), and you can disable it by calling disable_autosave().
# Note that enabling autosave is not recommended for big databases (rows >= 10000), manual saving it better.


# If you want to create the database in the current folder, just put the path as empty string and set current_directory to True, for example:
# db = DataBase("", "MyDb", current_directory=True)


class DataBase:
    def __init__(self, path='', name='', current_directory=False):
        """Initializes a DataBase with a path and name"""
        self.dir = path
        self.name = name
        self.auto = False
        self.curr = current_directory
        if self.curr: self.path = self.name+".py"
        else: self.path = path + "\\" + self.name + ".py"
        if self.exist():
            self.load()
        else:
            self.create()
            self.db = {}

    
    def exist(self):
        """Checks if the current database exists or not"""
        return os.path.isfile(self.path)



    def create(self):
        """Creates the database in the path passed before, and gives it the name you passed before"""
        if os.path.isfile(self.path):
            raise Exception("The database is already created, please use load() instead of create()")
        try:
            if self.curr:
                file = open(self.path, "w+")
                file.write("DataBase = {}")
                file.close()
                return
            file = open(self.path, "w+")
            file.write("DataBase = {}")
            file.close()
        except FileNotFoundError as msg:
            print(msg)

   
    def load(self):
        """Loads an existing database, with the name you passed when instantiated it"""
        if not os.path.isfile(self.path):
            raise Exception("The database is not created yet, please use create() instead of load()")
        try:
            if self.curr:
                database = __import__(self.name)
                self.db = database.DataBase
                return
        except ImportError as msg:
            print(msg)
        
        try:
            sys.path.insert(1, self.dir)
        except FileNotFoundError as msg:
            print(msg)

        try:
            database = __import__(self.name)

        except ImportError as msg:
            print(msg)

    
    def add(self, key, value):
        """Add key with corresponding value to the database"""
        try:
            if self.db.get(key):
                raise KeyError("The key is already found in the database, you may use the override method. to override it.")
            self.db[key] = value

            if self.auto: self.save()

        except KeyError as msg:
            print(msg)


    def add_keys(self, dictionary):
        """Add multiple keys in one time"""
        try:
            for key in dictionary:
                self.db[key] = dictionary[key]
        except KeyError as msg:
            print("Key Error: " + msg)


    def change(self, key, new_value):
        """Overrides existing keys' values by new_value"""
        try:
            if not self.db.get(key):
                raise KeyError("The key is not found in the database, you may add it using add_key method.")

            self.db[key] = new_value

            if self.auto: self.save()

        except KeyError as msg:
            print(msg)

    
    def delete(self, key):
        """Deletes the specified key"""
        try:
            del self.db[key]
            if self.auto: self.save()

        except KeyError as msg:
            print(msg)


    def get(self, key):
        """Returns the value of the passed key"""
        assert(self.isfound(key))
        return self.db[key]


    def get_keys(self, *args):
        """Returns a sub-database of the given keys"""
        sub_db = {}
        for key in args:
            sub_db[key] = self.db[key]

        return sub_db
    
    
    def keys(self):
        """Returns the list of keys found in the database"""
        return self.db.keys();


    def values(self):
        """Returns the list of values in the database"""
        return self.db.values();
    

    def isfound(self, key):
        """Returns a bool if the key is found in the database or not"""
        return (key in self.db)


    def clear_all(self):
        """Clears all the rows of the database"""
        self.db = {}
        self.save()


    def display(self):
        """Prints each key with its corresponding value in a clean way"""
        for key, value in self.db.items():
            print(key, ':', value)


    def delete_this_database(self):
        """Deletes the current database you are working with"""
        try:
            import os
            if not self.curr: os.remove(self.path+"\\"+self.name+".py")
            else: os.remove(self.name+".py")
            print(f"The DataBase {self.name} has been deleted.")
        except FileNotFoundError as msg:
            raise FileNotFoundError(msg)


    def enable_autosave(self):
        """Enables auto saving every time you make a change"""
        self.auto = True


    def disable_autosave(self):
        """Disables auto saving"""
        self.auto = False


    def save(self):
        """Saves the database, notice that without saving it, nothing in the database will change so be careful"""
        file = open(self.path, "w+")
        file.write("DataBase = ")
        file.write(str(self.db))
        file.close()


    def copy(self, other):
        """Copies the other database into the current database, which will remove it"""
        self.db = other.db


    def merge(self, other, path, name, curr=False):
        """Merges two databases into one
        Notice that if there exist two keys which are the same, one of them will
        disappear
        """
        new_db = self.db
        for key in other.db:
            new_db[key] = other.db.get(key)

        other.delete_database()
        self.db = new_db


    def __str__(self):
        return "<Key-Value DataBase: " + str(len(self.db)) + " row(s)>"


def deleteDataBase(dirc, name):
    try:
        import os
        if dirc == "":
            os.remove(name+".py")
            return
        os.remove(dirc+'\\'+name+'.py')
        print(f"Database {name} has been deleted.")
    except FileNotFoundError:
        raise FileNotFoundError("No such a file or directory")