#!/usr/bin/python3
""" Console Module """
import cmd
import re
import sys

from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'State': State, 'City': City, 'User': User, 'Review': Review, 'Place': Place
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def parse_attr(self, args):
        """Parses class attributes and returns a dictionary representation"""
        arg_dict = {}
        for x in range(1, len(args)):
            tmp = args[x].split("=")
            arg_dict[tmp[0]] = tmp[1]
        new_dict = {}
        for key, value in arg_dict.items():
            if isinstance(value, str):
                new_dict[key] = value.replace("_", " ").replace("", '')
            else:
                new_dict[key] = value
        return new_dict

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""

        args = args.split(' ')[0]  # remove possible trailing args
        if args and args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        records = storage.all(args)
        result = f'[{", ".join(str(value) for value in records.values())}]'
        print(result)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] != '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    def precmd(self, line: str):
        try:
            _fn = 'do_' + line.split(' ')[0]
            if getattr(self, _fn) is not None:
                return super().precmd(line)
        except (AttributeError):
            try:
                ln = self.preprocess_input(line)
                return super().precmd(ln)
            except (AttributeError, TypeError, ValueError, IndexError):
                return super().precmd(line)

        return super().precmd(line)

    def do_create(self, *args):
        """Create a new model"""
        _args = (str(args[0]).split(' '))
        kw = self.parse_attr_v2(_args[1:])

        if len(_args) < 1 or args[0] == '':
            print('** class name missing **')
            return
        _Class = self.classes.get(_args[0])
        if _Class is None:
            print("** class doesn't exist **")
            return

        try:
            instance = _Class()
            for k in kw:
                if k in self.types:
                    setattr(instance, k, self.types[k](kw[k]))
                else:
                    setattr(instance, k, kw[k])
            instance.save()
            print(instance.id)
        except AttributeError:
            pass

    def parse_attr_v2(self, args):
        """Parses class attributes and returns a dictionary representation"""
        arg_dict = {}
        for x in range(0, len(args)):
            tmp = args[x].split("=")
            arg_dict[tmp[0]] = tmp[1]
        new_dict = {}
        for key, value in arg_dict.items():
            if isinstance(value, str):
                new_dict[key] = value.replace("_", " ").replace('"', '')
            else:
                new_dict[key] = value
        return new_dict

    def preprocess_input(self, line: str):
        args = [self.remove_quotes(x)
                for x in self.tokenize_string(line)]
        _entity = args[0]
        _method = args[1]
        _args = args[2:]
        if getattr(self, 'do_' + _method) is not None:
            return ' '.join([_method, _entity] + _args)

    def remove_quotes(self, input: str):
        if input.startswith(('"', "'")) and input.endswith(('"', "'")):
            return input[1:-1]
        else:
            return input

    def tokenize_string(self, input_string):
        if input_string is None or len(input_string) == 0:
            return ['']
        pattern = r'([A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*)\.([A \
        -Za-z_][A-Za-z0-9_]*)\(([^)]*)\)'

        match = re.match(pattern, input_string)
        if match:
            class_name = match.group(1)
            method_name = match.group(3)
            args = [arg.strip() for arg in match.group(4).split(',')]
            return [class_name, method_name] + args

        return None


if __name__ == "__main__":
    HBNBCommand().cmdloop()
