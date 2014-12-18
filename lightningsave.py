import sublime
import sublime_plugin
import os
import subprocess
import json


class Helper(sublime_plugin.WindowCommand):
    def foo(self):
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

    def is_bundle_type(self, working_dir, comp_type):
        files = os.listdir(working_dir[0])
        for filename in files:
            fname, fext = os.path.splitext(filename)
            if (fext == "." + comp_type):
                return True
        return False

    def has_this_file(self, working_dir, filename):
        return os.path.exists(os.path.join(working_dir, filename))

    def do_login(self, username, password):
        self.window.run_command(
            'exec',
            {'cmd': ["force", "login", "-u", username, "-p", password]})
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

    def open_selected_bundle(self, index):
        if (index == 0):
            self.do_fetch("all", self.window.folders()[0])
        else:
            self.do_fetch(self.messages[index][2], self.window.folders()[0])
        return

    def show_bundle_list(self):
        self.messages = []
        p = subprocess.Popen(["force", "query", "Select Id, DeveloperName, "
                              "MasterLabel, Description From "
                              "AuraDefinitionBundle",
                              "--format:json"], stdout=subprocess.PIPE)
        result = p.communicate()[0]
        try:
            m = json.loads(result.decode("utf-8)"))
            self.messages.append(["All Bundles", "*", "Every Bundle",
                                  "All the lightning bundles in your org!"])
            for mm in m:
                x = [mm['MasterLabel'], mm['Id'], mm["DeveloperName"],
                     mm["Description"]]
                self.messages.append(x)

            self.window = sublime.active_window()
            self.window.show_quick_panel(self.messages,
                                         self.open_selected_bundle,
                                         sublime.MONOSPACE_FONT)
        except:
            return

    def make_bundle_file(self, file_name, extension, snippet, dirs):
        working_dir = dirs[0]
        os.chdir(working_dir)
        if extension == "cmp" or extension == "app" or extension == "evt":
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
        cmd = '-f=' + filename
        self.window.run_command(
            'exec',
            {'cmd': ["force", "pushAura", cmd]})

        return app


class LoginCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            "Username: ",
            "",
            self.get_password,
            None,
            None)
        pass

    def get_password(self, username):
        self.username = username
        self.window.show_input_panel(
            "Password: ",
            "",
            self.do_login,
            None,
            None)
        pass

    def do_login(self, password):
        Helper(self.window).do_login(self.username, password)
        return

    def is_visible(self):
        return True


class FetchCommand(sublime_plugin.WindowCommand):
    def run(self):
        #self.window.show_input_panel(
        #    "Bundle name: ",
        #    "all",
        #    self.do_fetch,
        #    None,
        #    None)
        #pass
        Helper(self.window).show_bundle_list()

    def do_fetch(self, bundle):
        self.dirs = self.window.folders()
        Helper(self.window).show_bundle_list()
        return

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
        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Controller.js")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


class LightningNewSVGCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        #name = os.path.basename(dirs[0]) + ".svg"
        #Helper(self.window).make_bundle_file(
        #    name,
        #    "SVG Name:",
        #    '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
        #    '<svg width="120px" height="120px" viewBox="0 0 120 120" '
        #    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
        #    'xmlns:xlink="http://www.w3.org/1999/xlink">'
        #    '<g stroke="none" stroke-width="1" fill="none" '
        #    'fill-rule="evenodd">'
        #    '<path d="M120,108 C120,114.6 114.6,120 108,120 L12,120 C5.4,120 '
        #    '0,114.6 0,108 L0,12 C0,5.4 5.4,0 12,0 L108,0 C114.6,0 120,5.4 '
        #    '120,12 L120,108 L120,108 Z" id="Shape" fill="#2A739E"/>'
        #    '<path d="M77.7383308,20 L61.1640113,20 L44.7300055,63.2000173 '
        #    'L56.0543288,63.2000173 L40,99.623291 L72.7458388,54.5871812 '
        #    'L60.907727,54.5871812 L77.7383308,20 Z" id="Path-1" '
        #    'fill="#FFFFFF"/>'
        #    '</g>'
        #    '</svg>',
        #    self.dirs)

    def is_visible(self):
        print("Checking visibility...")
        return False
    #   helper = Helper(self.window)
    #    if len(dirs) == 0:
    #        return False
    #    hasFile = helper.has_this_file(
    #        dirs[0],
    #        os.path.basename(dirs[0]) + ".svg")
    #    isValidBundle = helper.is_bundle_type(dirs, "app") or \
    #        helper.is_bundle_type(dirs, "cmp")

    #    return Helper(self.window).file_op_is_visible(dirs) and \
    #        isValidBundle and not hasFile


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
        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Renderer.js")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


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

        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Helper.js")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


class LightningNewDocumentationCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Documentation"
        Helper(self.window).make_bundle_file(
            name,
            "js",
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

        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Documentation.js")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


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

        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Style.css")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


class LightningDeleteCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        for f in files:
            command = "delete -p=" + f
            self.window.run_command(
                'exec',
                {'cmd': ["force", "aura", command]})

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
        for d in dirs:
            command = 'delete -p=' + d
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


class LightningSave(sublime_plugin.EventListener):

    def on_post_save(self, view):
        filename = view.file_name()
        if Helper.parent_dir_is_aura(os.path.dirname(filename)):
            command = '-f=' + filename
            view.window().run_command(
                'exec',
                {'cmd': ["force", "pushAura", command]})

#        if os.path.basename(
#            os.path.dirname(
#                os.path.dirname(filename))) == "aura":
#            command = '-f=' + filename
#            view.window().run_command(
#                'exec',
#                {'cmd': ["force", "pushAura", command]})
        return
