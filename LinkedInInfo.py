from linkedin_api import Linkedin
from linkedin_api.client import ChallengeException
import time

class LinkedInProfileFetcher:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.api = None

    def authenticate(self):
        try:
            self.api = Linkedin(self.email, self.password)
            self.api.get_profile(self.email)
            return True
        except ChallengeException:
            print("Authentication failed: Challenge required. Check your credentials.")
            return False
        except Exception as e:
            print(f"An error occurred during authentication: {e}")
            return False

    def fetch_linkedin_info(self):
        """
        Fetches LinkedIn profile information for a specific connection.
        """
        desired_connection = input("Enter the name of who you want to query information for (firstname-lastname): ")
        profile_desired = self.api.get_profile(desired_connection)
        return profile_desired

    @staticmethod
    def remove_dict_from_list(dict_list):
        """
        Helper function to merge dictionaries in a list into a single dictionary.
        """
        merged_dict = {}
        for i in dict_list:
            merged_dict.update(i)
        return merged_dict

    def fetch_company_info(self, specific_info):
        """
        Fetches company name from the 'experience' section of the LinkedIn profile.
        """
        if isinstance(specific_info, dict):
            if 'experience' in specific_info:
                company_name = specific_info['experience']

                if isinstance(company_name, list):
                    for item in company_name:
                        if isinstance(item, dict) and 'companyName' in item:
                            return item['companyName']

                elif isinstance(company_name, dict):
                    if 'companyName' in company_name:
                        return company_name['companyName']
                else:
                    print("DataType Invalid")
            else:
                print("'experience' key not found")
        else:
            print('DataType Invalid')

        return None

    def fetch_school_name(self, specific_info):
        """
        Fetches school name from the 'education' section of the LinkedIn profile.
        """
        def dict_case(specific_info):
            count = 0
            school_name_col = None
            for i in specific_info.keys():
                if i == 'education':
                    count += 1
                    if count == 1:
                        school_name = self.remove_dict_from_list(specific_info[i])
                        for j in school_name.keys():
                            if j == 'schoolName':
                                school_name_col = school_name[j]
            return school_name_col

        if isinstance(specific_info, dict):
            school_name_col = dict_case(specific_info)
        elif isinstance(specific_info, list):
            merged_dict = self.remove_dict_from_list(specific_info)
            school_name_col = dict_case(merged_dict)
        else:
            print('Enter a valid data type!')

        return school_name_col

    def fetch_position_info(self, specific_info):
        """
        Fetches position information from the 'experience' section of the LinkedIn profile.
        """
        def if_dict_sit(specific_info):
            count = 0
            for i in specific_info.keys():
                if i == 'experience':
                    count += 1
                    if count == 1:
                        pos_info = specific_info[i]
                        pos_info_dict = self.remove_dict_from_list(pos_info)
                        pos_name = pos_info_dict['title']
            return pos_name

        if isinstance(specific_info, dict):
            pos_name = if_dict_sit(specific_info)
        elif isinstance(specific_info, list):
            merged_dict = self.remove_dict_from_list(specific_info)
            pos_name = if_dict_sit(merged_dict)

        return pos_name

    def fetch_specific_linkedin_info(self, profile_desired):
        """
        Fetches specific LinkedIn profile information based on user input.
        """
        # init info desired with a user input
        info_desired = input("From these options: [education, experience, position] what information do you want to fetch: ")

        # case based on the type of information requested
        if info_desired == 'education':
            return self.fetch_school_name(profile_desired)
        elif info_desired == 'experience':
            return self.fetch_company_info(profile_desired)
        elif info_desired == 'position':
            return self.fetch_position_info(profile_desired)
        else:
            print('Info type not recognized, try again!')

        return None

def main():
    max_attempts = 3
    attempt_limit_seconds = 120  
    attempts = 0
    lockout_start_time = None

    while True:
        if attempts >= max_attempts:
            if lockout_start_time is None:
                lockout_start_time = time.time()

            # enforce attempt and give 2 min penalty if limit exceeded
            current_time = time.time()
            if (current_time - lockout_start_time) < attempt_limit_seconds:
                remaining_time = int(attempt_limit_seconds - (current_time - lockout_start_time))
                time.sleep(remaining_time)
                attempts = 0
                lockout_start_time = None
            else:
                attempts = 0
                lockout_start_time = None

        # ask user for their LinkedIn credentials
        user_email = input("Enter your LinkedIn email address: ")
        user_password = input("Enter your LinkedIn password: ")

        # init LinkedInProfileFetcher with credentials
        fetcher = LinkedInProfileFetcher(user_email, user_password)

        # check authentication
        if fetcher.authenticate():
            profile_desired = fetcher.fetch_linkedin_info()
            if profile_desired:
                info_desired_out = fetcher.fetch_specific_linkedin_info(profile_desired)
                print(info_desired_out)
            break
        else:
            attempts += 1
            if attempts < max_attempts:
                remaining_attempts = max_attempts - attempts
                print(f"Invalid credentials. You have {remaining_attempts} attempts left.")
            else:
                print("Too many failed attempts. Please wait 2 minutes before trying again.")


if __name__ == "__main__":
    main()
