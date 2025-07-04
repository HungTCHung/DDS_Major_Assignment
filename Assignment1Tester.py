#
# Tester for the assignement1
#
DATABASE_NAME = 'ddb_assignment1'
from pathlib import Path
current_dir = Path(__file__).parent
print(f"Current directory: {current_dir}")
file_path = current_dir /"ml-10M100K"/"ratings.dat"
print(f"File path: {file_path}")

RATINGS_TABLE = 'ratings'
RANGE_TABLE_PREFIX = 'range_part'
RROBIN_TABLE_PREFIX = 'rrobin_part'
USER_ID_COLNAME = 'userid'
MOVIE_ID_COLNAME = 'movieid'
RATING_COLNAME = 'rating'
INPUT_FILE_PATH = file_path
ACTUAL_ROWS_IN_INPUT_FILE = 220 #nmber of lines in the input file

import psycopg2
import traceback
import testHelper
import Interface as MyAssignment

if __name__ == '__main__':
    try:
        testHelper.createdb(DATABASE_NAME)
       
        with testHelper.getopenconnection(dbname=DATABASE_NAME) as conn:
          
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
            testHelper.deleteAllPublicTables(conn)
            
            print("\nTesting loadratings function") 
            [result, e] = testHelper.testloadratings(MyAssignment, RATINGS_TABLE, INPUT_FILE_PATH, conn, ACTUAL_ROWS_IN_INPUT_FILE)
            if result :
                print("loadratings function pass!")
            else:
                print("loadratings function fail!")
      
            print("\nTesting rangepartition functions")
            [result, e] = testHelper.testrangepartition(MyAssignment, RATINGS_TABLE, 5, conn, 0, ACTUAL_ROWS_IN_INPUT_FILE)
            if result :
                print("rangepartition function pass!")
            else:
                print("rangepartition function fail!")
           
            # ALERT:: Use only one at a time i.e. uncomment only one line at a time and run the script
            [result, e] = testHelper.testrangeinsert(MyAssignment, RATINGS_TABLE, 100, 2, 3, conn, '2')
            # [result, e] = testHelper.testrangeinsert(MyAssignment, RATINGS_TABLE, 100, 2, 0, conn, '0')
            if result:
                print("rangeinsert function pass!")
            else:
                print("rangeinsert function fail!")

            testHelper.deleteAllPublicTables(conn)
            
            print("\nTesting roundrobinpartition functions")
            MyAssignment.loadratings(RATINGS_TABLE, INPUT_FILE_PATH, conn)
            
            [result, e] = testHelper.testroundrobinpartition(MyAssignment, RATINGS_TABLE, 5, conn, 0, ACTUAL_ROWS_IN_INPUT_FILE)
            if result :
                print("roundrobinpartition function pass!")
            else:
                print("roundrobinpartition function fail")

            # ALERT:: Change the partition index according to your testing sequence.
            [result, e] = testHelper.testroundrobininsert(MyAssignment, RATINGS_TABLE, 100, 1, 3, conn, '0')
            # [result, e] = testHelper.testroundrobininsert(MyAssignment, RATINGS_TABLE, 100, 1, 3, conn, '1')
            # [result, e] = testHelper.testroundrobininsert(MyAssignment, RATINGS_TABLE, 100, 1, 3, conn, '2')
            if result :
                print("roundrobininsert function pass!")
            else:
                print("roundrobininsert function fail!")

            choice = input('Press "y" to Delete all tables? ')
            if choice == 'y':
                testHelper.deleteAllPublicTables(conn)
            if not conn.close:
                conn.close()

    except Exception as detail:
        traceback.print_exc()