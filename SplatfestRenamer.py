# Splatfest Renamer - For easy batch renaming of Splatoon 3 splatfest files
import os
import time


# General variables
# game_name = input("Enter game abbreviation: ").upper()

# splatfest_teams = [
# 	input("Team 1: "),
# 	input("Team 2: "),
# 	input("Team 3: ")
# ]
# splatfest_name = f"{splatfest_teams[0]} vs. {splatfest_teams[1]} vs. {splatfest_teams[2]}"
# special_fest_name = input("Enter alt fest name if applicable (such as \"Ice-cream Splatfest\"). Otherwise, press enter: ")

# Splatfest shirts
tee_side = [
	"front",
	"back"
]
side = 0

# Idol groups/names
idol_group = [
	["Deep Cut", "Shiver", "Frye", "Big Man"],
	["Squid Sisters", "Callie", "Marie"],
#	["Off the Hook", "Pearl", "Marina"],
]
idol_select = 0

# File template generation stuff
generate_template = False
path_to_template_file = ""
colors_count = None

# This is hacky and stupid but i think this is what this is meant to be used for so its fine
splatfest_name = "None"


def __main__():
	# Setup
	# This is deprecated but im keeping it on the off chance i need it for like
	# Splatoon 4 or something.
	game_name = "S3"
	splatfest_teams = [
		input("Team 1: "),
		input("Team 2: "),
		input("Team 3: ")
	]
	for team in splatfest_teams:
		if team == "" or None:
			retry = input(f"WARNING: The value of Team {splatfest_teams.index(team) + 1} is \"{team}\". Would you like to re-input? (Y/N)").lower()
			if retry == "y":
				input(f"Enter Team {splatfest_teams.index(team) + 1}: ")
			else:
				if retry != "n":
					print("Invalid input. Defaulting to No")
				print(f"Continuing with Team {splatfest_teams.index(team) + 1} as \"{team}\"")
					

	global splatfest_name
	splatfest_name = f"{splatfest_teams[0]} vs {splatfest_teams[1]} vs {splatfest_teams[2]}"
	global splatfest_name_period 
	splatfest_name_period = f"{splatfest_teams[0]} vs. {splatfest_teams[1]} vs. {splatfest_teams[2]}"
	special_fest_name = input("Enter alt fest name if applicable (such as \"Ice-cream Splatfest\" or \"Frostyfest\"). Otherwise, press enter: ")

	repeat = True
	while repeat == True:
		choose_format(splatfest_teams, splatfest_name, special_fest_name)
		repeat_response = input("Perform another rename? (Y/N)\n")
		if repeat_response.lower() == "y":
			repeat = True
		else:
			if repeat_response.lower() != "n":
				print("Invalid response. Defaulting to No")
			repeat = False
	print("See you next time o7")
	time.sleep(2)



def choose_format(splatfest_teams, splatfest_name, special_fest_name, game_name="S3", function=None):
	format_select_1 = input("Screenshot category: \n1: Tee \n2: Sprinkler of Doom \n3: Idols \n4: Splatfest Jellyfish\n")
	# I don't remember what this code does if anything at all
	if function:
		format_select_1 = function
	# team = int(input(f"Select team: \n1: {splatfest_teams[0]}\n2: {splatfest_teams[1]}\n3: {splatfest_teams[2]}")) - 1
	

	match format_select_1.lower():
		# Eventually cycle through and accept input for each file to be renamed
		# Ideally put the renaming in its own function....
		case "1":
			repeat = True
			while repeat == True:
				tee(splatfest_teams, game_name)
				repeat = repeat_function()


		case "2":
			sprinkler(splatfest_teams, game_name)

		case "3":
			day_choice = input("Day (1, 2): ")
			group_list = []
			
			# dynamically generate idol group choices
			# uuuuuh this was done pretty badly and im too afraid to fix it now. Sorry
			idol_group_choice_text = "Idol group: "
			for list in idol_group:
				group_list.append(list[0])
				idol_group_choice_text += "\n" + str(group_list.index(list[0]) + 1) + ". " + (group_list[-1])
			idol_group_choice_text += "\n"
			idol_group_choice = int(input(idol_group_choice_text)) - 1
			idol_group_choice_raw = idol_group_choice
			
			if special_fest_name == "":
				special_fest_name == None
			# idol_select = 1
			if day_choice == "1":
				if idol_group_choice in range(0,2):
					idols_day_1(idol_group_choice, idol_group[idol_group_choice], splatfest_teams, splatfest_name, alt_fest_name=special_fest_name)
				else:
					# Literally just lie to the user because im fucking with their input for index purposes
					print(f"Invalid input: {idol_group_choice_raw}. Expected: [1, 2]")

			elif day_choice == "2":
					if idol_group_choice in range(0,2):
						idols_day_2(idol_group_choice, idol_group[idol_group_choice], splatfest_name, alt_fest_name=special_fest_name)
					else:
						print(f"Invalid input: {idol_group_choice_raw}. Expected: [1, 2]")

			else:
				print(f"Invalid input. Input: {day_choice}. Expected: [1, 2]")
		
		case "4":
				jellyfish(splatfest_teams, game_name)
			

def repeat_function():
	choice = input("Repeat operation? (Y/N)\n")
	if choice.lower() == "y":
		return True
	if choice.lower() == "n":
		return False
	else:
		print("Invalid input. Defaulting to No")
		return False


def rename_file(new_filename):
	# Gets the path to the file to rename
	file_to_rename = input(f"Drag file to be renamed to \"{new_filename}\", and press enter:\n")

	if len(file_to_rename) > 0:
		# Allows for skipping of one filename
		if file_to_rename.lower() == "0":
			print(f"Skipping {new_filename}...")
			return False, None
		# Checks for quotes to compensate for windows sucking
		if file_to_rename[0] == "\"" or "'":
			file_to_rename = file_to_rename[1:-1]
	
	else:
		print("Filepath cannot be empty. Please try again.")
		return True, None
	
	# If the path doesn't exist, prompt to try again
	if not os.path.isfile(file_to_rename):
		print(f"ERROR: The filename/path, \"{file_to_rename}\" is invalid. Please try again.")
		return True, None

	# Splits filename from path, separately splits file extension
	head, tail = os.path.split(file_to_rename)
	_discard, file_extension = os.path.splitext(tail)
	# Stitches the new file name, file extension, and filepath together
	new_filename += file_extension
	new_filename = os.path.join(head, new_filename)

	# For use in the Template function
	global path_to_template_file 
	path_to_template_file = head

	# Checks if the file exists. If yes, throws an error.  If no, renames the file
#	print(new_filename)
	if os.path.isfile(new_filename):
		retry = input(f"A file already exists in {tail} under the name {new_filename}. Press Enter to retry or type 1 to cancel.\n")
		if retry == "1":
			print("Rename operation canceled by user.")
		else:
			os.rename(file_to_rename, new_filename)
	else:
		os.rename(file_to_rename, new_filename)

	# Returning false tells the while loop not to try again so it can move on
	print("Operation finished.")
	return False, file_extension



# ----------- CATEGORY FUNCTIONS BEGIN HERE -----------

def tee(teams, game_name="S3"):
	team = input(f"Team: \n1: {teams[0]} \n2: {teams[1]} \n3: {teams[2]} \n")
	side = 0
	# Repeats once to get both sides of the shirt renamed
	while side <= 1:
		cur_team = teams[int(team) - 1]
		cur_side = tee_side[int(side)]
		new_filename = f"{game_name} Splatfest Tee {cur_team} {cur_side}"

		# Gallery caption
		# This setup is dumb as hell but im too tired to refactor my rename_file func
		# So this is what you get
		# My super laser  spaghetti code
		_discard, file_extension = rename_file(new_filename)
		if file_extension:
			generate = template_ask()
			if generate:
				image_caption = f"\n{new_filename}{file_extension}|Team {cur_team} {cur_side} view\n\n"
				file_template("tee", generate, team=cur_team, tee_side=cur_side, gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))
		else:
			print("Skipped")
		side = side + 1


def idols_day_1(group_index, group, teams, splatfest_name, alt_fest_name=None, game_name="S3"):
	# Group index is as follows:
	# 1: Deep Cut
	# 2: Squid Sisters
	# 3: Off the Hook (not currently set up)
	if group_index == 0:
		for member in group[1:]:
			if alt_fest_name == None or "":
				# Creates the new filename and links deep cut member to their proper splatfest team
				new_filename = f"{game_name} {alt_fest_name} {teams[group.index(member) - 1]} {member}"

				# Gallery caption
				_discard, file_extension = rename_file(new_filename)
				if file_extension:
					generate = template_ask()
					if generate: 
						if member == "Big Man":
							pronoun = "his"
						else:
							pronoun = "her"
						image_caption = f"\n{new_filename}{file_extension}|{member} performing in {pronoun} Splatfest colors\n\n"

						file_template("idols_1", generate, group=group[0], team=teams[group.index(member) - 1], member=member, splatfest_teams=splatfest_name,  gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))

			else:
				new_filename = f"{game_name} Splatfest {teams[group.index(member) - 1]} {member}"
				
				# Gallery caption
				_discard, file_extension = rename_file(new_filename)
				if file_extension:
					generate = template_ask()
					if generate:
						if member == "Big Man":
							pronoun = "his"
						else:
							pronoun = "her"
						image_caption = f"\n{new_filename}{file_extension}|{member} performing in {pronoun} Splatfest colors\n\n"

						file_template("idols_1", generate, group=group[0], team=teams[group.index(member) - 1], member=member, splatfest_teams=splatfest_name,  gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))

	elif group_index == 1:
		for member in group[1:]:
			if alt_fest_name == None or "":
				new_filename = f"{game_name} {alt_fest_name} {member} Day 1 colors"
			else:
				new_filename = f"{game_name} {splatfest_name} {member} Day 1 colors"
			
			# Gallery caption
			_discard, file_extension = rename_file(new_filename)
			if file_extension:
				generate = template_ask()
				if generate:
					image_caption = f"\n{new_filename}{file_extension}|{member}'s color variants\n\n"
					file_template("idols_1", generate, group=group[0],team=teams[group.index(member) - 1], member=member, gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))



def idols_day_2(group_index, group, splatfest_name, alt_fest_name=None, game_name="S3"):
	# Group index is as follows:
	# 1: Deep Cut
	# 2: Squid Sisters
	# 3: Off the Hook (not currently set up)
	if group_index == 0:
		if alt_fest_name == None or "":
			new_filename = f"{game_name} {alt_fest_name} {group[0]}"
		else: 
			new_filename = f"{game_name} {splatfest_name} Splatfest {group[0]}"
		
		# Gallery caption
		_discard, file_extension = rename_file(new_filename)
		if file_extension:
			generate = template_ask()
			if generate:
				image_caption = f"\n{new_filename}{file_extension}|Deep Cut performing on day 2\n\n"
				file_template("idols_2", generate, group=group[0], splatfest_teams=splatfest_name_period, gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))

	elif group_index == 1:
		global colors_count
		colors_count = 1
		while colors_count <= 2:
			if alt_fest_name == None or "":
				new_filename = f"{game_name} {alt_fest_name} {group[0]} Day 2 colors {colors_count}"
			else:
				new_filename = f"{game_name} {splatfest_name} Splatfest {group[0]} Day 2 colors {colors_count}"
			
			if colors_count == 1:
				caption_with_day = "First half of the Squid Sisters' day 2 color variants\n\n"
			else:
				caption_with_day = "Second half of the Squid Sisters' day 2 color variants\n\n"
			colors_count += 1

			# Gallery caption
			_discard, file_extension = rename_file(new_filename)
			
			if file_extension:
				generate = template_ask()
				if generate:
					image_caption = f"\n{new_filename}{file_extension}|{caption_with_day}\n\n"
					file_template("idols_2", generate=generate, group=group[0], splatfest_teams=splatfest_name, gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))

	else:
		print(f"Invalid group: {group_index}. I don't know how you managed this but please report it")


# Sprinklers of Doom
def sprinkler(teams, member, game_name="S3"):
	# Loops through teams and assigns the filename, template prompt
	for team in teams:
		run_rename = True
		while run_rename:
			new_filename = f"{game_name} Splatfest Sprinkler of Doom {team}"
			
			# Gallery caption
			# run_rename is required here, so do not _discard
			run_rename, file_extension = rename_file(new_filename)
			if not file_extension:
				if not run_rename:
					break
			
			if not run_rename:
				generate = template_ask()
				if generate:
					image_caption = f"\n{new_filename}{file_extension}|{member}'s Team {team} Sprinkler of Doom\n\n"
					file_template("sprinkler", generate, team, member, gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))
	


# Jellyfish. cycles through all of them in team order and then types in alphabetical order
def jellyfish(teams, game_name="S3"):
	jellyfish_types = [
		"",
		"Baby ",
		"Glowstick ",
		"Tall "
	]

	# Loops through teams and jellyfish types, and repeats the prompt for invalid filepaths
	for team in teams:
		for type in jellyfish_types:
			run_rename = True
			while run_rename:
				new_filename = f"{game_name} Team {team} {type}Jellyfish"
							
				# Gallery caption
				# run_rename is required here, so do not _discard
				run_rename, file_extension = rename_file(new_filename)
				if not file_extension:
					if not run_rename:
						break

				if not run_rename: 
					generate = template_ask()
					if generate:
						image_caption = f"\n{new_filename}{file_extension}|Team {team} {type}Jellyfish\n\n"
						file_template("jellyfish", generate, jellyfish_type=type, team=team, gallery_caption=image_caption, filename=".".join([new_filename, file_extension[1:]]))

	# SAMPLE OUTPUT : 
		



# ------------ CATEGORY FUNCTIONS END HERE ------------



def template_ask():
	# Ask to generate template
	generate_template_ask = input("Generate File Template and Gallery caption? (Y/N)\n").lower()
	if generate_template_ask == "y":
		generate_template = True
	else:
		if generate_template_ask != "n":
			print("Invalid input. Defaulting to No")
		generate_template = False
	# And return the result
	return generate_template


# ----------- TEMPLATE CREATIONS BEGIN HERE -----------

def file_template(category, generate=False, team=None, tee_side=None, splatfest_teams=None, group=None, member=None, jellyfish_type=None, filename=None, gallery_caption=None):
	global splatfest_name
	global splatfest_name_period
	
	# If generate was set properly
	if generate:
		match category:
			case "tee":
				# Tees
				# Requires: team, tee_side
				file_template = f'''{filename}
{{{{File 
|game=Splatoon 3
|description=The Team {team} [[Splatfest Tee]] from the {tee_side}.
|type=splatfestteamtee
|source=self
}}}}'''
				# file_template = f"{{{{File \n|game=Splatoon 3\n|description={member} during the {teams} Splatfest. Screenshot taken with a capture card.}}}}"
				output_template(file_template, gallery_caption)

			case "idols_1":
				# Idols day 1
				costumed = costume_ask_func()
				# Deep Cut
				# Requires: member, splatfest_teams
				if group == "Deep Cut":
					if costumed:
						costume_text = " in costume"
					else:
						costume_text = ""

					file_template = f'''{filename}
{{{{File 
|game=Splatoon 3
|description=[[{member}]]{costume_text} during the [[{splatfest_name_period}]] Splatfest.
|type=screenshot
|source=self
}}}}'''
					output_template(file_template, gallery_caption)

				# Squid sisters
				# Requires: member, splatfest_teams
				elif group == "Squid Sisters":
					if costumed:
						costume_text = [" performing in her costume", ""]
					else:
						costume_text = ["'s color variants", ". Screenshots taken then cropped and combined."]
					file_template = f'''{filename}
{{{{File 
|game=Splatoon 3
|description=[[{member}]]{costume_text[0]} during the first half of the [[{splatfest_name_period}]] Splatfest{costume_text[1]}.
|type=screenshot
|source=self
}}}}'''
					output_template(file_template, gallery_caption)
					
				else:
					print("ERROR: Neither DC nor SS calling properly!")
					file_template, gallery_caption = "ERROR"
					output_template(file_template, gallery_caption)

					
			case "idols_2":
				# Idols day 2
				costumed = costume_ask_func()
				if group == "Deep Cut":
				# Deep Cut
				# Requires: group, splatfest_teams
					if costumed:
						file_template = f'''{filename}
{{{{File
|game=Splatoon 3
|description=[[{group}]] performing in their costumes on day 2 of [[{splatfest_name_period}]].
|type=screenshot
|source=self
}}}}'''
					else:
						file_template = f'''{filename}
{{{{File
|game=Splatoon 3
|description=[[{group}]]'s colors on day 2 of [[{splatfest_name_period}]].
|type=screenshot
|source=self
}}}}'''
					output_template(file_template, gallery_caption)


				# Squid Sisters
				# Requires: group, splatfest_teams
				elif group == "Squid Sisters":
					if costumed:
						file_template = f'''{filename}
{{{{File
|game=Splatoon 3
|description=The [[{group}]] performing in their costumes during the second half of the [[{splatfest_name_period}]] Splatfest.
|type=screenshot
|source=self
}}}}'''
					else:
						# I know it's kind of bad practice
						# But i don't want to refactor all this for a 6th time
						# Grab the global colors_count
						global colors_count
						if colors_count <= 2:
							half = "first half "
						else:
							half = "second half "

						
						file_template = f'''{filename}
{{{{File
|game=Splatoon 3
|description=The {half}of the {group}' color variants during the second half of the [[{splatfest_name_period}]] Splatfest. Screenshots taken then cropped and combined.
|type=screenshot
|source=self
}}}}'''
					output_template(file_template, gallery_caption)
				else:
					print(f"Group \"{group}\" unrecognized")


			case "jellyfish":
				# Jellyfish
				# Requires: team, jellyfish_type, splatfest_teams
				file_template = f'''{filename}
{{{{File
|game=Splatoon 3
|description=A Team {team} {jellyfish_type}jellyfish during [[{splatfest_name_period}]]
|type=screenshot
|source=self
}}}}'''
				output_template(file_template, gallery_caption)
			
			case "sprinkler":
				# Sprinkler of Doom
				# Requires: team, member, splatfest_teams
				file_template = f'''{filename}
{{{{File
|game=Splatoon 3
|description=[[{member}]]'s [[{splatfest_name_period}|Team {team}]] [[Sprinkler of Doom]]
|type=screenshot
|source=self
}}}}'''
				output_template(file_template, gallery_caption)

			# Should be impossible
			case _ :
				print("How did you manage this")

# ------------ TEMPLATE CREATIONS END HERE ------------


# Outputs finished template and gallery caption, labeled with filename
# Gallery caption is now a required argument
def output_template(file_template, gallery_caption):
	# Creates/modifies a text file to append the file template to
	# Throws an error and aborts if file template would default to where the script is
	# This is easily changed if the user would rather that be expected behavior
	# But i don't suggest it to keep things organized
	if not os.path.exists(path_to_template_file):
		print("ERROR: Invalid filepath. Cannot output file template")
		return
	template_file_with_path = os.path.join(path_to_template_file, "TemplateFile.txt")
	template_file = open(template_file_with_path, "a")
	template_file.write(file_template)
	template_file.write(gallery_caption)
	template_file.close()
	# I remembered to close it this time so i dont cause a memory leak again :itcoheres:
	print(f"File template and gallery caption appended to {template_file_with_path}")


# Ask if the idols are in costume
def costume_ask_func():
	costume_ask = input("Are the idols in costume? (Y/N)\n").lower()
	if costume_ask == "y":
		costumed = True
	else:
		if costume_ask != "n":
			print("Invalid input. Defaulting to No")
		costumed = False
	return costumed


# Defines main function
if __name__ == "__main__":
	__main__()