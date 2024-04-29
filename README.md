# ASU PHY 432 Final Project #

For your **Final Project** you have to:

1. fulfill the **objectives** that you defined in your **Proposal**
   (add your `proposal.pdf` to the repository under `docs`);
2. collaborate as a team;
3. use the [Wiki](wiki) to keep a shared "lab notebook" for the project;
4. present the work as a video presentation;
5. individually explain various aspects of the work in a virtual Q&A

For an overview over the requirements see
[docs/final_overview.pdf](docs/final_overview.pdf) and the
deliverables
[docs/final_deliverables.pdf](docs/final_deliverables.pdf) (i.e.,
notes on the Abstract and Video Presentation).

## Team repository
You will be working in your private repository to which only your team
has access. Your instructor will send you a link to automatically set
up this repository (services provided by
[Classroom for GitHub](https://classroom.github.com/)).

Your private team repository will be named **final-2022-TEAMNAME**.



## Directory layout

* `Submission`: Put all the *code* and *data* required to perform the required
   simulations in this directory. When grading, only code in this
   directory will be taken into account.
* `docs`: notes and other documentation (not graded).
* `abstract`: put the **abstract** and **CONTRIBUTIONS.txt** into this directory; you can
   use the template in the directory.
* `Work`: additional code and data that you want to version control
   but that should not be graded.
* `Grade`: instructors/graders can add comments in this directory.
  

## Submission

* Submit **code and data** through your GitHub repository. Make sure that
  [GitHub properly associates your commits with your GitHub username](https://help.github.com/articles/why-are-my-commits-linked-to-the-wrong-user/). Check
  that the *contributions* are properly accounted
  for (the **Contributors** statistics under **Graphs**).
* Commit your **abstract** as `abstract/abstract.txt` and 
* Follow instructions on Canvas for the **video presentation**.


### How To Use
* Input variables that involve both of these (constants c, G, and the mass of the black hole M) are in `inputVariables.py`.
* For the plots of trajectories, run `photonTraj.py`, it will output the figures in the *figures* folder. 
* For the lensing effect with the use of a background galaxy, run `lensing.py`.
	- In this file, the resolution of the image can be changed by changing `y_sizef` and `z_sizef` (both integers). There is a limit though, and it depends on how much your computer can handle; it happens to be 250x250 for mine but if it crashes, making it lower can solve the issue (it has to do with how many bytes you can send to each thread).
	- The frames per second can be changed by editing the `fps` variable. 
	- The number of rendered frames can be edited by changing the `nFrames` variable. Setting it to one will not produce a video, and the output can be found in the *video* folder.
	- There is parallelization for this code, a function from `joblib` called `Parallel` is called near the bottom right before it prints "Frames Done." which has a vairable `n_jobs` which can be changed to be bigger based on number of cores in your CPU. 
		- WARNING: Changing this to -1 will use all but 1, -2 will use all but 2, etc. This in turn can make your computer run very hot and risks the danger of overheating without sufficient cooling!
	- **Waiting Time:** 1 frame at a resolution of 250x250 can take a few minutes to render, (it should not take anywhere more than 15 minutes to render a single frame). A video with 60 frames took my computer a little over 1.5 hours to render (with parallelization, `n_jobs=6`). 
	- Lowering the resolution does make it faster but lowering it too far makes it all black because each pixel is actually a unit of mass (which is the length in our units) so all the trajectories end up getting sucked into the black hole if the resolution is too small. This canbe remedied by lowering the mass of the black hole but a 10x10 pixel image tends to not be particularly useful.
	- If for some reason the script for parallelization does not work, or there are errors popping up with joblib, or the `Parallel` function, comment the line out and replace `def process(f):` with `for f in range(nFrames):`
		- This will remove the parallelization that I had, in which rendering a 250x250 resolution 60 frame video took around 10 hours to make.