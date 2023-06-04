#!/usr/bin/python3
import cmd

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from shlex import split
import re
import json

"""Console to
manage
hbnb data
"""


class HBNBCommand(cmd.Cmd):
    """Type class HBNBCommand CLI"""
    prompt = '(hbnb) '
    __classes = {
        'BaseModel',
        'Amenity',
        'Place',
        'User',
        'State',
        'Review',
        'City'
    }

    def emptyline(self):
        """Type method emptyline"""
        pass

    def do_quit(self, line):
        """Exits the shell"""
        return True

    def do_EOF(self, line):
        """Exit the shell"""
        print()
        return True

    def do_create(self, args):
        """Type method create"""
        if not args:
            print('** class name missing **')
        elif args not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
        else:
            cls_d = {'BaseModel': BaseModel, 'User': User, 'Amenity': Amenity,
                     'City': City, 'Place': Place,
                     'Review': Review, 'State': State}
            new_obj = cls_d[args]()
            new_obj.save()
            print('{}'.format(new_obj.id))
            storage.save()

    def do_show(self, line):
        """Type method show"""
        arg = line.split()
        obj_dict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, line):
        """Type method destroy"""
        arg = line.split()
        obj_dict = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, args):
        """Type method all"""
        yes = 0
        all_obj = [str(v) for v in storage.all().values()]
        if not args:
            yes = 1
            print('{}'.format(all_obj))
        elif args:
            arg_list = args.split()
        if args and arg_list[0] in HBNBCommand.__classes:
            yes = 1
            all_obj = storage.all()
            name = arg_list[0]
            all_obj = [str(v) for k, v in all_obj.items()
                       if name == v.__class__.__name__]
            print(all_obj)

        if yes != 1:
            print('** class doesn\'t exist **')

    def do_update(self, args):
        """Type method update"""
        args_ = args.split()
        if not args:
            print('** class name missing **')
            return
        else:
            up_dir = re.search(r"(?<=\{)([^\}]+)(?=\})", args)
            all_obj = storage.all()
            yes = 0

        if args_[0] not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
        elif len(args_) < 2:
            print('** instance id missing **')
        else:
            for k, v in all_obj.items():
                iddd = args_[1].replace('"', '').replace(',', '')
                name_nw = args_[0] + '.' + iddd
                if name_nw == k:
                    yes = 1
                    if up_dir:

                        s_d = up_dir.group()
                        dir_s = '{' + s_d[:] + '}'
                        dir_s1 = dir_s.replace('\'', '"')
                        dir_ob = json.loads(dir_s1)
                        for u_k, u_v in dir_ob.items():
                            if u_k and u_v:
                                setattr(v, u_k, u_v)
                                storage.all()[name_nw].save()
                        return

                    elif len(args_) == 2:
                        print("** attribute name missing **")
                    elif len(args_) == 3:
                        print("** value missing **")
                    else:
                        value1 = str(args_[3]).replace('"', '')
                        valuee = value1.replace(',', '')
                        namev = str(args_[2]).replace('"', '').replace(',', '')
                        setattr(v, namev, valuee)
                        storage.all()[name_nw].save()
            if yes != 1:
                print("** no instance found **")

    def do_count(self, line):
        """Type method count"""
        arg = line.split()
        counter = 0
        for obj in storage.all().values():
            if arg[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def default(self, arg):
        """Type method default"""
        m_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        m = re.search(r"\.", arg)
        if m is not None:
            marg = [arg[:m.span()[0]], arg[m.span()[1]:]]
            m = re.search(r"\((.*?)\)", marg[1])
            if m is not None:
                cmd = [marg[1][:m.span()[0]], m.group()[1:-1]]
                if cmd[0] in m_dict.keys():
                    if cmd[0] == 'update':
                        up_dir = re.search(r"(?<=\{)([^\}]+)(?=\})", cmd[1])
                        up = cmd[1].split()
                        idd = up[0].replace('"', '').replace(',', '')
                        if up_dir:
                            content = up_dir.group()
                            dir_s = '{' + content[:] + '}'
                            r_ar = "{} {} {}".format(marg[0], idd, dir_s)
                            return m_dict['update'](r_ar)
                    get = "{} {}".format(marg[0], cmd[1].replace('"', ''))
                    return m_dict[cmd[0]](get)
        print("*** Unknown syntax: {}".format(arg))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
