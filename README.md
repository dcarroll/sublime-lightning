sublime-lightning
============

Sublime Plugin for Lightning Component Development

This plugin requires Sublime Text 3 and works in conjunction with the Force CLI. You can download the version for your OS here: https://force-cli.herokuapp.com

Make sure that you have installed the Force CLI into a folder on your path and that is marked as executable.

To install the plugin, you will need to install Package Control.  Installation instructions are here: https://sublime.wbond.net/installation

Once you have both of these installed, create a new folder to be your working folder.

`mkdir mywork`

`cd mywork`

Launch Sublime Text and open the new folder.  If you have not logged in recently from the command line, you can right-click the folder in Sublime's sidebar and click "Salesforce Login". In the bottom tray of Sublime enter your username and hit the enter key, enter your password (the password will be shown in clear text, sorry) and hit the enter key.

At this point, you will not be able to create any Lightning artifacts, unless you have a folder under your work directory named 'metadata/aura'.  You can, however, fetch existing Lightning artifacts by right clicking the work folder and selecting "Fetch Lightning".  This will query your Salesforce instance for all Lightning bundles and display them for you to choose which thing you want to edit.  You can open all lightning bundles at once, scroll to the one you want, or begin typing the name of the Lightning bundle to filter the list and then select the one you want.

Once you have a Lightning bundle locally in sublime, you can begin editing your component, controller, event, app, css.  To save your changes back to Salesforce, simply press cmd+s on your Mac or ctrl+s on your Windows machine.  You will see a verification of the save and the time it took in the status bar at the bottom of the screen.  You will also see any errors that might have prevented pushing component artifact there as well.

To create a new Lightning bundle, right-click the "aura" folder and select the type of component that you want to create. You are prompted for a name at the bottom of the screen. Enter a name and hit enter. Once your bundle is created, you can right click the bundle folder and add other artifacts to your bundle as appropriate for the type of bundle that you created.

Deleting artifacts is accomplished by right-clicking the file and selecting "Delete Lightning Definition". This will only delete the selected file and remove that artifact from the bundle both locally and on Salesforce.  If you want to delete the entire bundle, right-click the bundle folder and select "Delete Lightning Bundle".  Deletes CANNOT be undone and there is no confirmation prompt in the current version of the plugin.  

You can safely right click any file or folder and select the Sublime menu item for deleting file or folder, as what is saved locally is a copy of what is in Salesforce.  You can easily retrieve the Lightning bundle or artifact by re-fetching, right-click and select "Fetch Lightning".

![screenshot-235](https://cloud.githubusercontent.com/assets/116254/5481950/b2d08212-860d-11e4-9e2c-7f294c7b3215.png)

![screenshot-236](https://cloud.githubusercontent.com/assets/116254/5481951/b730bc1e-860d-11e4-8b8c-7eea2c0303df.png)

![screenshot-237](https://cloud.githubusercontent.com/assets/116254/5481952/b8ea6fa0-860d-11e4-8ce8-11b26c5a1aa1.png)

![screenshot-238](https://cloud.githubusercontent.com/assets/116254/5481953/ba3ae5ce-860d-11e4-8e9e-97d505963f54.png)

See "how to" video below.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=A_sUTfeGKxw
" target="_blank"><img src="http://img.youtube.com/vi/A_sUTfeGKxw/0.jpg"
alt="http://img.youtube.com/vi/A_sUTfeGKxw/0.jpg" width="240" height="180" border="10" /></a>
