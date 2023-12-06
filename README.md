# Group Name - ERL
Members:
- Elysse Samantha T. Beltran (Lead)
- Aldrine Drebb Cristobal
- Lawrence Quinones

# TO-DO
  **[Google sheets task tracker](https://docs.google.com/spreadsheets/d/1GRKTS3OtOthObzVezH7hfzfZaVjWrcyvOWxXkNz77BE/edit?usp=sharing)**
  
   **[Project Specs](https://classroom.google.com/c/NjE5NzM5ODA3MzY3/p/NjM3NDcxMDQwMTE3/details)**
1. Lexical Analyzer - Breaks down a program file into tokens, separating comments and whitespaces.
   **[Lexemes](https://docs.google.com/document/d/1WMG3ybYsAUXqvCtDHWNipT4i9G0zoB1TIA62uGWgPmY/edit?usp=sharing)**
2. Syntax Analyzer
3. Semantic Analysis

## How to use github (Taken from CMSC 128)

### Setup
1. (Optional) On your code editor, make sure you have logged-in your GitHub account.
2. Go to GitHub then Fork the develop branch of the main repository.
3. In your forked repository, click Code then copy the HTTPS or SSH link.
4. Go to your local directory on which you want your codebase to be located.
5. On your terminal, clone your forked repository.
6. git clone <link>

### Commands
- create branch from `develop`
    ```
    git checkout -b NEWBRANCH
    ```
- Displays your current branch.
    ```
    git branch
    ```
- Displays the state of the working directory and the staging area.
    ```
    git status
    ```

### How to pull request
- In your forked repository, `Sync Fork` your develop branch to the develop branch in the main repository.
- Pull the changes in your local machine.
    ```
    git checkout develop
    git pull
    ```
4. Create a branch from develop.
   ```
   git checkout -b NEWBRANCH
   ```
5. Start working on your code inside the newly created branch. Make sure that no changes will be done under the develop branch.

### Publish Code Changes
1. To check the state of your working directory:
   ```
   git status
   ```
2. On your code editor, if you have Git extensions, click `Commit and Push`. Then check the naming convention for commits. Otherwise, proceed to step 3.
3. Else, add your code changes.
   ```
   git add .
   ```
4. Commit your changes in your new branch and include the commit type in your commit message.

   ```
   git commit -m "<insert message>"
   ```

     <details> <summary> IMPORTANT: Commit Naming Convention </summary> 
     <ol>
       <li> feat – a new feature is introduced with the changes </li>
       <li> fix – a bug fix has occurred </li>
       <li> chore – changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies) </li>
       <li> refactor – refactored code that neither fixes a bug nor adds a feature </li>
       <li> docs – updates to documentation such as a the README or other markdown files </li>
     </details>

5. If your branch is not in the origin yet, run:
   ```
   git push --set-upstream origin NEWBRANCH
   ```
6. If your branch is already existing in the origin, push these changes.
   ```
   git push
   ```
### Create Pull Request
  
<details> <summary> Create Pull Request </summary>
  
1. In GitHub, go to your forked repository.
  
2. If there is a prompt for your pushed changes, click `Compare & pull request`. Otherwise, follow step 3.
  
3. Else, click `Contribute` then `Open Pull Request`.
