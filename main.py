from tasks import random_tasks, intro

# Transactions
MIN = 2
MAX = 5

def main():
    intro()
    random_tasks(MIN, MAX)
    
if __name__ == "__main__":
    main()