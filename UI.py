import tkinter as tk

import display


import Algos
from Algos import most_related_uploader as mru
from Algos import most_related_category as mrc
from Algos import most_related_forVideo as mrfv
from Algos import common_category_overlap as cco
from Algos import common_category_overlap as cco
from Algos import query as qry
from Algos import queryrelation as qryrel

#DO NOT TOUCH THESE TWO LINES
# these two HAVE to be above everything else, except for the import statements
main = tk.Tk()
main.geometry('500x500')

#might want to consider importing things instead of copying all
#the queries and such over here

#and dont touch this either!
executeQuery = tk.BooleanVar()
def execute():
    global executeQuery
    if executeQuery.get() == False:
        executeQuery.set(True)
    else:
        executeQuery.set(False)

def query1():
    global executeQuery
    print("instructions label setting")
    instructionLabel.config(text= "please enter number 1")
    executeButton.wait_variable(executeQuery)
    num1 = int(userEntry.get())
    instructionLabel.config(text= "please enter number 2")
    executeButton.wait_variable(executeQuery)
    num2 = int(userEntry.get())

    print(num1)
    print(num2)
    outputLabel.config(text = str(num1) + " " + str(num2))

def most_recommended_category_for_video_query():
    global executeQuery
    print("instructions label setting")
    instructionLabel.config(text= "Please enter video ID")
    executeButton.wait_variable(executeQuery)
    vidID = (userEntry.get())
    
    print(vidID)
    category = mrfv.ui_run(vidID)
    category = category[0]
    outputLabel.config(text = "The most recommended category for video: " +  vidID + " is " + category)

def most_recommended_uploader_query():
    global executeQuery
    print("Running query")
    uploader = mru.ui_run()
    outputLabel.config(text = "The most recommended uploader is " + uploader)

def most_commonly_overlapping_categories_query():
    global executeQuery
    print("Running query")
    catA, catB = cco.ui_run()
    catA = catA[0]
    catB = catB[0]
    outputLabel.config(text = "The two most frequently recommended together categories are " + catA + " and " + catB)

def most_recommended_category_query():
    global executeQuery
    print("Running query")
    category = mrc.ui_run()
    category = category[0]
    outputLabel.config(text = "The most recommended category is " + category)
    
def topXViewedVideos():
    global executeQuery
    instructionLabel.config(text= "How many?")
    executeButton.wait_variable(executeQuery)
    num1 = int(userEntry.get())

    result = "" #mostViews.topXVideos(num1)
    outputLabel.config(text = result)

def query():
    global executeQuery
    instructionLabel.config(text= "What's the videoID?")
    executeButton.wait_variable(executeQuery)
    vidID = str(userEntry.get())

    result = str(qry.ui_run(video_id=vidID))

    outputLabel.config(text = result)

#array of buttons for easy grid making
buttonsArray = []
#add buttons here in this format, set command to correct function
topRecommendedVbutton = tk.Button(main, text = 'Top Recommended Videos', command = query1)
buttonsArray.append(topRecommendedVbutton)

topCategoriesButton = tk.Button(main, text = 'Top Categories', command = query1)
buttonsArray.append(topCategoriesButton)

topRecommendedCategoriesButton = tk.Button(main, text = 'Top Recommended Categories', command = query1)
buttonsArray.append(topRecommendedCategoriesButton)

topRelatedCategoryButton = tk.Button(main, text = 'Top Related Category', command = query1)
buttonsArray.append(topRelatedCategoryButton)

topCategoriesButton = tk.Button(main, text = 'Top Categories', command = query1)
buttonsArray.append(topCategoriesButton)

mostRecommendedCategoryButton = tk.Button(main, text = 'Most Recommended Category', command = query1)
mostRecommendedCategoryButton = tk.Button(main, text = 'Most Recommended Category', command = most_recommended_category_query)
buttonsArray.append(mostRecommendedCategoryButton)

mostRecommendedUploaderButton = tk.Button(main, text = 'Most Recommended Uploader', command = most_recommended_uploader_query)
buttonsArray.append(mostRecommendedUploaderButton)

topViewedVideosButton = tk.Button(main, text = 'Top Viewed Videos', command = query1)
topViewedVideosButton = tk.Button(main, text = 'Top Viewed Videos', command = topXViewedVideos)
buttonsArray.append(topViewedVideosButton)

topViewedVideosCategoryButton = tk.Button(main, text = 'Top Viewed Video in Category', command = query1)
buttonsArray.append(topViewedVideosCategoryButton)

topViewedCategoriesButton = tk.Button(main, text = 'Top Viewed Categories', command = query1)
buttonsArray.append(topViewedCategoriesButton)

mostRecommendedCatFromVidButton = tk.Button(main, text = 'Top Recommended Category from Video', command = query1)
buttonsArray.append(mostRecommendedCatFromVidButton)

mostCommonMutualRecCatButton = tk.Button(main, text = 'Top Most Common Mutually Recommended Category', command = query1)
buttonsArray.append(mostCommonMutualRecCatButton)

most_commonly_overlappingButton = tk.Button(main, text = "Top two categories which are recommended together the most", command = most_commonly_overlapping_categories_query)
buttonsArray.append(most_commonly_overlappingButton)

most_recommended_cat_for_video_button = tk.Button(main, text = "Most Recommended Category for a VideoID", command=most_recommended_category_for_video_query)
buttonsArray.append(most_recommended_cat_for_video_button)


query_video_button = tk.Button(main, text = "Query VideoID", command=query)
buttonsArray.append(query_video_button)



#after making all the buttons, this will add them

i = 0
for button in buttonsArray:
    button.grid(row = i, column = 0)
    i = i + 1

#labels for instructions and text box for entry
instructionLabel = tk.Label(main, text = "Instructions:")
userEntry = tk.Entry(main)
instructionLabel.grid(row = i, column = 0)
userEntry.grid(row = i + 1, column = 0)
executeButton = tk.Button(main, text = "Submit", command = execute)
executeButton.grid(row = i+2, column = 0)

#outputs go on the right! column 2
outputLabel = tk.Label(main, text = "temp")
outputLabel.grid(row= 0, column = 2)

main.mainloop()