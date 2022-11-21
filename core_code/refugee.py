import pandas as pd
import numpy as np
from refugee_input_option import *
from exception.refugee_exception import *
from refugee_validation import *


class Refugee:
    def __init__(self, purpose):
        if purpose == "Register":
            print("Welcome to refugee registration system")
            print("--------------------------------------------")
            print("The form comprises of 3 main sections:\n1. General information\n2. Camp selection\n3. Medical condition\n")
        self.ref_row = []

    def refugee_name(self, refugee_df):
        self.fname, self.lastname = refugee_existence_check(refugee_df)
        self.ref_row.extend([self.fname, self.lastname])
        print("-------------------------------------------")
    def refugee_birthdate(self):
        # enter birthdate + validation
        self.birthdate = birthdate_format_check()
        self.ref_row.extend([self.birthdate])
        print("-------------------------------------------")
    def refugee_gender(self):
        gender_opt = refugee_input_option("Gender")
        gender_dict = input_matching("Gender")
        print("Select refugee's gender")
        self.gender = gender_dict[int(numerical_input_check(gender_opt)[0])]
        self.ref_row.extend([self.gender])
        print("-------------------------------------------")
    def refugee_race(self):
        race_opt = refugee_input_option("Ethnic Group")
        race_dict = input_matching("Ethnic Group")
        print("Select refugee's ethnic group")
        self.race = race_dict[int(numerical_input_check(race_opt)[0])]
        if ("Others" in self.race):
            self.race = input("Specify refugee's ethnic group: ")
        self.ref_row.extend([self.race])
        print("-------------------------------------------")
    def refugee_contact(self):
        self.email = email_format_check()
        self.phone = input("Enter refugee's phone number (if any): ")
        self.ref_row.extend([self.email,self.phone])
        print("-------------------------------------------")
    def refugee_family(self):
        self.family_member = int(input(
            "How many members are there in refugee's family?(input 0 if no family): "))
        print("-------------------------------------------")
        # append general data to row
        self.ref_row.extend([self.family_member])
        if self.family_member > 0:
            self.members = input(
                "Enter all members' first name (e.g. Dan, John, Emily): ")
            # add member's name
            self.ref_row.extend([self.members])
        else:
            self.ref_row.extend(["-"])

    def assign_camp_ID(self, camp_df, purpose, previous_camp=0):
        print("INSTRUCTION: Please assign the camp identification to the refugee.")
        print("The detail below shows the availability of each camp as well as its related conditions: ")
        print(camp_df)
        print("-------------------------------------------")
        # camp validation + assigned
        self.assigned_camp = camp_capacity_check(camp_df)
        # append camp number to the row
        self.ref_row.extend([self.assigned_camp])
        print("-------------------------------------------")
        # update number of refugees
        camp_df.at[self.assigned_camp-1,
                   'num_of_refugees'] = int(camp_df.loc[self.assigned_camp-1, 'num_of_refugees']) + 1
        if purpose == "edit":
            # reduce number in previous camp before edited
            camp_df.at[previous_camp-1,'num_of_refugees'] = int(camp_df.loc[previous_camp-1, 'num_of_refugees']) - 1

        # write data to csv
        with open('info_files/camp.csv', 'w') as f:
            camp_df.to_csv(f, index=False)
        print(
            f"Refugee is successfully assigned to the camp number {self.assigned_camp}.")

    def refugee_illnesses(self):

        print("------------- SECTION 1 : ILLNESSES --------------")
        ill_opt = refugee_input_option("Illnesses")
        ill_dict = input_matching("Illnesses")
        print("Select refugee's personal illness")
        # array of input
        ill_inpts = numerical_input_check(ill_opt)
        
        # convert numerical input to text
        self.ref_illness = []
        for v in ill_inpts:
            self.ref_illness.append(ill_dict[int(v)])

        for ind, il in enumerate(self.ref_illness):
            if "Allergies" in il:
                print("-------------ALLERGIES--------------")
                aller_opt = refugee_input_option("Allergies")
                aller_dict = input_matching("Allergies")
                print("Select refugee's allergy conditions")
                # array of input
                aller_inpts = numerical_input_check(aller_opt)
                # convert numerical input to text
                self.allergy_cond = []
                for v in aller_inpts:
                    self.allergy_cond.append(aller_dict[int(v)])

                for ind2, al in enumerate(self.allergy_cond):
                    if ("Food" in al):
                        self.food_allergy = input(
                            "Please specify the type of food that refugee is allergic to: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                        "("+self.food_allergy+")"
                    elif ("Medication" in al):
                        self.medicine_allergy = input(
                            "Please specify the name of medicine that refugee is allergic to: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                        "("+self.medicine_allergy+")"
                    elif ("Others" in al):
                        self.others_allergy = input(
                            "Please specify other allergies: ")
                        self.allergy_cond[ind2] = self.allergy_cond[ind2] + \
                        "("+self.others_allergy+")"

                self.ref_allergy = ", ".join(self.allergy_cond)
                self.ref_illness[ind] = self.ref_illness[ind] + \
                    "(" + self.ref_allergy + ")"
            if ("Others" in il):
                #  other disease please specify
                print("---------------OTHERS---------------")
                self.other_disc = input(
                    "Please specify other refugee's disease: ")
                self.ref_illness[ind] = self.ref_illness[ind] + \
                    "(" + self.other_disc + ")"
        self.ref_illness = ",".join(self.ref_illness)
        # add illness to row
        self.ref_row.extend([self.ref_illness])

    def refugee_surgery(self):
        print("---------------SECTION 2 : SURGERY--------------")
        self.has_surgery = input(
            "Does refugee has the history of surgery? (Yes/No): ")
        if (self.has_surgery == "Yes"):
            self.surgery = input("Enter refugee's surgery record: ")
        else:
            self.surgery = "None"
        self.ref_row.extend([self.surgery])

    def refugee_smoking(self):
        print("---------------SECTION 3 : SMOKING HABIT--------------")
        self.smoker = input("Does refugee smoke? (Yes/No): ")
        self.ref_row.extend([self.smoker])
    
    def refugee_alcoholic(self):
        print("---------------SECTION 4 : ALCOHOL CONSUMPTION--------------")
        self.is_alcoholic = input("Is refugee an alcoholic? (Yes/No): ")
        # add medical cond to row
        self.ref_row.extend([self.is_alcoholic])

    def add_refugee_to_db(self, refugee_df):
        # refugee dataframe
        self.col_name = list(refugee_df.columns)
        self.ref_ID = list(refugee_df.index)
        ref_length = len(refugee_df.index)
        self.ref_ID.append(int(ref_length))
        self.ref_row.insert(0, ref_length)
        # add refugee status at the back 
        # print("index", self.ref_ID)
        # print("col", self.col_name)
        # print("data", self.ref_row)
        updated_ref_db = pd.DataFrame(
            data=[self.ref_row], columns=self.col_name)
        # print(updated_ref_db)
        # append new data row to refugee.csv
        with open('info_files/refugee.csv', 'a') as f:
            updated_ref_db.to_csv(f, header=False, index=False)

    # FINAL: Registration form
    def refugee_registration_form(self,refugee_df,camp_df):
        # general info
        print("\nREFUGEE'S GENERAL INFORMATION")
        print("-------------------------------------------")
        self.refugee_name(refugee_df)
        self.refugee_birthdate()
        self.refugee_gender()
        self.refugee_race()
        self.refugee_contact()
        self.refugee_family()

        # assign_camp_ID
        print("\n-------------------------------------------")
        print("ASSIGNING CAMP IDENTIFICATION")
        print("-------------------------------------------")
        self.assign_camp_ID(camp_df,"create")

        # medical condition
        print("\n-------------------------------------------")
        print("REFUGEE'S MEDICAL PROFILE")
        print("-------------------------------------------")
        self.refugee_illnesses()
        self.refugee_surgery()
        self.refugee_smoking()
        self.refugee_alcoholic()

        # add to database
        self.add_refugee_to_db(refugee_df)

