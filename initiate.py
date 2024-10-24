"""
    To run all the necessary programs in one step.
    Second program will run depending upon the status
    of the first one.
    To initiate the project this is the only file that
    needs to be run given the other programs are in the 
    same working directory.
"""

# importing necessary modules
import subprocess

# Run the load program and check the return status. 
# If return status is non-zero go to the exceptions.
# If return status is zero run the second program.
try:
    subprocess.run(['python', 'load_data.py'], check=True)
    subprocess.run(['python', 'analysis2.py'], check=True)

except subprocess.CalledProcessError as error:
    print(f'Data for the city is not properly loaded. Please check city name again.\n')
    print(f'Error: Failed with exit code {error.returncode}\n')

except Exception as excptn:
    print(f'Error: unexpected error {excptn}\n')

