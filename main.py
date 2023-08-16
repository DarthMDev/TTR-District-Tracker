# based on https://github.com/dudeman49/TTR-District-Tracker
# this program will read the latest log file from TTR and save the district name to a file in the same directory
import os
import time
import sys
shard_indicator = "Entering shard"
game_dir = ''
if sys.platform == 'win32':
    game_dir = "C:/Program Files (x86)/Toontown Rewritten"
elif sys.platform == 'darwin':
    # game directory is in the Application Support directory
    game_dir = os.path.join(os.environ['HOME'], "Library/Application Support/Toontown Rewritten")
elif sys.platform.startswith('liunx'):
    # lets just let linux users put the executable in the game directory
    game_dir = os.get_cwd()
logs_folder = os.path.join(game_dir, "logs")
district_file_path = os.path.join(game_dir, "district.txt")
district_dictionary = {
        5000: "Gulp Gulch" ,
        5010: "Splashport",
        5020: "Fizzlefield",
        5030: "Whoosh Rapids",
        5040: "Blam Canyon",
        5050: "Hiccup Hills",
        5060: "Splat Summit",
        5070: "Thwackville",
        5080: "Zoink Falls",
        5090: "Kaboom Cliffs",
        5100: "Bounceboro",
        5110: "Boingbury",
        5120: "Zapwood",
        5130: "Splatville"
}

def clear_current_console_line():
    # clear the current console line
    current_line_cursor = 0
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\r", end="")

def main():
    while True:
        # get the latest log file
        
       
        # sort the log files by last modified time
        log_files = sorted(os.listdir(logs_folder), key=lambda f: os.path.getmtime(os.path.join(logs_folder, f)), reverse=True)
        latest_log_file = os.path.join(logs_folder, log_files[0])
        # read the latest log file
        with open(latest_log_file, "r") as log:
            last_line = ""
            for line in log:
                # if the line contains the shard indicator, then it is the last line
                if shard_indicator in line:
                    last_line = line

            shard_number = ""
            if last_line:
                # get the shard number from the last line , e.g. "Entering shard 5000"
                shard_number = last_line.split(":vltc803af4a: Entering shard ")[1][:4]
            else:
                continue # keep checking 
            # convert the shard number to an int
            shard_number_int = int(shard_number)
            # if the shard number is in the district dictionary, then save the district name to a file
            if shard_number_int in district_dictionary:
                district_name = district_dictionary[shard_number_int]

                
                with open(district_file_path, "w") as district_file:
                    district_file.write(district_name)

                clear_current_console_line()
                print(f"{shard_number_int} = {district_name}", end="\r")
                # make sure it stays up to date and makes sure that your CPU doesn't get too hot
                time.sleep(1)

if __name__ == "__main__":
    main()
