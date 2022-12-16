
def refugee_input_option(name):
    """
    This function is used to store the option for refugee registration detailed questions
    :return: string
    """
    match name:
        case 'Gender':
            return (
                '[ 1.] Male\n'
                '[ 2.] Female\n'
                '[ 3.] Transgender\n'
                '[ 4.] Others'
            )
        case 'Ethnic Group':
            return (
                '[ 1.] Asian\n'
                '[ 2.] White\n'
                '[ 3.] Black or African\n'
                '[ 4.] American Indian or Alaska Native\n'
                '[ 5.] Arab\n'
                '[ 6.] Mixed\n'
                '[ 7.] Others'
            )
        case 'Illnesses':
            return (
                '[ 1.] Allergies\n'
                '[ 2.] Cold and flu\n'
                '[ 3.] Diarrhea\n'
                '[ 4.] Headaches\n'
                '[ 5.] Mononucleosis\n'
                '[ 6.] Stomach aches\n'
                '[ 7.] Tuberculosis\n'
                '[ 8.] Stroke\n'
                '[ 9.] Heart disease\n'
                '[10.] Cancer\n'
                '[11.] Diabetes\n'
                "[12.] Alzheimer's disease\n"
                '[13.] Others\n'
                '[14.] None'
            )
        case 'Allergies':
            return (
                '[ 1.] Grass and tree pollen\n'
                '[ 2.] Animal dander\n'
                '[ 3.] Dust mites\n'
                '[ 4.] Latex\n'
                '[ 5.] Food\n'
                '[ 6.] Medication\n'
                '[ 7.] Others\n'
                '[ 8.] None'
            )

        case 'Task Request':
            return (
                '[ 1.] Medical care\n'
                '[ 2.] Psychological consultancy\n'
                '[ 3.] Physiotherapy\n'
                '[ 4.] Repair\n'
                '[ 5.] Translator\n'
                '[ 6.] Lessons'
            )
        case 'Shift Time':
            return (
                '[ 1.] Morning\n'
                '[ 2.] Afternoon\n'
                '[ 3.] Night'
            )
        case 'Edit':
            return (
                '[ 1.] Name\n'
                '[ 2.] Birthdate\n'
                '[ 3.] Gender\n'
                '[ 4.] Ethnic group\n'
                '[ 5.] Contact\n'
                '[ 6.] Family\n'
                '[ 7.] Camp\n'
                '[ 8.] Illnesses\n'
                '[ 9.] Surgery\n'
                '[10.] Smoking\n'
                '[11.] Alcoholic\n'
                '[12.] Request\n'
                '[13.] Exit'
            )


def input_matching(name):
    match name:
        case 'Gender':
            return {1: "Male", 2: "Female", 3: "Transgender", 4: "Others"}
        case 'Ethnic Group':
            return {1: "Asian", 2: "White", 3: "Black or African", 4: "American Indian or Alaska Native",
                    5: "Arab", 6: "Mixed", 7: "Others"}
        case 'Illnesses':
            return {1: "Allergies", 2: "Cold and flu", 3: "Diarrhea", 4: "Headaches", 5: "Mononucleosis",
                    6: "Stomach aches", 7: "Tuberculosis", 8: "Stroke", 9: "Heart disease",
                    10: "Cancer", 11: "Diabetes", 12: "Alzheimer's disease", 13: "Others", 14: "None"}
        case 'Allergies':
            return {1: "Grass and tree pollen", 2: "Animal dander", 3: "Dust mites", 4: "Latex", 5: "Food",
                    6: "Medication", 7: "Others", 8: "None"}
        case 'Task Request':
            return {1: "Medical care", 2: "Psychological consultancy", 3: "Physiotherapy", 4: "Repair", 5: "Translator", 6: "Lessons"}
        case 'Shift Time':
            return {1: "Morning", 2: "Afternoon", 3: "Night"}
        case 'Edit':
            return { 13: ["cancel"], 1: ["fName", "lName"], 2: ["birthdate"], 3: ["gender"], 4: ["ethnicGroup"],
                    5: ["email", "phone"], 6: ["familyMemberName"], 7: ["campID"],
                    8: ["illness"], 9: ["surgery"], 10: ["smoking"], 11: ["alcoholic"], 12: ["request"]}
