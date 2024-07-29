import os

def deletePycache():

    subDirs = ['temp//','avatar//__pycache__//'] #get all needed subdirectories to delete

    for subDir in subDirs:

        if os.path.exists(subDir):

            dirs = os.listdir(subDir) #get all file names in subdirectory
            #print(dir_list)
            for file in dirs:
                os.remove(subDir+file) #delete each file

def createTempDir():

    if not os.path.exists('temp//'):
        os.makedirs('temp//')

if __name__ == '__main__':

    deletePycache()