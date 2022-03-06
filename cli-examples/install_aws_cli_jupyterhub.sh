#Steps to Install AWS-CLI on JupyetrHub


1. Open JupyterLab and go to the new terminal. Use the curl command to download the installation script. The following command uses the -O (uppercase "O") parameter to specify that the downloaded file is to be stored in the current folder using the same name it has on the remote host.

    curl -O https://bootstrap.pypa.io/get-pip.py

2. Run the script with Python to download and install the latest version of pip and other required support packages.

    python get-pip.py --user

Or use the following.

      python3 get-pip.py --user

When you include the --user switch, the script installs pip to the path ~/.local/bin.

3. Ensure the folder that contains pip is part of your PATH variable.

      a. Find your shell's profile script in your user folder. If you're not sure which shell you have, run echo $SHELL.

      b. Add an export command at the end of your profile script that's similar to the following example.

          export PATH=~/.local/bin:$PATH

4. Now you can test to verify that pip is installed correctly.

          pip3 --version

5. Use pip to install the AWS CLI.

          pip3 install awscli --upgrade --user

6. Verify that the AWS CLI installed correctly.

          aws --version

7. aws configure

Provide the AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID to configure it and you should be all set to use AWS s3 and sync any files from local dirs/files  to AWS s3.

8. Test aws s3 access using aws s3 ls - you should be able to list s3 buckets you have access to.Once this is set up you can use aws s3 cp or aws s3 sync command to copy the data from local dir/files to aws s3 or vice versa.
