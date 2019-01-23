Purpose of this application:
    This is a long running program (LRP) which periodically searches a directory of files for a string.
    If a file is added, deleted, or modified, the application searches for the string without duplicating previous searches.
    Program should continue to run even if errors are encountered.
#
User input:
    User inputs the directory (of files to search) & a string "magic_word" for which to search.
    Optionally, user can input a file extention to specify the file type they want to search& the number of seconds between polling sessions
#
Step 1:
Search the given directory & put those files into a separate dictionary "watching_files", but only if they are not already in there.
Log a message whenever you add a file to "watching_files"
#
Step 2:
Look through your "watching_files" dictionary and compare that to a list of files in the directory.
If you notice that you have a file in "watching_files" that is not in the directory, you need to delete that file from "watching_files"
Log a message whenever you delete a file from "watching_files."
#
Step 3:
Once the directory & "watching_files" are synchronized,
1) iterate through each file in "watching_files" dictionary.
2) start at the last line that you read in each file and look for any "magic text".
3) If "magic text" is found, log the file_name and line number.
4) Update the last position that you read from for each file_name.