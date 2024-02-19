import os
import re
import argparse
from datetime import datetime, timedelta
from fnmatch import fnmatch

class ObsidianPostponer():

	def __init__(self, config_dict):
		# State storage
		self._config = config_dict
		self._today = datetime.today()

		# File path storage
		self._file_paths = list()

		# Counters
		self._total_file_count = 0

		self._postponed_notes_count = 0
		self._postponed_cards_count = 0

		self._due_counts = {
			'note': 0,
			'card': 0
		}

	def run(self):
		file_extension = self._config['markdown_file_extension']
		if self._generate_file_paths(file_extension):
			postpone_days = self._config['postpone_by_days']
			self._run_postponers(postpone_days)

		self._print_total_stats()

	def _generate_file_paths(self, ext):
		count = 0
		for dirpath, dirnames, files in os.walk('.'):
			"""
			dirpath:
				path of the current dir relative to the script
			dirnames:
				list of subdirs within the current dir
			files:
				list of files in current dir
			"""
			for filename in files:
				if fnmatch(filename, f"*{ext}"):
					count += 1
					relative_path = os.path.join(dirpath, filename)
					absolute_path = os.path.abspath(relative_path)
					self._file_paths.append(absolute_path)
		self._total_file_count = count
		return count

	def _prepare_postponer_list(self):
		executor_list = list()
		if self._config['postpone_notes']:
			executor_list.append(self._postpone_notes)
		if self._config['postpone_cards']:
			executor_list.append(self._postpone_cards)
		return executor_list

	def _run_postponers(self, days):
		executor_list = self._prepare_postponer_list()

		for file_path in self._file_paths:
			file_contents = self._read_file_contents(file_path)
			
			# Shallow copy is enough here, contains no mutables
			due_counts_before = self._due_counts.copy() # Tracks number of already due items

			sum_of_replacements = 0 # overall counter of replacements done in a file
			for postponing_executor in executor_list:
				postponed_content, num_replacements = postponing_executor(file_contents, days)
				if num_replacements:
					sum_of_replacements += num_replacements
					# If multiple executors are run and any one of them
					# makes a change in the file contents, `file_contents` has to be 
					# updated otherwise the next executor would work with an superseded
					# version of it. I.e. without updating the next executor
					# would overwrite the work of the previous executor.
					### self._save_file_contents(file_path, postponed_content)
					file_contents = postponed_content			
			
			if sum_of_replacements:
				self._save_file_contents(file_path, file_contents)
			
			due_counts_after = self._due_counts.copy() # The postponers may have incremented this number
			if due_counts_after != due_counts_before:
				# Calculate differences for cards and notes
				count_diff = {
					k: due_counts_after[k] - due_counts_before[k]
					for k in self._due_counts.keys() # defined in __init__
					}
				if self._config['verbose']:
					self._print_due_file_stats(file_path, count_diff)

		return None #ToDo

	def _read_file_contents(self, file_path): 
		with open(file_path, 'r', encoding = 'utf-8') as file:
			file_contents =  file.read()
		return file_contents

	def _save_file_contents(self, file_path, file_contents):
		with open(file_path, 'w', encoding = 'utf-8') as file:
			file.write(file_contents)
		return None
	
	def _postpone_notes(self, file_contents, days):
		# `sr-due: 2024-02-13`
		pattern = r"(sr-due: )([0-9]{4}-[0-9]{2}-[0-9]{2})"
		#               |                    |
		#         match.group(1)        match.group(2)

		def run_replacer(match):
			return self._replace_date_in_match(match, days, caller = 'note')

		# Since there is only one note date to change it makes sense
		# to terminate the search after findin it. Hence `count = 1`
		file_contents, num_repl = re.subn(pattern, 
										 run_replacer,
										 file_contents,
										 count = 1)

		self._postponed_notes_count += num_repl # 0 if no matches were found
		return file_contents, num_repl

	def _postpone_cards(self, file_contents, days):
		# `<!--SR:!2024-02-09` --> this is enough for identifying card due dates
		pattern = r'(<!--SR:!)([0-9]{4}-[0-9]{2}-[0-9]{2})'
		#               |                    |
		#         match.group(1)        match.group(2)

		def run_replacer(match):
			return self._replace_date_in_match(match, days, caller = 'card')

		file_contents, num_repl = re.subn(pattern, 
										 run_replacer,
										 file_contents)

		self._postponed_cards_count += num_repl # 0 if no matches found
		return file_contents, num_repl
	
	def _replace_date_in_match(self, match, days, caller):
		# Date info is assumed to be stored in `match.group(2)`
		# See `_postpone_notes` & `_postpone_cards`
		old_date_str = match.group(2)
		new_date_str = self._shift_date(old_date_str, days, caller)
		return f"{match.group(1)}{new_date_str}"

	def _shift_date(self, old_date_str, days, caller):
		old_date = self.parse_date(old_date_str) # datetime obj.
		new_date = old_date + timedelta(days)
		new_date_str = self.format_date(new_date)

		self._update_due_counts(old_date, caller)		
		return new_date_str
	
	def _update_due_counts(self, date, caller):
		if (self._today - date).days >= 0:
			self._due_counts[caller] += 1
		return None
	
	def _print_due_file_stats(self, file_path, diff_dict):
		print(f" {os.path.basename(file_path)}")
		print("   Due items:")
		for k, v in diff_dict.items():
			if v > 0: # display non-zeroes only
				print(f"      - {v} {k}(s)", end = None) # e.g. "- 15 card(s)"
		print()
		print()
		return None

	def _print_total_stats(self):
		print("#" * 80)
		print()
		print(f" Markdown files found: {self._total_file_count}")
		print()
		print(f" - Postponed the following by {self._config['postpone_by_days']} days:")
		print(f"   - Note review dates:\t {self._postponed_notes_count}\t ({self._due_counts['note']} were due)")
		print(f"   - Card review dates:\t {self._postponed_cards_count}\t ({self._due_counts['card']} were due) ")
		return None
	
	@staticmethod
	def parse_date(date_str):
		return datetime.strptime(date_str, "%Y-%m-%d")

	@staticmethod
	def format_date(datetime_obj):
		return datetime.strftime(datetime_obj, "%Y-%m-%d")
	

def create_initial_config():
	config = dict()
	config['markdown_file_extension'] = ".md"
	config['postpone_by_days'] = 0
	config['postpone_cards'] = False
	config['postpone_notes'] = False
	config['verbose'] = False
	return config


def create_parser():
	parser = argparse.ArgumentParser(description = "## Spaced Repetition Postponer for Obsidian ##")

	parser.add_argument("days", help="number of days you want to postpone by (negative numbers are also accepted)", type = int)
	parser.add_argument("-n", "--notes", action = "store_true", help = "notes only will be postponed")
	parser.add_argument("-c", "--cards", action = "store_true", help = "cards only will be postponed")
	parser.add_argument("-v", "--verbose", action = "store_true", help = "list all files that contained any item already due")
	return parser


if __name__ == "__main__":
	config = create_initial_config()
	parser = create_parser()

	args = parser.parse_args()

	config['postpone_by_days'] = args.days
	config['verbose'] = args.verbose

	if args.notes:
		config['postpone_notes'] = True
	elif args.cards:
		config['postpone_cards'] = True
	else:
		config['postpone_notes'] = True
		config['postpone_cards'] = True

	postponer = ObsidianPostponer(config)
	postponer.run()
