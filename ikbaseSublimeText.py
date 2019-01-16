#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re
import sublime
import sublime_plugin
import os
sys.path.append(os.environ['IKBASE_PY3_PACKAGES'])
from git import Repo
from .settings import Settings
from .cryptlib import get_file_list, encode, update_file, get_key, decode
from .message import print_info, print_err


# local pa
ikbase_root_path = os.environ['IKBASE_ROOT']


#
# Create a new output panel, insert the message and show it
#
def panel(window, message):
  p = window.get_output_panel('crypto_error')
  p.run_command("crypto_message", {"message": message})
  p.show(p.size())
  window.run_command("show_panel", {"panel": "output.crypto_error"})


# 拉取更新
class ikbase_pullCommand(sublime_plugin.WindowCommand):
	def run(self, enc):
		repo = Repo(r''+ikbase_root_path)
		remote = repo.remote()
		remote.pull()
		# print('ikbase_pull finish')
		sublime.status_message('>>>> ikbase_pull finish!')
		panel(self.window.active_view().window(), "ikbase pull success!")


# 提交并上传
class ikbase_commitCommand(sublime_plugin.WindowCommand):
	def run(self, enc):
		repo = Repo(r''+ikbase_root_path)
		remote = repo.remote()
		git = repo.git
		git.add('.')
		git.commit('-m', 'commit by sublime text')
		remote.push()
		# print('ikbase_commit finish')
		sublime.status_message('>>>> ikbase_commit finish!')
		panel(self.window.active_view().window(), "ikbase commit and push success!")


class ikbase_encryptedCommand(sublime_plugin.WindowCommand):
	readingInput=False
	pwd=""
	message="Enter Password:"
	obfuscate=False

	def run(self, enc):
		sublime.status_message('ikbase encrypting')
		sts = Settings()
		if not sts.get_encrypted_status():
			self.pwd = ""
			self.readingInput=False
			self.show_input("")
		pass
	def show_input(self, initial):
	    sublime.status_message('show_input')
	    self.window.show_input_panel(
	        self.message, 
	        initial, 
	        self.on_done, None, None)
	def on_done(self, password):
	    sublime.status_message('on_done')
	    try:
	      if self.window.active_view():
	        finalPass = self.pwd if self.obfuscate else password
	        sts = Settings()
	        if not sts.get_encrypted_status():
	            key = finalPass
	            st = update_file(encode, get_file_list(), key)
	            if st:
	            	print('Something went wrong while encrypting')
	            	panel(self.window.active_view().window(), "encrypting error")
	            else:
	            	sts.change_encrypted_status(True)
	            	panel(self.window.active_view().window(), "encrypting success!")
	        self.pwd=""
	        finalPass=""
	    except ValueError:
	      pass


class ikbase_decryptedCommand(sublime_plugin.WindowCommand):
	readingInput=False
	pwd=""
	message="Enter Password:"
	obfuscate=False

	def run(self, enc):
		sublime.status_message('ikbase decrypted')
		sts = Settings()
		if sts.get_encrypted_status():
			self.pwd = ""
			self.readingInput=False
			self.show_input("")
		pass
	def show_input(self, initial):
	    sublime.status_message('show_input')
	    self.window.show_input_panel(
	        self.message, 
	        initial, 
	        self.on_done, None, None)
	def on_done(self, password):
	    sublime.status_message('on_done')
	    try:
	      if self.window.active_view():
	        finalPass = self.pwd if self.obfuscate else password
	        sts = Settings()
	        if sts.get_encrypted_status():
	            key = finalPass
	            st = update_file(decode, get_file_list(), key)
	            if st:
	            	print('Something went wrong while decrypted')
	            	panel(self.window.active_view().window(), "decrypted error")
	            else:
	            	sts.change_encrypted_status(False)
	            	panel(self.window.active_view().window(), "decrypted success!")
	        self.pwd=""
	        finalPass=""
	    except ValueError:
	      pass


# test
# class ikbase_test1111Command(sublime_plugin.TextCommand):
	# def run(self, edit):
	# 	sublime.status_message('ikbase test')
class ikbase_testCommand(sublime_plugin.WindowCommand):
	def run(self, enc):
		print('ikbase test')
		sublime.status_message('ikbase test')
		# print(os.environ['NDK_ROOT'])
		# print(os.environ['IKBASE_ROOT'])
		# print(os.environ.get('IKBASE_ROOT'))
		# try:
		#     if self.window.active_view():
		# 	    panel(self.window.active_view().window(), "hello")
		# except ValueError:
		# 	pass

