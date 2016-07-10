# -*- coding: utf-8 -*-
"""
AuraLint: Sublime Text 2 plugin.

Check Lightning JS files with
"""
import json
import os
import shlex
import subprocess

import sublime
import sublime_plugin


settings = sublime.load_settings("Lightning.sublime-settings")
FLAKE_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORS_IN_VIEWS = {}
IS_WINDOWS = os.name == 'nt'

def update_statusbar(view):
    """Update status bar with error."""
    # get view errors (exit if no errors found)
    view_errors = ERRORS_IN_VIEWS.get(view.id())
    if view_errors is None:
        return

    # get view selection (exit if no selection)
    view_selection = view.sel()
    if not view_selection:
        return

    # get current line (line under cursor)
    current_line = view.rowcol(view_selection[0].end())[0]

    if current_line in view_errors:
        # there is an error on current line
        errors = view_errors[current_line]
        view.set_status('lightning-tip',
                        'Lightning lint errors: %s' % ' / '.join(errors))
    else:
        # no errors - clear statusbar
        view.erase_status('flake8-tip')


class LightningLintCommand(sublime_plugin.TextCommand):
    """Do flake8 lint on current file."""

    def run(self, edit):
        """Leave me alone."""
        filename = os.path.abspath(self.view.file_name())

        # check if active view contains file
        if not filename:
            return

        # we need to always clear regions. three situations here:
        # - we need to clear regions with fixed previous errors
        # - is user will turn off 'highlight' in settings and then run lint
        # - user adds file with errors to 'ignore_files' list
        self.view.erase_regions('lightning-errors')

        # we need to always erase status too. same situations.
        self.view.erase_status('lightning-tip')

        folders = self.view.window().folders()
        print("Folders are " + folders[0])
        quote = lambda x: shlex.quote(x) if IS_WINDOWS else x
        p = subprocess.Popen(["heroku", "lightning:lint",
                             quote(folders[0]), "--files", quote(filename), "--json"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=IS_WINDOWS)
        print("Calling for results.")
        results, err = p.communicate()
        if err:
            print("Error on lint...")
            # sublime.error_message(err.decode("utf-8"))
        else:
            print("No error on lint...")
            r = str(results.decode("utf-8"))
            r = r.replace("\\\"", "'")
            m = json.loads(r)
            self.errors_list = []
            for mm in m:
                data = mm['result']
                for res in data:
                    x = [mm['file'], res['ruleId'] + " " +
                         res['message'],
                         res['source'].strip(),
                         str(res['line']), str(res['column'])]
                    self.errors_list.append(x)

            # show errors
            if self.errors_list:
                self.show_errors()

    def show_errors(self):
        """Show all errors."""
        errors_to_show = []

        # get select and ignore settings
        # select = settings.get('select') or []
        # ignore = settings.get('ignore') or []
        is_highlight = True
        is_popup = True
        # is_highlight = settings.get('highlight', False)
        # is_popup = settings.get('popup', True)

        regions = []
        view_errors = {}
        errors_list_filtered = []

        for e in self.errors_list:
            print(e)
            current_line = int(e[3]) - 1
            error_text = e[1]

            # get error line
            text_point = self.view.text_point(current_line, 0)
            line = self.view.full_line(text_point)
            full_line_text = self.view.substr(line)
            line_text = full_line_text.strip()

            # build error text
            error = [error_text, u'{0}:{1} {2}'.format(current_line + 1,
                                                       e[4],
                                                       line_text)]
            errors_to_show.append(error)

            # build line error message
            if is_popup:
                errors_list_filtered.append(e)

            # prepare errors regions
            if is_highlight:
                # prepare line
                line_text = full_line_text.rstrip('\r\n')
                line_length = len(line_text)

                # calculate error highlight start and end positions
                start = text_point + line_length - len(line_text.lstrip())
                end = text_point + line_length

                regions.append(sublime.Region(start, end))

            # save errors for each line in view to special dict
            view_errors.setdefault(current_line, []).append(error_text)

        # renew errors list with selected and ignored errors
        self.errors_list = errors_list_filtered
        # save errors dict
        ERRORS_IN_VIEWS[self.view.id()] = view_errors

        # highlight error regions if defined
        if is_highlight:
            self.view.add_regions('lightning-errors', regions,
                                  'invalid.deprecated', '',
                                  sublime.DRAW_OUTLINED)

        if is_popup:
            # view errors window
            self.view.window().show_quick_panel(errors_to_show,
                                                self.error_selected)

    def error_selected(self, item_selected):
        """Error was selected - go to error."""
        if item_selected == -1:
            return

        # reset selection
        selection = self.view.sel()
        selection.clear()

        # get error region
        error = self.errors_list[item_selected]
        region_begin = self.view.text_point(int(error[3]) - 1,
                                            int(error[4]) - 1)

        # go to error
        selection.add(sublime.Region(region_begin, region_begin))
        self.view.show_at_center(region_begin)
        update_statusbar(self.view)


class LightningLintBackground(sublime_plugin.EventListener):
    """Listen to Siblime Text 2 events."""

    def on_post_save(self, view):
        """Do lint on file save if not denied in settings."""
        if settings.get('lint_on_save', True):
            view.run_command('flake8_lint')

    def on_selection_modified(self, view):
        """Selection was modified: update status bar."""
        update_statusbar(view)
