import tkinter as tk
main = tk.Tk()
main.geometry('500x500')

#Dont touch this!
#also, might want to consider importing things instead of copying all
#the queries and such over here
executeQuery = tk.BooleanVar()
def execute():
    global executeQuery
    if executeQuery.get() == False:
        executeQuery.set(True)
    else:
        executeQuery.set(False)

#add handlers for events here, do entry as shown in example.
# Stick your query outputs in the query output text widget.
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
buttonsArray.append(mostRecommendedCategoryButton)

mostRecommendedUploaderButton = tk.Button(main, text = 'Most Recommended Uploader', command = query1)
buttonsArray.append(mostRecommendedUploaderButton)

topViewedVideosButton = tk.Button(main, text = 'Top Viewed Videos', command = query1)
buttonsArray.append(topViewedVideosButton)

topViewedVideosCategoryButton = tk.Button(main, text = 'Top Viewed Video in Category', command = query1)
buttonsArray.append(topViewedVideosCategoryButton)

topViewedCategoriesButton = tk.Button(main, text = 'Top Viewed Categories', command = query1)
buttonsArray.append(topViewedCategoriesButton)



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