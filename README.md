# emergency-system
This repo is the coursework solution of Team K in module COMP0066 Introductory Programming



# Steps:

## Login:

1. Choose your account type first
   1. admin
      1. Input: ONLY password
      2. To do programs:
         1. 
   2. volunteer
      1. Input from user:
         1. uerName
         2. Password
      2. To do programs
         1. load volunteer info(ALL)

## Admins:

1. Create a new plan
   1. Input from user:
      1. type
      2. description
      3. area
      4. startDate(yyyy-mm-dd)
      5. campNumer(int)
   2. To do by program
      1. Set up the corresponding numer of empty camps  according to the maximum number of camps.
2. Create volunteer account
   1. Input from user:
      1. firstName
      2. lastName
      3. userName
      4. password
      5. choose working shift by day
         1. Morning
         2. Afternoon
         3. Night
      6. choose working day
      7. Choose a CampID for this volunteer
   2. To bo by program
      1. Set accountStatus

## Volunteer:

1. Register a refugee

   1. Input from user:
      1. campID
      2. firstname
      3. lastname
      4. birthdate
      5. gender
      6. ethnic_group
      7. email
      8. phone
      9. num_of_family_members
      10. family_member_name (string)
      11. illnesses
      12. surgery
      13. smoking
      14. alcoholic
      15. status
      16. special_request
          1. task_info
          2. Date(yyyy-mm-dd) (this week only)
          3. Working_shift
          4. options for possible volunteer
   2. To do by program
      1. update volunteer timeSchedule

   index: weekday: Monday to Sunday

   -1: unavailable

   0: free

   23: TaskID

   1. Manage volunteer information
      1. edit
         1. Input from user
            1. column allow to change
               1. Anytime
                  1. fName
                  2. lName
                  3. password
               2. only when the volunteer is able to do this change
                  1. campID
                  2. workingShift
                  3. workingdays
      2. view
         1. view their personal information
         2. view my timeSchedule
            1. fetch current systime compare it with lastLogin
            2. update if needed

   Tips: volunteerID will be read when init the class volunteer, you can visit it by self.volunteerID
