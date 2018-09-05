"""Example Google style docstrings."""

import json
import os
import shlex
import subprocess

from subprocess import PIPE, Popen

import sublime

import sublime_plugin

from . import auralint


from . import semver

IS_WINDOWS = os.name == 'nt'
PROJECT_DIRECTORY = os.getcwd()


def plugin_loaded():
    """Make me put in a doc string."""
    print("WE ARE TOTALLY LOADED!")
    try:
        p = popen_force_cli(["version"])
        version, err = p.communicate()
        if err:
            sublime.error_message(err.decode("utf-8"))
        else:
            ver = version.decode("utf-8").replace("\n", "")

        if ver != "dev":
            ver = ver[1:]
            if semver.match(ver, "<0.22.26"):
                message = (u"Sublime Lightning\n\n" +
                           u"You are using version " + ver + " of the " +
                           u"Force CLI.\n\nThis version of Sublime Lightning" +
                           u" requires version 0.22.26 or greater.\n\n" +
                           u"Please download the latest version from " +
                           u"force-cli.herokuapp.com")
                sublime.error_message(message)
    except:
        sublime.error_message("Sublime Lightning requires the " +
                              "Force.com CLI to function.\n\n" +
                              "Please visit force-cli.herokuapp.com to " +
                              "install the Force.com CLI.\n\n" +
                              "If you’ve already installed it, make sure " +
                              "that you saved it or created a " +
                              "symlink to it in Sublime’s default path.")
    return


def log(msg, level=None):
    """Log to ST python console.

    If log level 'debug' (or None) print only if debug setting is enabled.
    """
    if level is None:
        level = 'debug'

    print("[Flake8Lint {0}] {1}".format(level.upper(), msg))


def quote(subprocess_arg):
    return shlex.quote(subprocess_arg) if IS_WINDOWS else subprocess_arg


def popen_force_cli(quoted_args):
    args = ['force']
    args.extend(quoted_args)
    return subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=open(os.devnull, 'w'),
                            shell=IS_WINDOWS)


class Helper(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def foo(self):
        """Sample doc string."""
        return

    def install_cli(self):
        """Sample doc string."""
        return

    def get_xml_snippet(self, md_type):
        return '<?xml version="1.0" encoding="UTF-8"?>\n' \
            + '<' + md_type \
            + ' xmlns="http://soap.sforce.com/2006/04/metadata">\n' \
            + '<apiVersion>38.0</apiVersion>\n' \
            + '<status>Active</status>\n' \
            + '</' + md_type + '>'

    def get_page_xml_snippet(self, page_name):
        return '<?xml version="1.0" encoding="UTF-8"?>\n' \
            + '<ApexPage xmlns="http://soap.sforce.com/2006/04/metadata">\n' \
            + '\t<apiVersion>36.0</apiVersion>\n' \
            + '\t<availableInTouch>false</availableInTouch>\n' \
            + '\t<confirmationTokenRequired>false' \
            + '</confirmationTokenRequired>\n' \
            + '\t<label>' + page_name + '</label>\n' \
            + '</ApexPage>'

    def get_immediate_subdirectories(self, dir):
        return [name for name in os.listdir(dir)
                if os.path.isdir(os.path.join(dir, name))]

    def bundle_op_is_visible(self, dirs):
        """Sample doc string."""
        cdpath = Helper(self.window).get_md_child_name(dirs[0])
        ismetadata = os.path.basename(dirs[0]) in ["metadata", "src"]
        isclasses = os.path.basename(dirs[0]) == "classes"
        if cdpath == "":
            cdpath = Helper(self.window).find_upstram_md(dirs[0])
        if (cdpath != "") or ismetadata or isclasses:
            return True

    def file_op_is_visible(self, dirs):
        """Sample doc string."""
        return self.parent_dir_is_aura(dirs[0])

    def dir_is_aura(self, working_dir):
        """Sample doc string."""
        return os.path.basename(working_dir) == "aura"

    def parent_dir_is_aura(self, working_dir):
        """Sample doc string."""
        return os.path.basename(os.path.dirname(working_dir)) == "aura"

    def get_md_child_name(self, dir):
        for dirname in self.get_immediate_subdirectories(dir):
            if dirname in ["metadata", "src"]:
                return os.path.join(dir, dirname)
        return ""

    def get_md_dir(self, dir):
        working_dir = self.get_md_child_name(dir)
        if working_dir == "":
            working_dir = Helper.find_upstram_md(self, dir)
        if working_dir == "not found":
            if sublime.ok_cancel_dialog(
                    "Could not locate a src or metadata directory. "
                    "Create a metadata directory at " + dir + "?",
                    "Create Metadata"):
                working_dir = os.path.join(dir, "metadata")
                os.mkdir(working_dir)

        return working_dir

    def is_metadata(self, working_dir):
        """Sample doc string."""
        wd = os.path.dirname(working_dir)
        print("Working dir: " + working_dir)
        print("wd: " + wd)
        return os.path.basename(wd) in ["metadata", "src"]

    def is_static_resource(self, file):
        """Sample doc string."""
        for root, dirs, files in Helper.walk_up(self, file):
            if "staticresources" in dirs:
                return True

        return False

    def get_resource_name(self, file):
        """Sample doc string."""
        for root, dirs, files in Helper.walk_up(self, os.path.dirname(file)):
            if os.path.basename(os.path.dirname(root)) == "staticresources":
                return os.path.basename(root)

    def is_bundle_type(self, working_dir, comp_type):
        """Sample doc string."""
        files = os.listdir(working_dir[0])
        for filename in files:
            fname, fext = os.path.splitext(filename)
            if (fext == "." + comp_type):
                return True
        return False

    def has_this_file(self, working_dir, filename):
        """Sample doc string."""
        return os.path.exists(os.path.join(working_dir, filename))

    def do_login(self, username, password, instance):
        """Sample doc string."""
        if username == "interactive":
            self.window.run_command(
                'exec',
                {'cmd': ["force", "login"]})
        else:
            if instance == "":
                self.window.run_command(
                    'exec',
                    {'cmd': ["force",
                             "login",
                             "-u",
                             username, "-p", password]})
            else:
                self.window.run_command(
                    'exec',
                    {'cmd': ["force", "login", "-u", username, "-p", password,
                             "-i", instance]})
        return

    def do_aura_query(self):
        """Sample doc string."""
        return

    def do_fetch(self, bundle, adir):
        """Sample doc string."""
        os.chdir(adir)
        if (bundle == 'all'):
            self.window.run_command(
                'exec',
                {'cmd': ["force", "fetch", "-t", "aura", "-d", adir],
                 'working_dir': adir})
        else:
            self.window.run_command(
                'exec',
                {'cmd': ["force", "fetch", "-t", "aura", "-n", bundle, "-d",
                         adir], 'working_dir': adir})

        return

    def get_instance_url(self):
        """Sample doc string."""
        p = popen_force_cli(['active', '-j'])
        out = p.communicate()[0]
        data = json.loads(out.decode("utf-8"))
        return data["instanceUrl"]

    def get_namespace(self):
        """Sample doc string."""
        p = popen_force_cli(['active', '-j'])
        out = p.communicate()[0]
        data = json.loads(out.decode("utf-8"))
        return data["namespace"]

    def get_app_name(self, adir):
        """Sample doc string."""
        os.chdir(adir)
        return os.path.basename(adir)

    def open_selected_bundle(self, index):
        """Sample doc string."""
        if (index == -1):
            return

        if (index == 0):
            self.do_fetch("all", self.activedir)
        else:
            self.do_fetch(self.messages[index][2], self.activedir)
        return

    def open_selected_metadata(self, index):
        """Sample doc string."""
        if (index == -1):
            return

        self.show_metadata_instance_list(self.messages[index][0],
                                         self.activedir)
        return

    def fetch_selected_metadata(self, index):
        """Sample doc string."""
        if index == -1:
            return
        item = self.messages[index][0]
        print("Type: " + self.type)
        print("Item: " + item)
        self.window.run_command(
            'exec',
            {'cmd': ["force", "fetch", "-t", self.type, "-n", item, "-unpack"],
             'working_dir': self.activedir})
        return

    def meets_forcecli_version(self, minversion):
        """Sample doc string."""
        version = Helper.get_forcecli_version(self)
        # version = version[1:]
        print("Version: " + version + ", min: " + minversion)
        if version == "dev":
            return version == "dev"
        return semver.match(version, ">=" + minversion)

    def lint_error_to_message(self, linterror):
        """Sample doc string."""
        return

    def get_forcecli_version(self):
        """Sample doc string."""
        try:
            p = popen_force_cli(["version"])
            version, err = p.communicate()
            if err:
                sublime.error_message(err.decode("utf-8"))
            else:
                ver = version.decode("utf-8").replace("\n", "")

            if ver != "dev":
                ver = ver[1:]
                if semver.match(ver, "<0.22.26"):
                    message = (u"Sublime Lightning\n\n" +
                               u"You are using version " + ver + " of the " +
                               u"Force CLI.\n\nThis version of Sublime " +
                               u"Lightning" +
                               u" requires version 0.22.26 or greater.\n\n" +
                               u"Please download the latest version from " +
                               u"force-cli.herokuapp.com")
                    sublime.error_message(message)
        except:
            sublime.error_message("Sublime Lightning requires the " +
                                  "Force.com CLI to function.\n\n" +
                                  "Please visit force-cli.herokuapp.com to " +
                                  "install the Force.com CLI.\n\n" +
                                  "If you’ve already installed, make sure " +
                                  "that you saved it or created a " +
                                  "symlink to it in Sublime’s default path.")
        return ver.replace("\n", "")

    def show_metadata_instance_list(self, metaname, activedir):
        """Sample doc string."""
        self.type = metaname
        self.activedir = activedir
        self.messages = []
        p = popen_force_cli(["describe", "-t", "metadata", "-n",
                            quote(metaname), "-j"])
        result, err = p.communicate()
        if err:
            sublime.error_message(err.decode("utf-8"))
        else:
            try:
                m = json.loads(result.decode("utf-8"))
                if str(m) == "None":
                    sublime.message_dialog(
                        "There are no instances of " + metaname +
                        " in this org.")
                    return

                for mm in m:
                    x = [mm['FullName'], "Modified by: " +
                         mm['LastModifiedByName'],
                         "File name: " + mm['FileName'],
                         "Id: " + mm['Id']]
                    self.messages.append(x)
                    print(x)

                self.window = sublime.active_window()
                sublime.set_timeout(
                    lambda:
                    self.window.show_quick_panel(
                        self.messages,
                        self.fetch_selected_metadata,
                        sublime.MONOSPACE_FONT), 10)
            except:
                return

    def open_url(self, url):
        """Sample doc string."""
        self.window.run_command(
            'exec',
            {'cmd': ["open", url]}
        )

    def show_metadata_type_list(self, activedir):
        """Sample doc string."""
        working_dir = self.get_md_dir(activedir)
        if working_dir == "not found":
            self.open_selected_bundle(-1)
            return

        self.activedir = activedir
        self.messages = []
        p = popen_force_cli(["describe", "-t", "metadata", "-j"])
        result, err = p.communicate()
        if err:
            sublime.error_message(err.decode("utf-8"))
        else:
            try:
                m = json.loads(result.decode("utf-8"))
                for mm in m:
                    x = [mm['XmlName'], "In folder: " + mm['DirectoryName'],
                         "Suffix: " + mm['Suffix']]
                    self.messages.append(x)

                self.window = sublime.active_window()
                self.window.show_quick_panel(self.messages,
                                             self.open_selected_metadata,
                                             sublime.MONOSPACE_FONT)

            except:
                print("There was some kind of error...")
                return

    def show_package_list(self):
        """Sample doc string."""
        self.messages = []
        p = popen_force_cli(["describe", "-t", "metadata", "-j"])
        result, err = p.communicate()
        if err:
            sublime.error_message(err.decode("utf-8"))
        else:
            try:
                m = json.loads(result.decode("utf-8"))
                for mm in m:
                    x = [mm['XmlName'], "In folder: " + mm['DirectoryName'],
                         "Suffix: " + mm['Suffix']]
                    self.messages.append(x)

                self.window = sublime.active_window()
                self.window.show_quick_panel(self.messages,
                                             self.open_selected_metadata,
                                             sublime.MONOSPACE_FONT)

            except:
                return

    def show_bundle_list(self, activedir):
        """Sample doc string."""
        self.messages = []
        working_dir = self.get_md_dir(activedir)
        if working_dir == "not found":
            self.open_selected_bundle(-1)
            return

        self.activedir = activedir
        if Helper.meets_forcecli_version(self, "0.22.36"):
            print("Using --tooling and show list")
            p = popen_force_cli(["query", "Select Id,DeveloperName, "
                                 "MasterLabel, Description From "
                                 "AuraDefinitionBundle",
                                 "--format:json", "-t"])
        else:
            print("NOT using -t")
            p = popen_force_cli(["query", "Select Id,DeveloperName, "
                                 "MasterLabel, Description From "
                                 "AuraDefinitionBundle",
                                 "--format:json", "--tooling"])
        result, err = p.communicate()
        # if err:
        # errmessage = err.decode("utf-8")
        # if "Deprecated" in errmessage:
        #  self.show_list(result.decode("utf-8"))
        # else:
        # sublime.error_message(err.decode("utf-8"))
        # else:
        m = result.decode("utf-8")
        print("Data " + m)
        self.show_list(m)

    def show_list(self, data):
            m = json.loads(data)
            if len(m) == 0:
                sublime.message_dialog(
                    "There aren't any lightning components "
                    " in this org.")
                return

            print("data: " + str(m))
            self.messages.append(["All Bundles", "*", "Every Bundle",
                                  "All the lightning bundles "
                                  "in your org!"])
            print("And now here")
            for mm in m:
                x = [mm['MasterLabel'], mm['Id'], mm["DeveloperName"],
                     mm["Description"]]
                self.messages.append(x)

            self.window = sublime.active_window()
            self.window.show_quick_panel(self.messages,
                                         self.open_selected_bundle,
                                         sublime.MONOSPACE_FONT)

    def make_bundle_file(self, file_name,
                         bundle_type, extension, snippet, dirs):
        """Sample doc string."""
        metadata_dir = self.get_md_dir(dirs[0])
        if metadata_dir == "not found":
            return
        aura_dir = os.path.join(metadata_dir, "aura")
        if not os.path.isdir(aura_dir):
            os.mkdir(aura_dir)

        bundle_dir = os.path.join(aura_dir, file_name)
        e = extension
        if e == "cmp" or e == "app" or e == "intf" or e == "evt":
            fn, ex = os.path.splitext(file_name)
            os.mkdir(os.path.join(bundle_dir))

        file_path = os.path.join(bundle_dir,
                                 file_name + bundle_type + "." + extension)
        app = open(file_path, "wb")
        print("Writing " + snippet + " \nto: " + file_path)
        if int(sublime.version()) >= 3000:
            app.write(bytes(snippet, 'UTF-8'))
        else:  # To support Sublime Text 2
            app.write(bytes(snippet))

        app.close()
        self.window.open_file(file_path)
        cmd = 'push -f="' + file_path + '"'
        self.window.run_command(
            'exec',
            {'cmd': ["force", "aura", cmd]})

        return app

    def find_upstram_md(self, start_dir):
        print("start_dir: " + start_dir)
        for root, dirss, files in Helper.walk_up(self, start_dir):
            print("Root: " + root)
            print("Dirname for root: " + os.path.dirname(root))
            print(str(dirss))
            if "metadata" in dirss:
                working_dir = os.path.join(root, "metadata")
                print("Found metadata above: " + working_dir)
                return working_dir
            elif "src" in dirss:
                working_dir = os.path.join(root, "src")
                print("Found src above: " + working_dir)
                return working_dir
            elif os.path.dirname(root) == start_dir:
                print("Not found root and start_dir are the same.")
                return "not found"
            else:
                self.find_upstram_md(os.path.dirname(root))

    def do_quick_create(self, file_name, type, title_case_type, metadata_dir):
        res, err = Popen(['force', 'create',
                          '-w', type,
                          '-n', file_name],
                         stdout=PIPE,
                         stderr=PIPE).communicate()
        if len(err) != 0:
            sublime.error_message(str(err))

        else:
            self.window.run_command('exec',
                                    {'cmd': ["force", "fetch",
                                             "-t", title_case_type,
                                             "-n", file_name, "-unpack"],
                                     'working_dir': metadata_dir})

    def make_class_file(self, file_name, dirs):
        """Sample doc string."""
        metadata_dir = self.get_md_dir(dirs[0])
        if metadata_dir == "not found":
            return
        classes_dir = os.path.join(metadata_dir, "classes")
        if not os.path.isdir(classes_dir):
            os.mkdir(classes_dir)

        cls_file_path = os.path.join(classes_dir, file_name + ".cls")
        # xml_file_path = cls_file_path + "-meta.xml"
        if os.path.exists(cls_file_path):
            sublime.error_message("The class " +
                                  file_name +
                                  "already exists.")
            return

        self.do_quick_create(
            file_name,
            "apexclass",
            "ApexClass",
            metadata_dir)

    def make_page_file(self, file_name, dirs):
        """Sample doc string."""
        metadata_dir = self.get_md_dir(dirs[0])
        if metadata_dir == "not found":
            return
        pages_dir = os.path.join(metadata_dir, "pages")
        if not os.path.isdir(pages_dir):
            os.mkdir(pages_dir)

        page_file_path = os.path.join(pages_dir, file_name + ".cls")
        # xml_file_path = page_file_path + "-meta.xml"
        if os.path.exists(page_file_path):
            sublime.error_message("The class " +
                                  file_name +
                                  "already exists.")
            return

        self.do_quick_create(
            file_name,
            "visualforce",
            "ApexPage",
            metadata_dir)

    def make_vf_file(self, file_name, dirs):
        """Sample doc string."""
        working_dir = self.get_md_child_name(dirs[0])
        print("Metadata dir: " + working_dir)
        classes_dir = os.path.join(working_dir, "pages")
        if not os.path.isdir(classes_dir):
            os.mkdir(classes_dir)

        cls_file_path = os.path.join(classes_dir, file_name + ".page")
        xml_file_path = cls_file_path + "-meta.xml"
        print("cls_file_path: " + cls_file_path)
        print("xml_file_path: " + xml_file_path)
        if os.path.exists(cls_file_path):
            sublime.error_message("The class " +
                                  file_name +
                                  "already exists.")
            return

        cls = open(cls_file_path, "wb")
        cls_snippet = "public with sharing class " + file_name + " {"
        cls_snippet = cls_snippet + "\n\n}"
        if int(sublime.version()) >= 3000:
            cls.write(bytes(cls_snippet, 'UTF-8'))
        else:  # To support Sublime Text 2
            cls.write(bytes(cls_snippet))

        xml = open(xml_file_path, "wb")
        xml_snippet = self.get_xml_snippet("ApexClass")
        if int(sublime.version()) >= 3000:
            xml.write(bytes(xml_snippet, 'UTF-8'))
        else:  # To support Sublime Text 2
            xml.write(bytes(xml_snippet))

        xml.close()
        cls.close()

        self.window.open_file(cls_file_path)
        self.window.run_command(
            'exec',
            {'cmd': ["force", "push", "-f", cls_file_path]})

        return cls

    def get_aura_dir(self):
        """Sample doc string."""
        self.folders = self.window.folders()
        print(self.folders)
        return self.folders

    def walk_up(self, bottom):
        """
        Mimic os.walk, but walk 'up'.

        instead of down the directory tree
        """
        bottom = os.path.realpath(bottom)

        # get files in current dir
        try:
            names = os.listdir(bottom)
        except Exception as e:
            print(e)
            return

        dirs, nondirs = [], []
        for name in names:
            if os.path.isdir(os.path.join(bottom, name)):
                dirs.append(name)
            else:
                nondirs.append(name)

        yield bottom, dirs, nondirs

        new_path = os.path.realpath(os.path.join(bottom, '..'))

        # see if we are at the top
        if new_path == bottom:
            return

        for x in Helper.walk_up(self, new_path):
            yield x


class LoginCommand(sublime_plugin.WindowCommand):
    """This is my docstring."""

    def run(self):
        """Sample doc string."""
        version = Helper(self.window).get_forcecli_version()
        print("Checking the aura dir...")
        Helper(self.window).get_aura_dir()
        print("Running version " + version + " of Force CLI!")
        self.window.show_input_panel(
            "Username: ",
            "",
            self.get_password,
            None,
            None)
        pass

    def get_password(self, username):
        """Sample doc string."""
        if len(username) == 0:
            Helper(self.window).do_login("interactive", "", "")
        else:
            self.username = username
            self.window.show_input_panel(
                "Password: ",
                "",
                self.get_instance,
                None,
                None)
        pass

    def get_instance(self, password):
        """Sample doc string."""
        if (len(password) == 0) or (len(self.username) == 0):
            Helper(self.window).do_login("interactive", "", "")
        else:
            self.password = password
            self.window.show_input_panel(
                "Instance Url: ",
                "",
                self.do_login,
                None,
                None)
        pass

    def do_login(self, instance):
        """Sample doc string."""
        Helper(self.window).do_login(self.username, self.password, instance)
        return

    def is_visible(self):
        """Sample doc string."""
        return True


class FetchMetaCommand(sublime_plugin.WindowCommand):
    """This is my docstring."""

    def run(self, dirs):
        """Sample doc string."""
        print("Running FetchMetaCommand")
        Helper(self.window).show_metadata_type_list(dirs[0])

    def is_visible(self):
        """Sample doc string."""
        return True


class FetchPackageCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self):
        """Sample doc string."""
        print("Running FetchPackageCommand")
        Helper(self.window).show_package_list()

    def is_visible(self):
        """Sample doc string."""
        return True


class FetchCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        print("Running FetchLightningCommand")
        Helper(self.window).show_bundle_list(dirs[0])

    # def do_fetch(self, bundle):
    #    self.dirs = self.window.folders()
    #    Helper(self.window).show_bundle_list()
    #    return

    def is_visible(self):
        """Sample doc string."""
        return True


class ApexNewClassCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        if (Helper(self.window).meets_forcecli_version("0.22.62")):
            self.dirs = dirs
            self.window.show_input_panel("Class Name:",
                                         "", self.on_done, None, None)
            pass
        else:
            sublime.message_dialog("This feature requires at least version"
                                   " 62 of the Force")

    def on_done(self, file_name):
        """Sample doc string."""
        Helper(self.window).make_class_file(file_name, self.dirs)

        return

    def is_visible(self, dirs):
        """Sample doc string."""
        return Helper(self.window).bundle_op_is_visible(dirs)


class VisualforceNewPageCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        if (Helper(self.window).meets_forcecli_version("0.22.62")):
            self.dirs = dirs
            self.window.show_input_panel("Page Name:",
                                         "", self.on_done, None, None)
            pass
        else:
            sublime.message_dialog("This feature requires at least version"
                                   " 62 of the Force")

    def on_done(self, file_name):
        """Sample doc string."""
        Helper(self.window).make_page_file(file_name, self.dirs)

        return

    def is_visible(self, dirs):
        """Sample doc string."""
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewAppCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        self.window.show_input_panel("App Name:", "", self.on_done, None, None)
        pass

    def on_done(self, file_name):
        """Sample doc string."""
        Helper(self.window).make_bundle_file(
            file_name,
            "",
            "app",
            "<aura:application>\n\n</aura:application>",
            self.dirs)
        return

    def is_visible(self, dirs):
        """Sample doc string."""
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewComponentCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        self.window.show_input_panel(
            "Component Name:",
            "",
            self.on_done,
            None,
            None)
        pass

    def on_done(self, file_name):
        """Sample doc string."""
        Helper(self.window).make_bundle_file(
            file_name,
            "",
            "cmp",
            "<aura:component>\n\n</aura:component>",
            self.dirs)
        return

    def is_visible(self, dirs):
        """Sample doc string."""
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewEventCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        self.window.show_input_panel(
            "Event Name:",
            "",
            self.on_done,
            None,
            None)
        pass

    def on_done(self, file_name):
        """Sample doc string."""
        Helper(self.window).make_bundle_file(
            file_name,
            "",
            "evt",
            '<aura:event type="APPLICATION">\n\n</aura:event>',
            self.dirs)
        return

    def is_visible(self, dirs):
        """Sample doc string."""
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewInterfaceCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        self.window.show_input_panel(
            "Interface Name:",
            "",
            self.on_done,
            None,
            None)
        pass

    def on_done(self, file_name):
        """Sample doc string."""
        Helper(self.window).make_bundle_file(
            file_name,
            "",
            "intf",
            '<aura:interface description="Interface template">'
            '\n\t<aura:attribute name="example" type="String" default="" '
            'description="An example attribute."/>'
            '\n</aura:interface>',
            self.dirs)
        return

    def is_visible(self, dirs):
        """Sample doc string."""
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningPreviewCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        appname = Helper.get_app_name(self, dirs[0])
        url = Helper.get_instance_url(self)
        namespace = Helper.get_namespace(self)
        if len(namespace) == 0:
            url = url + "/c/" + appname + ".app"
        else:
            url = url + "/" + namespace + "/" + appname + ".app"

        Helper.open_url(self, url)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        isvalidbundle = helper.is_bundle_type(dirs, "app")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle


class LightningNewControllerCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "Controller",
            "js",
            "({\n"
            "\tmyAction: function(component, event, helper) {\n"
            "\t}\n"
            "})",
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Controller.js")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewSvgCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "",
            "svg",
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<svg width="120px" height="120px" viewBox="0 0 120 120" '
            'version="1.1" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink">\n'
            '\t<g stroke="none" stroke-width="1" fill="none" '
            'fill-rule="evenodd">\n'
            '\t\t<path d="M120,108 C120,114.6 114.6,120 108,120 L12,120 '
            'C5.4,120 '
            '0,114.6 0,108 L0,12 C0,5.4 5.4,0 12,0 L108,0 C114.6,0 120,5.4 '
            '120,12 L120,108 L120,108 Z" id="Shape" fill="#2A739E"/>\n'
            '\t\t<path d="M77.7383308,20 L61.1640113,20 '
            'L44.7300055,63.2000173 '
            'L56.0543288,63.2000173 L40,99.623291 L72.7458388,54.5871812 '
            'L60.907727,54.5871812 L77.7383308,20 Z" id="Path-1" '
            'fill="#FFFFFF"/>\n'
            '\t</g>\n'
            '</svg>\n',
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + ".svg")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewDesignCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "",
            "design",
            '<design:component>\n'
            '</design:component>',
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + ".design")
        isvalidbundle = helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewRendererCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "Renderer",
            "js",
            "({\n"
            "\trender: function(component, helper) {\n"
            "\t\treturn this.superRender();\n"
            "\t}\n"
            "})",
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Renderer.js")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewHelperCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "Helper",
            "js",
            "({\n"
            "\thelperMethod: function() {\n"
            "\n\t}\n"
            "})",
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False

        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Helper.js")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewDocumentationCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "Documentation",
            "auradoc",
            '<aura:documentation>\n'
            '\t<aura:description>Documentation</aura:description>\n'
            '\t<aura:example name="ExampleName" '
            'ref="exampleComponentName" label="Label">\n'
            '\t\tExample Description\n'
            '\t</aura:example>\n'
            '</aura:documentation>',
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        print("looking for " + os.path.basename(dirs[0]) +
              "Documentation.auradoc")
        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Documentation.auradoc")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewStyleCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "Style",
            "css",
            '.THIS.container {'
            '\twidth: 100%;\n'
            '\tpadding: 10px 0px;\n'
            '\tmargin: 0px;\n'
            '}\n\n'
            '.THIS .center {\n'
            '\tmargin: 0px auto;\n'
            '}\n\n'
            '.THIS .content {\n'
            '\tmax-width: 768px;\n'
            '\tfont-size: 12px;\n'
            '\tcolor: #3c3d3e;\n'
            '}',
            self.dirs)

    def is_visible(self, dirs):
        """Sample doc string."""
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False

        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Style.css")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningDeleteCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, files):
        """Sample doc string."""
        for f in files:
            command = "delete -p=" + f
            self.window.run_command(
                'exec',
                {'cmd': ["force", "aura", command]})
            self.window.find_open_file(f).close()

        return

    def is_visible(self, files):
        """Sample doc string."""
        for f in files:
            p = os.path.dirname(f)
            if os.path.basename(p) == "aura":
                return True
            else:
                p = os.path.dirname(p)
                if os.path.basename(p) == "aura":
                    return True
                else:
                    return False
        return False


class LightningDeleteBundleCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        # comment
        for d in dirs:
            command = 'delete -p=' + d
            self.window.run_command(
                'exec',
                {'cmd': ["force", "aura", command]})
            for root, dirs, files in os.walk(d):
                for name in files:
                    v = self.window.find_open_file(os.path.join(root, name))
                    if not (v is None):
                        v.close()

        return

    def is_visible(self, dirs):
        """Sample doc string."""
        for d in dirs:
            p = os.path.dirname(d)
            if os.path.basename(p) == "aura":
                return 1 == 1
            else:
                p = os.path.dirname(p)
                if os.path.basename(p) == "aura":
                    return 1 == 1
                else:
                    return 1 == 2
        return False


class LightningSave(sublime_plugin.EventListener):
    """Sample doc string."""

    def on_post_save(self, view):
        """Sample doc string."""
        self.view = view
        filename = view.file_name()
        print("Check to see if this an aura thingy.")
        if Helper.parent_dir_is_aura(self, os.path.dirname(filename)):
            print("Check to see if the file ends in .JS. " + filename)
            _, ext = os.path.splitext(filename)
            if ext == ".js":
                view.run_command('lightning_lint')
            command = "push -f='" + filename + "'"
            view.window().run_command(
                'exec',
                {'cmd': ["force", "aura", "push", "-f",
                         '\'' + filename + '\'']})
        elif Helper.is_metadata(self, os.path.dirname(filename)):
            if Helper.is_static_resource(self, filename):
                print("is static resource")
            else:
                view.window().run_command(
                    'exec',
                    {
                        'working_dir':
                            os.path.dirname(
                                os.path.dirname(
                                    os.path.dirname(filename))),
                        'cmd': ["force", "push", "-f", filename]
                    })
        elif Helper.is_static_resource(self, os.path.dirname(filename)):
            resource_name = Helper.get_resource_name(self, filename)
            command = '-t=StaticResource'
            command2 = '-n="' + resource_name + '"'
            view.window().run_command(
                'exec',
                {'cmd': ["force", "push", command, command2]})

        return

    def on_selection_modified(self, view):
        """Selection was modified: update status bar."""
        auralint.update_statusbar(view)


class LightningSaveBundleCommand(sublime_plugin.WindowCommand):
    """Sample doc string."""

    def run(self, dirs):
        """Sample doc string."""
        print(dirs)
        command = 'push -f="' + dirs[0] + '"'
        self.window.run_command(
            'exec',
            {'cmd': ["force", "aura", command]})
        return

    def is_visible(self, dirs):
        """Sample doc string."""
        for d in dirs:
            p = os.path.dirname(d)
            if os.path.basename(p) == "aura":
                return 1 == 1
            else:
                p = os.path.dirname(p)
                if os.path.basename(p) == "aura":
                    return 1 == 1
                else:
                    return 1 == 2
        return False
