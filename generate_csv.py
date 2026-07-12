import csv

problems = [
    ("Two Sum", "Easy", "Find two numbers that add up to the target."),
    ("Palindrome Number", "Easy", "Check whether a number is a palindrome."),
    ("Roman to Integer", "Easy", "Convert a Roman numeral to an integer."),
    ("Longest Common Prefix", "Easy", "Find the longest common prefix."),
    ("Valid Parentheses", "Easy", "Check if brackets are balanced."),
    ("Merge Two Sorted Lists", "Easy", "Merge two sorted linked lists."),
    ("Remove Duplicates from Sorted Array", "Easy", "Remove duplicates from a sorted array."),
    ("Binary Search", "Easy", "Search in a sorted array."),
    ("Maximum Subarray", "Easy", "Find the maximum sum subarray."),
    ("Climbing Stairs", "Easy", "Count the number of ways to climb stairs.")
]

with open("data/problems.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["title", "difficulty", "description"])

    for problem in problems:
        writer.writerow(problem)

print("CSV file created successfully!")