import pandas as pd
import numpy as np
import math

# ID3 decision tree implementation
class DecisionTree:

    options = {}
    
    def __init__(self, data):

        self.data = data
        self.data_size = len(data)
        self.attribute_list = set()
        self.dataset_classes = self.determine_classes(self.data)
        self.most_common_class = max(self.dataset_classes, key = self.dataset_classes.get)
        self.information_gain = self.gain(data)
        self.attribute_size = len(self.information_gain)
        self.decisionTree = self.generate_dt()

    # Class Methods
    def generate_dt(self):
        for attribute in self.information_gain.keys():
            self.attribute_list.add(attribute)
        DT = self.generate_dt_recursive(self.data, self.attribute_list.copy())
        return DT

    # Generates a decision tree given 'training data'
    # data format is expected to be a list of tuples as specified in the assignment 2 document.
    def generate_dt_recursive(self, data, attributeList = None):
        node = DTree()
        classes = self.determine_classes(data)
        attribute_list_empty = not bool(attributeList)

        # Case 1: All samples are all of the same class C, label node as class
        if len(classes) == 1:
            for key in classes:
                node = DTree(key)

        # Case 2: Checks if all attributes have been used, assigns majority class
        elif attribute_list_empty:
            node = DTree(self.most_common_class)
        
        else:
            # Assigns attribute to the attribute with highest information gain
            attribute = None
            self.information_gain = self.gain(data)

            for index in range(self.attribute_size):
                attribute = max(self.information_gain, key = self.information_gain.get)
                self.information_gain.pop(attribute)
                if attribute in attributeList:
                    break

            attributeList.remove(attribute)
            node = DTree(attribute)

            for option in self.options[attribute]:
                samples = self.generate_samples(data, attribute, option)
                samples_has_items = bool(samples)

                if samples_has_items:
                    node.add_child(option, self.generate_dt_recursive(samples, attributeList))
                else:
                    node.add_child(option, DTree(self.most_common_class))

            # Adds 'None" option to every attribute to handle missing data.
            classes = self.determine_classes(data)
            most_common_class = max(classes, key = classes.get)
            node.add_child(None, DTree(most_common_class))

        return node
    
    # Calculates information gain of every attribute in self.data
    def gain (self, data):

        attributes_gain = {}
        dataset_entropy = 0

        # Calculates entropy of entire dataset
        for key, value in self.dataset_classes.items():
            coefficient = value/self.data_size
            dataset_entropy = dataset_entropy - coefficient * math.log(coefficient,2)

        # Calculates entropy for each attribute
        attributes_entropy = {}

        for attribute in data[:][0][0]:

            self.options[attribute] = self.generate_options(data, attribute)

            for option, value in self.options[attribute].items():

                option_entropy = 0
                total = 0

                for key in value:
                    total += value[key]

                for opt_class, value in self.options[attribute][option].items():
                    coefficient = value/total
                    option_entropy = option_entropy - coefficient * math.log(coefficient,2)

                attribute_entropy = (total/self.data_size) * option_entropy

                if attribute not in attributes_entropy:
                    attributes_entropy[attribute] = attribute_entropy
                else:
                    attributes_entropy[attribute] += attribute_entropy

            attributes_gain[attribute] = dataset_entropy - attributes_entropy[attribute]

        return attributes_gain

    # Calculates all 'classes' defined in the dataset and returns a dictionary
    # in which each key is a class and the corresponding value is the number of 
    # times that class appears in the training data.
    def determine_classes(self, data):

        classes = {}
        # Generates classes for entire dataset
        for entry in data:
            entry_class = str(entry[1])
            if entry_class not in classes:
                classes[entry_class] = 1
            else:
                classes[entry_class] += 1
        return classes

    # Given a specified attribute, finds all 'options' or entries that attribute has in the
    # training data. ALso, retains what options led to what classes 
    def generate_options(self, data, attribute):

        options = {}
        # Counts classes based on choices of attribute
        for entry in data:
            entry_class = entry[1]
            option = entry[0][attribute]
            if option not in options:
                options[option] = {entry_class: 1}         
            else:
                if entry_class not in options[option]:
                    options[option][entry_class] = 1
                else:
                    options[option][entry_class] += 1
        return options
    
    def generate_samples(self, data, attribute, option):

        samples = []
        for entry in data:
            if entry[0][attribute] == option:
                samples.append(entry)
        return samples
    
    def classify(self, data):

        classification = None
        current_node = self.decisionTree

        while classification is None:

            if current_node.name in data:
                option = data[current_node.name]
                if option in current_node.children:
                    current_node = current_node.children[option]
                else:
                    current_node = current_node.children[None]

            elif current_node.name in self.dataset_classes:
                classification = current_node.name
                break   

            else:
                classification = current_node.children[None].name
                break

        return classification 


class DTree:

    def __init__(self, name = 'root'):

        self.name = name
        self.children = {}
        self.children_amount = len(self.children)
        self.node = (self.name, self.children)
    
    def add_child(self, option, node):

        self.children[option] = node
        self.children_amount = len(self.children)
        self.node = (self.name, self.children)
    
    def traverse(self, option):
        return self.children[option]

    def display(self, indent = 0, space = 0, new_line = True):

        if self.children_amount > 0:
            if new_line:
                print(f"('{self.name}',", end = '\n')
            else:
                print(f"('{self.name}',", end = '')

            count = 0
            space = 1
            new_line = False

            for branch, node in self.children.items():

                count += 1

                if count == 1:
                    print('\t' * indent + ' ' * space + '{' + f"'{branch}'", end = ':')
                else:
                    print('\t' * indent + ' ' * space + f"'{branch}'", end = ':')

                node.display(indent, space, new_line)

            print('})', end = '\n')

        elif self.children_amount == 0:

            if new_line:
                print(f"'{self.name}'", end = '\n')
            else:
                print(f"'{self.name}'", end = ',')

        else:
            print("error, negative children")