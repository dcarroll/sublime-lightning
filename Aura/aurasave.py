import sublime, sublime_plugin, os, subprocess
 
class AuraSave(sublime_plugin.EventListener):
 
  def on_post_save(self, view):
    print 'BuildonSave: on_post_save'

    #let's see if project wants to be autobuilt.
    should_build = view.settings().get('build_on_save')
    filename = view.file_name()
    if os.path.basename(os.path.dirname(os.path.dirname(filename))) == "aurabundles":
      print os.path.dirname(filename)

      command = '-f=' + filename
      view.window().run_command('exec',{ 'cmd':["force", "pushAura", command] })
      print 'Command should have executed'
    else:
      print 'BuildonSave: Project not configured for build_on_save.  Try setting build_on_save in project settings'