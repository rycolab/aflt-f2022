# Instructions

1. The first time you accept an assignment you'll have to select your name from the roster (once you select it you won't be able to change it). If your name is not in the list or you have any other problem let us know.
2. Following the github messages, you will end up with a private repo with the same code of the base repo (https://github.com/rycolab/aflt-f2022).
3. You'll have to fill the blanks in the code of your private repo with your implementation. Once you push a new commit to your github repo, the autograder will automatically run the tests. In your private github repo, you'll be able to see the result of the tests in actions> [your last commit name] classroom workflow > jobs > autograding. If the code is correct you'll end up with a green check on the workflow. 
**TIP:** You can also run the tests locally using `pytest`. Ex.: `pytest test_hw1.py`. Usually, it's more readable too.

Notes:
1. Please bear in mind that this is out first time using github classrooms and the autograder, so some issues may arise. For any problem related with the submission of the assignments on github you can use the appropiate rocket channel.
2. You can make as many submissions as you want, only the last commit you push to your repo by the deadline will be taken into account.
3. Every Sunday, a cron job will overwrite any changes to the files not appearing in the ``.templatesyncignore`` file.


## Private repo updates

As we find issues in the base repo that is used as template for your private repos, we will release new updates. The process to update your repos without erasing your work is a bit tricky, so do not hesitate to ask any questions you may have. 

Only (_only_) when we announce an update to the base repo, you'll have to follow the next steps:

1. Go to the _Actions_ tab in your repo
2. On the left, you'll see a list with workflows. Click on ``.github/workflows/template-sync.yml`.
3. You'll see a drop-down meno with the name `Run workflow`. Click on it and then press the green botton with the same name.
4. Once the workflow is finished, a new PR will have been created. Click on it and review the changes. **IMPORTANT**: Merging this PR may overwrite your work! It's not lost by any means because of git, but still, it's annoying. Plase, review that the PR is not overwritten any of your changes to your repo. Then, merge the PR and you'll have the very last version of the base repo.
