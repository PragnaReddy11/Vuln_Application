import os

# Define the log file path and search terms
log_file = "/opt/sonarqube/logs/ce.log"
success_keywords = ["gr8scope"]


def check_sonarqube_analysis(log_file, success_keywords):
    # Check if the log file exists
    if not os.path.isfile(log_file):
        print(
            "Grading Script 1 failed! Check if you have successfully run the analysis."
        )
        return

    # Open and read the log file line by line
    with open(log_file, "r") as file:
        found_success = False

        for line in file:
            # Check if the line contains any of the success keywords
            if any(keyword in line for keyword in success_keywords):
                found_success = True

            # If both are found, print confirmation and break out of loop
            if found_success:
                print("Grading Script 1 passed! +10 points")
                return

    # If analysis was not confirmed, print a message
    if not found_success:
        print(
            "Grading Script 1 failed! Check the name of the project."
        )


# Run the function
check_sonarqube_analysis(log_file, success_keywords)
