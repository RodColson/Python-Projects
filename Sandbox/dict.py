# Creating an empty dictionary
data = {}
# OR
data = dict()

# Creating a dictionary with initial values
data = {'a':1,'b':2,'c':3}
# OR
data = dict(a=1, b=2, c=3)
# OR
data = {k: v for k, v in (('a', 1),('b',2),('c',3))}

# Inserting/Updating a single value
data['a']=1  # Updates if 'a' exists, else adds 'a'
# OR
data.update({'a':1})
# OR
data.update(dict(a=1))
# OR
data.update(a=1)

# Inserting/Updating multiple values
data.update({'c':3,'d':4})  # Updates 'c' and adds 'd'

# Creating a merged dictionary without modifying originals
data3 = {}
data3.update(data)  # Modifies data3, not data
data3.update(data2)  # Modifies data3, not data2

# Deleting items in dictionary
del data[key]  # Removes specific element in a dictionary
data.pop(key)  # Removes the key & returns the value
data.clear()  # Clears entire dictionary

# Check if a key is already in dictionary
key in data

# Iterate through pairs in a dictionary
for key in data: # Iterates just through the keys, ignoring the values
for key, value in d.items(): # Iterates through the pairs
for key in d.keys(): # Iterates just through key, ignoring the values
for value in d.values(): # Iterates just through value, ignoring the keys

# Create a dictionary from 2 lists
data = dict(zip(list_with_keys, list_with_values))