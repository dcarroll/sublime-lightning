import sublime
import sublime_plugin
import os


class Helper(sublime_plugin.WindowCommand):
    def foo(self):
        return

    def bundle_op_is_visible(self, dirs):
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

    def make_bundle_file(self, file_name, extension, snippet, dirs):
        #print(file_name)
        #print(extension)
        working_dir = dirs[0]
        #print(working_dir)
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
        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Helper.js")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


class LightningNewModelCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.dirs = dirs
        name = os.path.basename(dirs[0]) + "Model"
        Helper(self.window).make_bundle_file(
            name,
            "js",
            '{\n'
            '\t"example": "example value"\n'
            "}",
            self.dirs)

    def is_visible(self, dirs):
        helper = Helper(self.window)
        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Model.js")
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
        hasFile = helper.has_this_file(
            dirs[0],
            os.path.basename(dirs[0]) + "Style.css")
        isValidBundle = helper.is_bundle_type(dirs, "app") or \
            helper.is_bundle_type(dirs, "cmp")

        return Helper(self.window).file_op_is_visible(dirs) and \
            isValidBundle and not hasFile


class LightningDeleteCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        #print(files)
        for f in files:
            #print(f)
            command = "delete -f=" + f
            #subprocess.call(["force", "aura", "-f", f])
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


class LightningDeleteBundleCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        for d in dirs:
            command = 'delete -f=' + d
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


class LightningSave(sublime_plugin.EventListener):

    def on_post_save(self, view):
        filename = view.file_name()
        if os.path.basename(
            os.path.dirname(
                os.path.dirname(filename))) == "aura":
            command = '-f=' + filename
            view.window().run_command(
                'exec',
                {'cmd': ["force", "pushAura", command]})
        return
