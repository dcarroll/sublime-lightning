import sublime
import sublime_plugin
import os
import subprocess
import json
from . import semver


def plugin_loaded():
    print("WE ARE TOTALLY LOADED!")
    try:
        p = subprocess.Popen(["force", "version"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
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
        sublime.error_message("Sublime Lightning Plugin requires the " +
                              "Force.com CLI to functionn\n\nPlease " +
                              "visit force-cli.herokuapp.com to install" +
                              "the Force.com CLI.\n\nIf you have already" +
                              " installed it, please make sure that you " +
                              "have stored it or created a symlink to " +
                              "it in Sublime's default path.")
    return


class Helper(sublime_plugin.WindowCommand):
    def foo(self):
        return

    def install_cli(self):
        return

    def bundle_op_is_visible(self, dirs):
        if len(dirs) == 0:
            return False
        else:
            return self.dir_is_aura(dirs[0])

    def file_op_is_visible(self, dirs):
        return self.parent_dir_is_aura(dirs[0])

    def dir_is_aura(self, working_dir):
        return os.path.basename(working_dir) == "aura"

    def parent_dir_is_aura(self, working_dir):
        return os.path.basename(os.path.dirname(working_dir)) == "aura"

    def is_metadata(self, working_dir):
        return os.path.basename(os.path.dirname(working_dir)) == "metadata"

    def is_static_resource(self, file):
        for root, dirs, files in Helper.walk_up(self, file):
            if "staticresources" in dirs:
                return True

        return False

    def get_resource_name(self, file):
        for root, dirs, files in Helper.walk_up(self, os.path.dirname(file)):
            if os.path.basename(os.path.dirname(root)) == "staticresources":
                return os.path.basename(root)

    def is_bundle_type(self, working_dir, comp_type):
        files = os.listdir(working_dir[0])
        for filename in files:
            fname, fext = os.path.splitext(filename)
            if (fext == "." + comp_type):
                return True
        return False

    def has_this_file(self, working_dir, filename):
        return os.path.exists(os.path.join(working_dir, filename))

    def do_login(self, username, password, instance):
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
        return

    def do_fetch(self, bundle, adir):
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
        p = subprocess.Popen(['force', 'active', '-j'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out = p.communicate()[0]
        data = json.loads(out.decode("utf-8"))
        return data["instanceUrl"]

    def get_namespace(self):
        p = subprocess.Popen(['force', 'active', '-j'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out = p.communicate()[0]
        data = json.loads(out.decode("utf-8"))
        return data["namespace"]

    def get_app_name(self, adir):
        os.chdir(adir)
        return os.path.basename(adir)

    def open_selected_bundle(self, index):
        if (index == -1):
            return

        if (index == 0):
            self.do_fetch("all", self.window.folders()[0])
        else:
            self.do_fetch(self.messages[index][2], self.window.folders()[0])
        return

    def open_selected_metadata(self, index):
        if (index == -1):
            return

        self.show_metadata_instance_list(self.messages[index][0])
        return

    def fetch_selected_metadata(self, index):
        item = self.messages[index][0]
        print("Type: " + self.type)
        print("Item: " + item)
        self.window.run_command(
            'exec',
            {'cmd': ["force", "fetch", "-t", self.type, "-n", item, "-unpack"],
             'working_dir': self.window.folders()[0]})
        return

    def meets_forcecli_version(self, minversion):
        version = Helper.get_forcecli_version()
        version = version[1:]
        return semver.match(version, ">=" + minversion)

    def get_forcecli_version(self):
        try:
            p = subprocess.Popen(["force", "version"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
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
            sublime.error_message("Sublime Lightning Plugin requires the " +
                                  "Force.com CLI to functionn\n\nPlease " +
                                  "visit force-cli.herokuapp.com to install" +
                                  "the Force.com CLI.\n\nIf you have already" +
                                  " installed it, please make sure that you " +
                                  "have stored it or created a symlink to " +
                                  "it in Sublime's default path.")
        return ver.replace("\n", "")

    def show_metadata_instance_list(self, metaname):
        self.type = metaname
        self.messages = []
        p = subprocess.Popen(["force", "describe", "-t", "metadata",
                              "-n", metaname, "-j"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result, err = p.communicate()
        if err:
            sublime.error_message(err.decode("utf-8"))
        else:
            try:
                m = json.loads(result.decode("utf-8"))
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
        self.window.run_command(
            'exec',
            {'cmd': ["open", url]}
        )

    def show_metadata_type_list(self):
        self.messages = []
        p = subprocess.Popen(["force", "describe", "-t", "metadata",
                              "-j"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
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

    def show_package_list(self):
        self.messages = []
        p = subprocess.Popen(["force", "describe", "-t", "metadata",
                              "-j"], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
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

    def show_bundle_list(self):
        self.messages = []
        if Helper.meets_forcecli_version("0.22.36"):
            p = subprocess.Popen(["force", "query", "Select Id,DeveloperName, "
                                  "MasterLabel, Description From "
                                  "AuraDefinitionBundle",
                                  "--format:json", "-t"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        else:
            p = subprocess.Popen(["force", "query", "Select Id,DeveloperName, "
                                  "MasterLabel, Description From "
                                  "AuraDefinitionBundle",
                                  "--format:json", "-t"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        result, err = p.communicate()
        if err:
            sublime.error_message(err.decode("utf-8"))
        else:
            try:
                m = json.loads(result.decode("utf-8"))
                self.messages.append(["All Bundles", "*", "Every Bundle",
                                      "All the lightning bundles "
                                      "in your org!"])
                for mm in m:
                    x = [mm['MasterLabel'], mm['Id'], mm["DeveloperName"],
                         mm["Description"]]
                    self.messages.append(x)

                self.window = sublime.active_window()
                self.window.show_quick_panel(self.messages,
                                             self.open_selected_bundle,
                                             sublime.MONOSPACE_FONT)
            except:
                print("error: occurred")
                return

    def make_bundle_file(self, file_name, extension, snippet, dirs):
        working_dir = dirs[0]
        os.chdir(working_dir)
        e = extension
        if e == "cmp" or e == "app" or e == "intf" or e == "evt":
            fn, ex = os.path.splitext(file_name)
            os.mkdir(os.path.join(working_dir, file_name))
            os.chdir(fn)
            working_dir = os.getcwd()

        app = open(file_name + "." + extension, "wb")
        if int(sublime.version()) >= 3000:
            app.write(bytes(snippet, 'UTF-8'))
        else:  # To support Sublime Text 2
            app.write(bytes(snippet))

        app.close()
        filename = os.path.join(working_dir, file_name + "." + extension)
        self.window.open_file(filename)
        cmd = 'push -f=' + filename
        self.window.run_command(
            'exec',
            {'cmd': ["force", "aura", cmd]})

        return app

    def walk_up(self, bottom):
        """
        mimic os.walk, but walk 'up'
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
    def run(self):
        version = Helper(self.window).get_forcecli_version()
        print("Running version " + version + " of Force CLI!")
        self.window.show_input_panel(
            "Username: ",
            "",
            self.get_password,
            None,
            None)
        pass

    def get_password(self, username):
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
        Helper(self.window).do_login(self.username, self.password, instance)
        return

    def is_visible(self):
        return True


class FetchMetaCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("Running FetchMetaCommand")
        Helper(self.window).show_metadata_type_list()

    def is_visible(self):
        return True


class FetchPackageCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("Running FetchPackageCommand")
        Helper(self.window).show_package_list()

    def is_visible(self):
        return True


class FetchCommand(sublime_plugin.WindowCommand):
    def run(self):
        print("Running FetchLightningCommand")
        Helper(self.window).show_bundle_list()

    # def do_fetch(self, bundle):
    #    self.dirs = self.window.folders()
    #    Helper(self.window).show_bundle_list()
    #    return

    def is_visible(self):
        return True


class LightningNewAppCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        self.window.show_input_panel("App Name:", "", self.on_done, None, None)
        pass

    def on_done(self, file_name):
        Helper(self.window).make_bundle_file(
            file_name,
            "app",
            "<aura:application>\n\n</aura:application>",
            self.dirs)
        return

    def is_visible(self, dirs):
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewComponentCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        self.window.show_input_panel(
            "Component Name:",
            "",
            self.on_done,
            None,
            None)
        pass

    def on_done(self, file_name):
        Helper(self.window).make_bundle_file(
            file_name,
            "cmp",
            "<aura:component>\n\n</aura:component>",
            self.dirs)
        return

    def is_visible(self, dirs):
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewEventCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        self.window.show_input_panel(
            "Event Name:",
            "",
            self.on_done,
            None,
            None)
        pass

    def on_done(self, file_name):
        Helper(self.window).make_bundle_file(
            file_name,
            "evt",
            '<aura:event type="APPLICATION">\n\n</aura:event>',
            self.dirs)
        return

    def is_visible(self, dirs):
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningNewInterfaceCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        self.window.show_input_panel(
            "Interface Name:",
            "",
            self.on_done,
            None,
            None)
        pass

    def on_done(self, file_name):
        Helper(self.window).make_bundle_file(
            file_name,
            "intf",
            '<aura:interface description="Interface template">'
            '\n\t<aura:attribute name="example" type="String" default="" '
            'description="An example attribute."/>'
            '\n</aura:interface>',
            self.dirs)
        return

    def is_visible(self, dirs):
        return Helper(self.window).bundle_op_is_visible(dirs)


class LightningPreviewCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
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
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False
        isvalidbundle = helper.is_bundle_type(dirs, "app")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle


class LightningNewControllerCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Controller"
        Helper(self.window).make_bundle_file(
            name,
            "js",
            "({\n"
            "\tmyAction: function(component, event, helper) {\n"
            "\t}\n"
            "})",
            self.dirs)

    def is_visible(self, dirs):
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
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
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
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0])
        Helper(self.window).make_bundle_file(
            name,
            "design",
            '<design:component>\n'
            '</design:component>',
            self.dirs)

    def is_visible(self, dirs):
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
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Renderer"
        Helper(self.window).make_bundle_file(
            name,
            "js",
            "({\n"
            "\trender: function(component, helper) {\n"
            "\t\treturn this.superRender();\n"
            "\t}\n"
            "})",
            self.dirs)

    def is_visible(self, dirs):
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
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Helper"
        Helper(self.window).make_bundle_file(
            name,
            "js",
            "({\n"
            "\thelperMethod: function() {\n"
            "\n\t}\n"
            "})",
            self.dirs)

    def is_visible(self, dirs):
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
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Documentation"
        Helper(self.window).make_bundle_file(
            name,
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
        helper = Helper(self.window)
        if len(dirs) == 0:
            return False

        hasfile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Documentation.js")
        isvalidbundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isvalidbundle and not hasfile


class LightningNewStyleCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Style"
        Helper(self.window).make_bundle_file(
            name,
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
    def run(self, files):
        for f in files:
            command = "delete -p=" + f
            self.window.run_command(
                'exec',
                {'cmd': ["force", "aura", command]})
            self.window.find_open_file(f).close()

        return

    def is_visible(self, files):
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
    def run(self, dirs):
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

    def on_post_save(self, view):
        filename = view.file_name()
        if Helper.parent_dir_is_aura(self, os.path.dirname(filename)):
            command = 'push -f=' + filename
            view.window().run_command(
                'exec',
                {'cmd': ["force", "aura", command]})
        elif Helper.is_metadata(self, os.path.dirname(filename)):
            if Helper.is_static_resource(self, filename):
                print("is static resource")
            else:
                command = '-f=' + filename
                view.window().run_command(
                    'exec',
                    {'cmd': ["force", "push", command]})
        elif Helper.is_static_resource(self, os.path.dirname(filename)):
            resource_name = Helper.get_resource_name(self, filename)
            command = '-t=StaticResource'
            command2 = '-n=' + resource_name
            view.window().run_command(
                'exec',
                {'cmd': ["force", "push", command, command2]})

        return


class LightningSaveBundleCommand(sublime_plugin.WindowCommand):

    def run(self, dirs):
        print(dirs)
        command = 'push -f=' + dirs[0]
        self.window.run_command(
            'exec',
            {'cmd': ["force", "aura", command]})
        return

    def is_visible(self, dirs):
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
