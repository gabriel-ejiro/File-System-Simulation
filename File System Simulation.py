#!/usr/bin/env python
# coding: utf-8

# 
# - Implement a FileSystemComponent interface or abstract class with methods like get_size() and display(indent=0).
# 
# To achieve this, we first need to import the necessary decorators from python’s built-in abc module to our notebook. It is the abc module that allows us create abstract classes in our code.
# 
# Next, we define our FileSystemComponent class which model a generic file system entity. Also, two abstract methods would be defined to get the size of the file and also display it.
# 
# 

# In[28]:


from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def display(self, indent=0):
        pass


# Create two concrete classes:
#                     File: representing a single file with a name and size.
#                     Folder: containing multiple files and folders.
# 

# In[29]:


class File(FileSystemComponent):
    def __init__(self, name, size):
        super().__init__(name)
        self._size = size


    def get_size(self):
        return self._size

    def display(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self._size} KB)")


# In[30]:


class Folder(FileSystemComponent):
    def __init__(self, name):
        super().__init__(name)
        self._children = []

    def add(self, component: FileSystemComponent):
        self._children.append(component)

    def remove(self, component: FileSystemComponent):
        self._children.remove(component)

    def get_size(self):
        return sum(child.get_size() for child in self._children)

    def display(self, indent=0):
        print(" " * indent + f"📁 {self.name}/")
        for child in self._children:
            child.display(indent + 2)


# In[7]:


def main():
    root = Folder("root")
    root.add(File("README.md", 5))
    root.add(File("setup.py", 2))

    src = Folder("src")
    src.add(File("main.py", 15))
    src.add(File("utils.py", 7))

    assets = Folder("assets")
    assets.add(File("logo.png", 150))
    assets.add(File("bg.jpg", 300))

    root.add(src)
    root.add(assets)

    print("\n🗂 File System Structure:\n")
    root.display()

    print(f"\n📦 Total size of 'root': {root.get_size()} KB\n")

main()


# Add file types and filtering by file extension

# In[25]:


class File(FileSystemComponent):
    def __init__(self, name, size):
        super().__init__(name)
        self._size = size

    def get_size(self):
        return self._size

    def get_extension(self):
       
        if '.' in self.name:
            return self.name[self.name.rindex('.'):]
        return ''

    def display(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self._size} KB)")


# Implement a method to find a file by name (search).

# In[33]:


class Folder(FileSystemComponent):


    def search(self, filename, path=""):
        matches = []
        current_path = f"{path}/{self.name}"
        for child in self._children:
            if isinstance(child, File):
                if filename.lower() in child.name.lower():
                    matches.append(f"{current_path}/{child.name}")
            elif isinstance(child, Folder):
                matches.extend(child.search(filename, current_path))
        return matches


#  Add permissions and modification dates

# In[23]:


from datetime import datetime

class File(FileSystemComponent):
    def __init__(self, name, size, permissions="rw-r--r--", mod_date=None):
        super().__init__(name)
        self._size = size
        self.permissions = permissions
        self.mod_date = mod_date or datetime.now()

    def display(self, indent=0):
        date_str = self.mod_date.strftime("%Y-%m-%d %H:%M:%S")
        print(" " * indent + f"📄 {self.name} ({self._size} KB) [{self.permissions}] (Modified: {date_str})")

class Folder(FileSystemComponent):
    def __init__(self, name, permissions="rwxr-xr-x", mod_date=None):
        super().__init__(name)
        self._children = []
        self.permissions = permissions
        self.mod_date = mod_date or datetime.now()

    def display(self, indent=0):
        date_str = self.mod_date.strftime("%Y-%m-%d %H:%M:%S")
        print(" " * indent + f"📁 {self.name}/ [{self.permissions}] (Modified: {date_str})")
        for child in self._children:
            child.display(indent + 2)


#  Export structure to .txt or .json

# In[31]:


import json

class File(FileSystemComponent):
  

    def to_dict(self):
        return {
            "type": "file",
            "name": self.name,
            "size": self._size,
            "permissions": self.permissions,
            "modification_date": self.mod_date.isoformat()
        }

class Folder(FileSystemComponent):
  
    def to_dict(self):
        return {
            "type": "folder",
            "name": self.name,
            "permissions": self.permissions,
            "modification_date": self.mod_date.isoformat(),
            "children": [child.to_dict() for child in self._children]
        }

    def export_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)


# In[ ]:




