import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

problems = []

easy_titles = [
    "Two Sum",
    "Valid Parentheses",
    "Merge Sorted Array",
    "Binary Search",
    "Maximum Subarray",
    "Climbing Stairs",
    "Best Time to Buy Stock",
    "Contains Duplicate",
    "Palindrome Number",
    "Roman to Integer",
    "Plus One",
    "Move Zeroes",
    "Remove Duplicates",
    "Intersection of Arrays",
    "Majority Element",
    "Power of Two",
    "Happy Number",
    "Reverse String",
    "Valid Anagram",
    "Missing Number"
]

medium_titles = [
    "Group Anagrams",
    "3Sum",
    "Coin Change",
    "Course Schedule",
    "Search in Rotated Array",
    "Longest Substring",
    "Container With Water",
    "Word Search",
    "Number of Islands",
    "Permutations",
    "Merge Intervals",
    "Subsets",
    "Product Except Self",
    "Rotate Image",
    "Spiral Matrix",
    "House Robber",
    "Decode Ways",
    "Kth Largest Element",
    "Top K Frequent Elements",
    "Partition Labels"
]

hard_titles = [
    "Regular Expression Matching",
    "Median of Two Sorted Arrays",
    "Serialize Binary Tree",
    "N Queens",
    "Edit Distance",
    "Trapping Rain Water",
    "Merge K Lists",
    "Word Ladder",
    "Sudoku Solver",
    "LFU Cache"
]

easy_description = "Solve this problem using arrays, strings, loops, or basic data structures."

medium_description = "Solve this problem using efficient algorithms, recursion, stacks, queues, trees, or dynamic programming."

hard_description = "Solve this advanced problem using optimized algorithms, graphs, dynamic programming, or advanced data structures."

# Generate 200 Easy Problems
for i in range(1, 201):
    title = easy_titles[(i - 1) % len(easy_titles)] + f" {i}"
    problems.append((title, "Easy", easy_description, "Not Solved", "No"))

# Generate 200 Medium Problems
for i in range(1, 201):
    title = medium_titles[(i - 1) % len(medium_titles)] + f" {i}"
    problems.append((title, "Medium", medium_description, "Not Solved", "No"))

# Generate 100 Hard Problems
for i in range(1, 101):
    title = hard_titles[(i - 1) % len(hard_titles)] + f" {i}"
    problems.append((title, "Hard", hard_description, "Not Solved", "No"))

cursor.executemany(
    """
    INSERT INTO problems(title,difficulty,description,status,favorite)
    VALUES(?,?,?,?,?)
    """,
    problems
)

conn.commit()
conn.close()

print("✅ 500 Problems inserted successfully!")