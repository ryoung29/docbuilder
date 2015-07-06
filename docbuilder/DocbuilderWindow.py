# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk, WebKit # pylint: disable=E0611
import logging
logger = logging.getLogger('docbuilder')

from docbuilder_lib import Window
from docbuilder.AboutDocbuilderDialog import AboutDocbuilderDialog
from docbuilder.PreferencesDocbuilderDialog import PreferencesDocbuilderDialog
import markdown

# See docbuilder_lib.Window.py for more details about how this class works
class DocbuilderWindow(Window):
    __gtype_name__ = "DocbuilderWindow"
    

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(DocbuilderWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutDocbuilderDialog
        self.PreferencesDialog = PreferencesDocbuilderDialog

        # Code for other initialization actions should be added here.

        self.BoxCount = 1
        self.cbAuthor = self.builder.get_object("cbAuthor")
        self.cbTitle = self.builder.get_object("cbTitle")
        self.tbAuthor = self.builder.get_object("tbAuthor")
        self.tbTitle = self.builder.get_object("tbTitle")
        self.cbDate = self.builder.get_object("cbDate")
        self.tbDate = self.builder.get_object("tbDate")
        self.btnBuild = self.builder.get_object("btnBuilder")
        self.boxFile1 = self.builder.get_object("boxFile1")
        self.boxHeader1 = self.builder.get_object("boxHeader1")
        self.boxDynamic = self.builder.get_object("boxDynamic")
        self.tbHeader1 = self.builder.get_object("tbHeader1")
        self.cbSuppress = self.builder.get_object("cbSuppress")
        self.rbTextBody = self.builder.get_object("rbTextBody")
        self.rbFileBody = self.builder.get_object("rbFileBody")
        self.fcbBody = self.builder.get_object("fcbBody")
        self.btnDelete = self.builder.get_object("btnDelete")
        self.BtnAdd = self.builder.get_object("BtnAdd")
        self.btnExport = self.builder.get_object("btnExport")
        self.btnUp = self.builder.get_object("btnUp")
        self.btnDown = self.builder.get_object("btnDown")
        self.tvBody = self.builder.get_object("tvBody")
        self.tvMarkdown = self.builder.get_object("tvMarkdown")
        self.MarkdownBuffer = self.builder.get_object("MarkdownBuffer")
        self.BodyBuffer1 = self.builder.get_object("BodyBuffer1")
        self.swPreview = self.builder.get_object("swPreview")

    # Event Handlers
    def on_btnBuild_clicked(self, widget):
        if self.cbTitle.get_active():
            MarkdownFinal = "title: " + self.tbTitle.get_text() + "  \n"
    
        if self.cbDate.get_active():
            MarkdownFinal += "date: " + self.tbDate.get_text() + "  \n"

        if self.cbAuthor.get_active():
            MarkdownFinal += "author: " + self.tbAuthor.get_text() + "  \n"

        MarkdownFinal += "...\n\n"
        MarkdownFinal += "# " + self.tbHeader1.get_text() + "\n"
        
        if self.rbTextBody.get_active():
            MarkdownFinal += "\n" + self.BodyBuffer1.get_text(self.BodyBuffer1.get_start_iter(), self.BodyBuffer1.get_end_iter(), True ) + "\n"
        else:
            sFile = self.fcbBody.get_filename()
            iInput = open(sFile,'r') 
            sBody = iInput.read()
            iInput.close()
            MarkdownFinal += "\n" + sBody + "\n"

        end_iter = self.MarkdownBuffer.get_end_iter()
        self.MarkdownBuffer.insert(end_iter, MarkdownFinal)

        self.webview = WebKit.WebView()
        self.swPreview.add(self.webview)
        self.webview.show()
        preview = markdown.markdown(MarkdownFinal)
        ws = self.webview.get_settings() 
        ws.set_property('enable-plugins',False) 
        self.webview.set_settings(ws) 
        self.webview.load_html_string(preview,"file:///")

    def on_rbTextBody_on_group_changed(self, widget):
        self.rbFileBody.Selected = fcbBody.Visible

    def on_cbTitle_toggled(self, widget):
        bChecked = widget.get_active()
        self.tbTitle.set_sensitive(bChecked)
        self.tbTitle.is_focus()

    def on_cbAuthor_toggled(self, widget):
        bChecked = widget.get_active()
        self.tbAuthor.set_sensitive(bChecked)
        self.tbAuthor.is_focus()

    def on_cbDate_toggled(self, widget):
        bChecked = widget.get_active()
        self.tbDate.set_sensitive(bChecked)
        self.tbDate.is_focus()

    def on_cbSuppress_toggled(self, widget):
        bChecked = widget.get_active()
        self.tvBody.set_sensitive(not bChecked)
        self.boxFile1.set_sensitve(not bChecked)

#    def on_fcbBody_file_set(self, widget):
#        sFile = widget.get_filename()
#        iInput = open(sFile,'r') 
#        sBody = iInput.read()
#        iInput.close()

    def on_rbFileBody_toggled(self, widget):
        self.fcbBody.set_sensitive(widget.get_active())
        self.tvBody.set_sensitive(not widget.get_active())

    def on_BtnAdd_clicked(self, widget):
        self.BoxCount += 1
        self.newBox = Gtk.HBox(True,3)
        self.boxDynamic.add(self.newBox)

