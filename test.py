from sqliteFunctions import *
with sqlite3.connect('emergency_system.db') as conn:
    c = conn.cursor()
    volunteerIDs = get_all_IDs('volunteer')
    for volunteerID in volunteerIDs:
        c.execute(
            f"UPDATE volunteer set userName = 'volunteer{volunteerID}' where volunteerID = {volunteerID}")
print("Done")
