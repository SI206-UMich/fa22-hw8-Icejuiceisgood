import matplotlib
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import pandas as pd
# Homework done by Rish Verma
# 12/5/22

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    conn = sqlite3.connect(db_filename)
    cur=conn.cursor()
    cur.execute("Select r.name, c.category, b.building, r.rating from restaurants r join buildings b on r.building_id=b.id join categories c on c.id=r.category_id")
    listing=[]
    for row in cur:
        diction={}
        diction["name"]=row[0]
        diction["category"]= row[1]
        diction["building"]=row[2]
        diction["rating"]=row[3]
        listing.append(diction)
    return listing
    pass

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    conn = sqlite3.connect(db_filename)
    cur=conn.cursor()
    cur.execute("Select c.category, count(r.id) from categories c join restaurants r on c.id=r.category_id group by c.category")
    diction={}
    categories=[]
    counts=[]
    for row in cur:
        diction[row[0]]=row[1]
        categories.append(row[0])
        counts.append(row[1])
    plt.figure(1, figsize=(20,3))
    matplotlib.rcParams.update({'font.size': 6})
    plt.bar(categories,counts)
    plt.show()
    return diction
    pass

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    conn = sqlite3.connect(db_filename)
    cur=conn.cursor()
    cur.execute("Select c.category, avg(r.rating) from categories c join restaurants r on c.id=r.category_id group by c.category")
    categories=[]
    avgRatings=[]
    diction={}
    for row in cur:
        diction[row[0]]=row[1]
    sortedRatings=sorted(diction.items(), key=lambda x: x[1], reverse=True)
    for nameRate in sortedRatings:
        name,rate=nameRate
        categories.append(name)
        avgRatings.append(rate)
    plt.figure(2, figsize=(20,3))
    df = pd.DataFrame({"Categories":categories, "Average Ratings":avgRatings})
    df_sorted= df.sort_values('Average Ratings', ascending=False)
    matplotlib.rcParams.update({'font.size': 6})
    plt.bar("Categories","Average Ratings",data=df_sorted)
    plt.xlabel("Categories", size=15)
    plt.ylabel("Average Ratings", size=15)
    plt.show()

    return sortedRatings[0]

    

    pass

#Try calling your functions here
def main():
    print(get_restaurant_data('South_U_Restaurants.db'))
    print()
    print(barchart_restaurant_categories('South_U_Restaurants.db'))
    print()
    print(highest_rated_category('South_U_Restaurants.db'))
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
