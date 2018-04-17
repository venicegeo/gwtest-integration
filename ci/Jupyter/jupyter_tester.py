#! python

import json, re, sys, subprocess, os

# Convert input files to JSON.
expected_responses_json = json.load(open(sys.argv[1]))
notebook_under_test = expected_responses_json["path"]
expected_command_responses = expected_responses_json["outputs"]
notebook_path = os.path.dirname(notebook_under_test)
# Execute the notebook
subprocess.call(["jupyter", "nbconvert", "--to", "notebook", "--execute", "--ExecutePreprocessor.timeout=600", "--ExecutePreprocessor.interrupt_on_timeout=True",
	"--ExecutePreprocessor.allow_errors=True", "--ExecutePreprocessor.kernel_name=pythonwithpixiedustspark21",
	"--output", "results.ipynb", notebook_under_test
	])
results = json.load(open(notebook_path + "/results.ipynb"))

# Extract all output fields from the results file.
cell_outputs = [cell["outputs"] for cell in results["cells"] if "outputs" in cell]

# Will become 1 if failure occurs
exit_code = 0

if not len(cell_outputs) == len(expected_command_responses):
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("WARNING: There is not an equal number of")
	print("         Results and Matching Patterns!")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	exit_code = 1

for i, expected_command_response in enumerate(expected_command_responses):
	# For each output/regex pair:

	print("")
	print("Checking Output %d" % i)
	print("-----------------")

	if not expected_command_response:
		print(" - Skipped")
		continue

	try:
		cell_output = cell_outputs[i]
	except:
		# Print failure for each cell without an associated regex.
		print(" - Failure: Output Not Present.")
		exit_code = 1 # Should already be 1.
		continue

	for i, expected_output in enumerate(expected_command_response):
		# Check each regex in the list of regexes for the section
		# Each regex section should pair with an output.

		# Get the output and the regex to compare it to for this iteration.
		output = cell_output[i]
		p = re.compile(expected_output)

		if "ename" in output:
			# For errors, mark as failure, print.
			exit_code = 1
			print(" - Failure: %s" % output["ename"])
		elif "text" in output:
			text = "\n".join(output["text"])
			if p.search(text):
				# If a match, print success.
				print(" - Passed")
			else:
				# For mismatches, mark as failure, print.
				exit_code = 1
				print(" - Failure: String mismatch")
				print("   - Actual String:")
				for line in output["text"]:
					print("     - ", line)
				print("   - Expected Pattern:")
				print("     - ", expected_output)
		else:
			# Mark as a failure if pass/failure can't be determined.
			exit_code = 1
			print(" - Failure: Could not read output")

# Exit with the result of the test.
sys.exit(exit_code)