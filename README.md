# Multi-Query Content Based Image Retrieval System for Bird Species Identification

## 1. Requirements
- This project requires Python>=3.10.0. You can create a conda environment using the following: \
```conda create -n <env_name> python=3.10.9``` \
and use `conda activate <env_name>` to activate your environment. \
**Please replace `<env_name>` with your preferred name for the environment.**

- Next, install Node.js and npm in your environment. You can refer to this [link](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) for installing npm and Node.js.\
We are using Node version `v16.20.2` and npm version `8.19.4`.\
If you are using MacOS or Linux, you can use Homebrew to install by running the following:\
`brew install node@16` 

- Run `python setup.py` to install required pakages.

## 2. Download dataset
- The dataset is avaliable at [Google Drive](https://drive.google.com/file/d/1dQx1cwO4W0WVYcnzGB1ftxEcwiQaFv90/view?usp=sharing). Note there are many folders and files inside,
  but we only need to use the `CUB_200_2011/images` folder. The hierarchy of the dataset is shown below:
  ```
   ${CUB_200_2011 ROOT}
    -- attributes.txt
    -- CUB_200_2011
        |-- images
        |-- attributes
        ...
   ```
- Put the `images` folder into the project directory as follows:
  ```
   ${Multimedia2024 ROOT}
    -- flask_web
        |-- vue_frontend
            |-- public
                |-- data
                    |-- images
    ...
    
   ```
  

## 3. Run the app
- First go to `flask-web/vue-frontend`, run `npm install` in a ternimal or powershell. \
  After installation, run `npm run serve`. \
  You should see a message that the app is running at local host. Copy the local url to a clipboard. You will need it later.
- In a new ternimal or powershell, direct to `flask-web/backend`. Run `python app.py`. After the server started successfully, open the url you copied in your web browser. Now you can see the running web app.
- You can upload to 5 images at once. After the images are uploaded successfully, click the search button and be patient. **Note that the initial search would take longer as the model needs to be initialized.**
- If you want to start a new search, click on refresh or refresh your browser. This will delete your previously uploaded files.

