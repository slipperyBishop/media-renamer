#!/bin/python
import os, re, sys, gi, renameMedia
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GridWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Media Renamer")
        self.set_size_request(400, 100)
       
        #setup box first parameter in Gtk.box() is 1 for vertical layout
        self.vbox = Gtk.Box(orientation = 1, spacing = 20)
        self.vbox.set_halign(Gtk.Align.CENTER)
        self.add(self.vbox)
        
        #initialse labels
        self.labelDescription = Gtk.Label()
        self.labelDescription.set_text("Selected Directory: ")
        self.selectedDirectoryLabel = Gtk.Label() 
        self.selectedDirectoryLabel.set_max_width_chars(50)
        self.selectedDirectoryLabel.set_width_chars(50)
        self.selectedDirectoryLabel.set_line_wrap(True)

        labelBox = Gtk.Box(orientation = 0, spacing = 20)
        labelBox.pack_start(self.labelDescription, False, False, 0)
        labelBox.pack_start(self.selectedDirectoryLabel, False, False, 0)
        labelBox.set_margin_top(20)
        labelBox.set_margin_left(20)
        labelBox.set_margin_right(20)

        #initialize buttons
        self.selectDirectory = Gtk.Button(label="Choose Directory")
        self.selectDirectory.connect("clicked", self.getDirectory)  
        self.continueButton = Gtk.Button(label="Continue") 
        self.continueButton.connect("clicked", self.openReviewResultsWindow)
        
        self.vbox.pack_start(labelBox, False, False, 0)
        
        hbox1 = Gtk.Box(orientation = 0, spacing = 20)
        hbox1.pack_start(self.selectDirectory, False, True, 0)
        hbox1.pack_start(self.continueButton, False, True, 0)
        hbox1.set_halign(Gtk.Align.CENTER)
        hbox1.set_margin_bottom(20)

        self.vbox.pack_start(hbox1, False, True, 0)

        self.directory = None 

    def getDirectory(self, params):
        
        #this was taken from https://python-gtk-3-tutorial.readthedocs.io/en/latest/dialogs.html#filechooserdialog
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,\
            Gtk.FileChooserAction.SELECT_FOLDER,\
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,\
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.directory = dialog.get_filename()
            self.selectedDirectoryLabel.set_text(self.directory)

        dialog.destroy() 

    def openReviewResultsWindow(self, params):

        processedMedia = renameMedia.process_directories(self.directory)       
        self.resultsWin = ReviewResultsWindow(processedMedia, self.directory)
        self.resultsWin.show_all()
    
class ReviewResultsWindow(Gtk.Window):
    
    def __init__(self, processedMedia, directory):

        Gtk.Window.__init__(self, title="Review Results")
        self.set_size_request(1100, 1000)

        self.directory = directory
        self.processedMedia = processedMedia

        self.newNamesEntries = []
        self.outerBox = Gtk.Box(orientation=1, spacing = 20) 
        self.outerBox.set_margin_bottom(20)
        self.outerBox.set_margin_top(20)
        self.add(self.outerBox)
        
        # create boxes to hold the labels and text input fields for
        # the original and new movie names respectively
        self.mediaBox = Gtk.Box(orientation=1, spacing = 20)
        self.mediaBox.set_halign(Gtk.Align.CENTER)
        
        originalNamesLabel = Gtk.Label()
        originalNamesLabel.set_text("Original Name")
        originalNamesLabel.set_size_request(500, 20)
        newNamesLabel = Gtk.Label()
        newNamesLabel.set_text("New Name")
        newNamesLabel.set_size_request(500, 20)

        box = Gtk.Box(orientation = 0, spacing = 20)
        box.pack_start(originalNamesLabel, False, False, 0)
        box.pack_start(newNamesLabel, False, False, 0)
        self.mediaBox.pack_start(box, False, False, 0)
        
        # create a scrolledWindow to add scrollablitiy to the mediaBox
        self.scrolledWindow = Gtk.ScrolledWindow()
        self.viewport = Gtk.Viewport()
        self.viewport.add(self.mediaBox)
        self.scrolledWindow.add(self.viewport)

        # create the update and abort buttons as well as a box to hold them
        self.buttonsBox = Gtk.Box(orientation = 0, spacing = 20)
        self.buttonsBox.set_halign(Gtk.Align.CENTER)
        self.abortButton = Gtk.Button(label="Cancel")
        self.abortButton.connect("clicked", self.closeWindow)
        self.updateNamesButton = Gtk.Button(label="Update Names")
        self.updateNamesButton.connect("clicked", self.updateMedia)
        
        # add buttons into button box
        self.buttonsBox.pack_start(self.abortButton, False, True, 0)
        self.buttonsBox.pack_start(self.updateNamesButton, False, True, 0)
        self.updateNamesButton.set_size_request(-1, 30)
        self.abortButton.set_size_request(-1, 30)

        #add mediaBox and buttonBox into the outerbox
        self.outerBox.pack_start(self.scrolledWindow, True, True, 0)
        self.outerBox.pack_start(self.buttonsBox, False, True, 0)

        for original, new in processedMedia:
           
            textview = Gtk.TextView()
            textview.set_wrap_mode(Gtk.WrapMode.CHAR)
            textBuffer = textview.get_buffer()
            textview.set_size_request(500, 50)

            if new == "":
                textBuffer.set_text(original)
            else:
                textBuffer.set_text(new)
            
            label = Gtk.Label()
            label.set_text(original)
            label.set_line_wrap(True)
            label.set_max_width_chars(50)
            label.set_width_chars(50)
            label.set_selectable(True)
 
            self.labelBox = Gtk.Box(orientation = 0, spacing = 0)
            self.labelBox.set_size_request(500, 50)
            self.labelBox.pack_start(label, False, False, 0)

            self.box = Gtk.Box(orientation = 0, spacing = 20)
            self.box.pack_start(self.labelBox, False, False, 0)
            self.box.pack_start(textview, False, False, 0)
            #self.box.set_size_request(1000, 50)

            self.mediaBox.pack_start(self.box, False, False, 0)
            
            self.newNamesEntries.append(textview)                
    
    def updateMedia(self, processedMedia):
        
        # promt user with a dialog that makes certain they understand that files and directories
        # will be updated
        dialog = DialogBox(self, "Proceeding will overwrite the names of the files and directories on the filesystem, are you sure you want to continue?", "Are you sure?")
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.CANCEL:
            return
        
        #get updated names from the textbox's
        index = 0
        while(index < len(self.processedMedia)):
            
            textbuffer = self.newNamesEntries[index].get_buffer()
            start = textbuffer.get_start_iter()
            end = textbuffer.get_end_iter()
            text = textbuffer.get_text(start, end, False)
            self.processedMedia[index][1] = text

            index += 1
        
        renameMedia.rename_media(self.processedMedia, self.directory)
       
    def closeWindow(self, params):
         
        self.close()
            

class DialogBox(Gtk.Dialog):

    def __init__(self, parent, labelText, title): 
        
        Gtk.Dialog.__init__(self, title, parent, 0, 
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        
        label = Gtk.Label(labelText)

        box = self.get_content_area() 
        box.add(label)
        self.show_all()


win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()
