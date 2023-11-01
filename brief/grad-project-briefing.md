## The project

The project is designed to give you some exposure working on end-to-end machine learning projects. You will be working with real data
to predict the probability of delay for a given flight departing from Arturo Merino Benitez International (SCL) Airport.

You will need to explore the data, train, evaluate, and select a suitable machine learning model, and create a production grade
scalable API for serving the model.

### The data

The dataset provided is real public data. Below is a description of the dataset:

| Column      | Description                                     |
|-------------|-------------------------------------------------|
| `Fecha-I`   | Scheduled date and time of the flight.          |
| `Vlo-I`     | Scheduled flight number.                        |
| `Ori-I`     | Programmed origin city code.                    |
| `Des-I`     | Programmed destination city code.               |
| `Emp-I`     | Scheduled flight airline code.                  |
| `Fecha-O`   | Date and time of flight operation.              |
| `Vlo-O`     | Flight operation number of the flight.          |
| `Ori-O`     | Operation origin city code.                     |
| `Des-O`     | Operation destination city code.                |
| `Emp-O`     | Airline code of the operated flight.            |
| `DIA`       | Day of the month of flight operation.           |
| `MES`       | Number of the month of operation of the flight. |
| `AÑO`       | Year of flight operation.                       |
| `DIANOM`    | Day of the week of flight operation.            |
| `TIPOVUELO` | Type of flight, I =International, N =National.  |
| `OPERA`     | Name of the airline that operates.              |
| `SIGLAORI`  | Name city of origin.                            |
| `SIGLADES`  | Destination city name.                          |


### The task

There are five components to this task.

1. Learn about and understand the data (exploratory data analysis).
2. Build a suitable machine learning model to predict the probability of delay for a flight taking off or landing at SCL
   airport.
3. Create a production ready implementation of your chosen model.
4. Create a production grade REST API that meets the specification in the [API Definition section](#api-definition).
   1. The API should be fully documented.
5. Implement a suitable CI/CD pipeline using GitHub Actions.


#### API Definition

The production grade API should provide an interface for training/managing models and generating predictions. It should support the following operations
1. `POST /models` should start a new training job with the specified dataset and settings (where appropriate).
   - You may assume that the data is a file or folder in the local environment.
   - The endpoint should not wait for training to finish but instead return a model identifier and a status.
2. `GET /models/{model_id}?export=true` should return the status of the model and save the model if the `export` query parameter is provided.
3. `DELETE /models/{model_id}` should delete the model with the specified ID.
4. `PUT /deploy?model-id={model_id}` should deploy the model with the specified ID only if the status of the model is `completed`, otherwise it should return an appropriate error.
5. `POST /predict` should generate predictions for the specified flights.


##### Example inputs/outputs

###### POST /models

When first creating a model, the endpoint should immediately return a `pending` status.

```json
{
    "id": "a1d42628-c4dd-402a-8dcd-30de1f18e3e4",
    "status": "pending"
}
```

You may assume that models only need to be stored for the duration of the current process, meaning that models can be managed
through a non-persistent in-memory data store. [REST API workshop](https://github.com/james-zafar/restapi-workshop#accessing-the-modelstore)
contains an example of this that you may find useful.

If you have additional time, you should also support downloading and training CSV data from a public Google Drive file or folder.


###### GET /models/{model_id}?export=True&file-name=pathToFile

This should return the current status of the specified model. The status should be `completed` if the model is ready, 
or `failed` if the training job failed. For this task it is not necessary to implement multi-threading/processing to run
training jobs, so you may omit the `in progress` status and run the training jobs in the same process as the API immediately 
after returning a status from the `POST` request.

```json
{
    "id": "a1d42628-c4dd-402a-8dcd-30de1f18e3e4",
    "status": "completed"
}
```

The query parameter `export` should be optional and `false` by default.

The query parameter `file-name` is not required, but if provided should replace the default model name.

If `export` is set to true and `file-name` is provided, then the model with the corresponding `model_id` should be saved to
the location specified in the `file-name` parameter. For simplicity, you may assume that the `file-name` is a location on the local file
system that is writable. If `file-name` is not provided but `export` is set to `true` then the model should be saved to
the current working directory using the `model_id` as the filename.

If the model was successfully exported, the response should contain an additional key in the response indicating the model has been exported. For example:

```json
{
    "id": "a1d42628-c4dd-402a-8dcd-30de1f18e3e4",
    "status": "completed",
    "download": "OK"
}
```

You may choose to provide a link to download the file and return a `302` response that downloads the model from the specified URL
to support running the API on remote servers and downloading to the client's local file system.

###### DELETE /models/{model_id}

If the specified `model_id` corresponds to a known model then return an empty response with a 204 status.
The endpoint should also produce a 500 response for 0.5% of requests.


###### PUT /deploy?model-id={model_id}

For simplicity, you should store a reference to the "deployed" model as a global constant through the API state. When
`{model_id}` is a valid model, this endpoint should return an empty 204 response after updating the constant to refer to the
specified model to indicate that it has been deployed.

To deploy a model the caller must provide a valid API key in the headers using the key `X-api-key`. You may hard code a validate api key
and the API should return a `401` or `403` when the specified key is either unrecognized or does not have permission to deploy models.


###### POST /predictions

The endpoint should return a 200 response with the generated predictions.

##### Can we change the schema, methods, and/or responses for some or all of the endpoints?

Yes. The above are examples and you may choose to change any aspect of the API as you deem it necessary but the functionality must be the same.
For example may choose to include an additional endpoint, or extra information in the response to an existing endpoint to provide
information about a completed model to help users determine if it is better than the current model based on the evaluation metrics you compute after training.

#### What are we expected to produce for each task?

It is up to you to decide what is an appropriate deliverable for each task. Any research and development discussions for
the first two tasks should be well documented and if you train and evaluate multiple models, then you should keep the model
and evaluation code for each model for discussion later.


### What technologies can we use?

You may use any languages, libraries, and frameworks that you wish, although it is highly recommended that you use GitHub Actions for CI/CD.

The project must be hosted on public GitHub (https://github.com) and all team members should be admins of the repository. 
It is up to you whether you choose to make the repository public or private. It must not be published as part of a GitHub organisation.


### Project organisation

You are free to self-organise the team however you want. You do not need to follow any specific "agile" framework or other
project organisation manifesto unless you deem it fit.


### What is the deadline?

There is no specific deadline for this project. You should aim to have a fully tested, presentable solution by October 27th 2023,
but we *may* choose to extend the project if necessary.

### How will the project be reviewed?

We will aim to schedule weekly reviews to check the progress of the project, and have a project retrospective where we will review
the solution, approach, and ways of working together to review what you have learnt and what you could improve going forward.

During the review we may discuss the following topics:

1. Your choice of model
2. The API and system design/documentation
3. The project setup/ways of working
4. Future design improvements and issues with the current solution
5. The code quality tools you have chosen to use in your DevOps pipeline
6. A code review looking at the functionality, quality, and testing of the production ready components


### Do you have resources that may help us learn more about Python and ML?

- If you'd like to learn more about the theory behind type annotations in Python, I'd recommend checking out [PEP483](https://peps.python.org/pep-0483/) 💪
- To learn more about typing annotations in Python check out [PEP484](https://peps.python.org/pep-0484/) and the [MyPy getting started page](https://mypy.readthedocs.io/en/stable/getting_started.html) 😍
- For those new to sklearn, considering checking out the sklearn [tutorials](https://scikit-learn.org/stable/tutorial/index.html) 🍁
- The [Understanding GitHub Actions Workflow File](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions#understanding-the-workflow-file) 
part of the Actions documentation provides an in depth overview of GitHub Actions Workflow files 🧐
- If you're interested in learning more about best practises in ML, check out [Google's "Rules of Machine Learning"](https://developers.google.com/machine-learning/guides/rules-of-ml) 🥳
- For this project you may wish to use one of the official GitHub Actions templates as a base, such as this [Python App template](https://github.com/actions/starter-workflows/blob/main/ci/python-app.yml) 👀
- A great general purpose resource for learning more about specific AI topics is [ai.google](https://ai.google/build/machine-learning/) 🤩
- [Made with ML](https://madewithml.com/#foundations) is another great tool for learning about various AI and ML Engineering/ML Software Engineering topics 🎃
- If you're somehow not bored of uni style lectures and want to attend some more then [MIT's Introduction to Machine Learning](https://openlearninglibrary.mit.edu/courses/course-v1:MITx+6.036+1T2019/course/) is great (or so I'm told)... 🥱
- For those new to machine learning, you may want to check out [Microsoft's AI For Beginners course](https://microsoft.github.io/AI-For-Beginners/) 🎊
- The slides presented during the introduction to REST APIs are [here](https://docs.google.com/presentation/d/1sHFFUFe402n1tTypRAw3BnaHHKQHdA4isS0Cvncb3-Q/edit#slide=id.p) 🎄
- The REST API workshop which includes a complete example OpenAPI doc can be found [here](https://github.com/james-zafar/restapi-workshop) and the solution is [here](https://github.com/james-zafar/restapi-workshop-solution) 🎉
- Finally, for those busy planning their next vacation, consider checking out [New York Times' 52 places to travel in 2023](https://www.nytimes.com/interactive/2023/travel/52-places-travel-2023.html) 🇨🇦 🇲🇽 🇦🇺 🇬🇧 🇨🇱 🇨🇳 🇪🇸

#### I've never used Git or GitHub, will this be a problem?

No, you should be fine with a basic understanding of Git. Below is a brief summary of some of the commands you'll likely need, 
but there are many other great tutorials available online should you get stuck.

- `git init <directory>` creates a new git repository in the specified directory, or if directory is omitted a new repo will
be created in the current working directory.
- Use `git add <files>` stages the specified files (or directory) for the next commit.
- `git commit -m <message>` commits anything in the staging area with the specified message.
- To amend the commit message use `git commit --amend`. If there are other changes in the staged area this will create add
any changes from the staged area to the previous commit.
- To push a commit to the remote run `git push`. If you are pushing to a new branch you may need to set a remote tracking branch
by running `git push --set-upstream origin <your-branch-name>` first.
- To fetch the remote version of a branch and merge it into your copy run `git pull`.
- To see a list of all staged, unstaged, and untracked changes use `git status`.
- Use `git branch` to see a list of branches, as well as the branch you are currently on.
- `git checkout -b <branch>` can be used to checkout an existing branch, or to create a new branch with the specified name when used with the `-b` flag.
- To merge another branch into the current branch use `git merge`.
- Occasionally you may need to fetch branches from the remote before running the `checkout` command. To do this use `git fetch --all`.
- `git reset` discards any changes in the staging area to match the most recent commit. 
To overwrite all changes in the current directory use `git reset --hard`.
- To discard all local changes (excluding untracked files) you can use `git checkout -- .`. The `--` is an explicit way of stating 
that you are not specifying a branch name and the `.` will checkout the head of the current branch.
