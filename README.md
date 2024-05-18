# gcloud-cli-tools
- Using GCloud CLI for doing very basic things with the Google Compute Engine / VMs, such as listing, stopping, and starting them. 
- Very simple and kinda hacky python scripts for doing said basic things.

The proper things to do and use (in python) are discussed here: `https://github.com/googleapis/python-compute`. What's below is useful if you want to get on with things in under 2.5 minutes instead of in, like, under 10 minutes (4x speedup!). 

## Setup 
### 1. Install the Google Cloud SDK.

Download [here](https://cloud.google.com/sdk/docs/install) and follow the instructions.

For me, it was as simple as downloading the tar file appropriate for my system, and then running `source install.sh` in the unpacked directory. I went with the default installation options.

Verify installation by running `gcloud --version`

### 2. Sign in to Google Cloud

Run `gcloud auth login`, which opens a browser window where you log into your Google Cloud account.

### 3. Configure defaults

#### 3.1. Set default project 
  `gcloud config set project [PROJECT_ID]`

  Google Cloud has a concept of "Organization" and the organization has "Projects". 
  
  If you are setting this up independently, the organization and project will be things you create when you are setting up your google cloud account. 
  
  If you are already using google cloud, the active project ID is displayed in the drop down menu with the three-dot symbol in the top left of the browser window, right next to the "Google Cloud" logo. 

#### 3.2. Set default compute zone
  `gcloud config set compute/zone [COMPUTE_ZONE]`

  Google Cloud provides compute resources in different geographical zones with names like `us-east1-b`. 
  
  These zones differ in their pricing, resource availability and offerings, as well as latency. For some resources (like most GPU boxes) it is necessary to ask for "quota," which requires you to get in touch with sales. 

You can verify your default configuration by looking at the config file at `~/.config/gcloud/configurations/config_default`. For me it looks like this:

    >> cat ~/.config/gcloud/configurations/config_default
      [core]
      account = <GCLOUD-ACCOUNT-EMAIL>
      project = <PROJECT_ID>
      
      [compute]
      zone = <DEFAUlT_ZONE>  

## Controlling Google Cloud Compute Engine VMs with CLI
Try typing `gcloud compute instances` and it should give you a very useful list of things you can do from here.

### 1. Create a new instance

I won't describe that here for now, and it can be done in the browser, of course. There are a lot of options and decisions. There's also the possibility of expensive mistakes like inadvertently launching a bunch of instances that by accident and not realizing it.

### 2. Check existing instances
  `gcloud compute instances list`

Should return a list of instances on your project. Note the status! You may be paying for things. To get the instance information you can do:

`gcloud compute instances describe [INSTANCE_NAME]`

If you need to disambiguate by zone, you can do that by adding the `--zone=[COMPUTE_ZONE]` flag. The command will print basically any of the information that you can find in the browser, from disk size to linked SSH keys and so on. 

### 3. Starting and Stopping an existing instance

Starting:
  `gcloud compute instances start [INSTANCE_NAME]`
  
Stopping:
  `gcloud compute instances stop [INSTANCE_NAME]`


