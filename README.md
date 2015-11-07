# alphaBot

Farming bot for the game **Alpha Wars** (http://eng.alphawars.com/)

<p align="center">
  <a href="http://www.youtube.com/watch?feature=player_embedded&v=YuqQ8hFBmiE" target="_blank"><img src="http://img.youtube.com/vi/YuqQ8hFBmiE/0.jpg" alt="alphaBot demo" width="240" height="180" border="10" /></a>
</p>

# Introduction
(Not important for running **alphaBot**)

In my last exam period, I was searching for a simple browser game that can be played without to much
intellectual effort. Something for the evenings after exhausting days of learning. 
One of my attempts was **Alpha Wars**. A game in which you must produce raw materials to update
your buildings and create an army. It seems that the whole purpose of this game is to wage war against other
players and there is no room left for players that prefer to build and collect. Thus it became boring to me very fast.
Additionally it turned out that the game follows the **Pay2Win** principle what makes it very hard
for me to like that game at all. 
Something that aroused my curiosity was the captcha system of the game. To prevent the usage of 
bots ( ;) ), you need to click on a captcha every time you produce a raw material. The captcha
consists of a number of simple geometric objects, mostly triangles and a single rectangle. To solve the
captcha, you need to identify and click on that single rectangle. Then you can produce a raw material for exactly one
minute. If you want to produce longer than a minute, you need **Titanium**. This can be bought
or created by transforming fuel. But the transformation is very expensive and the costs increases with every executed
conversion. To become a serious threat to your opponents you need to buy ***Titanium*** for money, otherwise
you spend whole days by clicking every minute on a capture.

<p align="center">
  <img src="https://raw.githubusercontent.com/highkite/alphaBot/master/documentation/Captcha_example.png"><br>
  Example of an <b>Alpha Wars</b> captcha.
</p>


Clicking on a rectangle. Seems to be a very simple task, even for a computer. My plan was to take
a screenshot and do some image processing. I always searched for a project where I could use image
processing, because I was eager to learn the skill. Thus it was a great opportunity. My first approach
was very optimistic. I thought one hour for a python script and my computer solves the captchas
for me. Yeah... one hour became five hours and five hours became a couple of days. Mostly spent
with optimizing the algorithms and the assessment parameters.

My first approach was to apply a corner detector and cluster the detected corner points. A problem of this approach
is that the number of clusters is not fixed. Sometimes there are up to four different geometric
objects, but on other occasions there is only one single rectangle. So I needed to cluster for
k = {1,...,4}. This provided a big pile of clusters and I needed a rating function that founds
the best fitting (and hopefully the correct) cluster. My plan was to determine the
convex hull of a cluster and then compare the points within the hull with the points that are
part of the convex hull itself. This alone was very inacurate and I decided to consider also
the angles between adjacent lines of the convex hull. My plan was to analyse every possible
clustering and define its rating according to the number of right corners (+/- an epsilon) in
the convex hull.
Actually, the algorithm worked... kind of. The hit rate was ***4/7*** that means: for ***7*** clicks the algorithm
hit the rectangle in ***4*** cases.
It seems not very good but if you do not have to stand beside your computer it is acceptable.
However, it turned out, that the game has an additional bot protection. If you click on the wrong object 
to often, you will be logged off eventually. The number of wrong clicks  until you are logged off is adaptive. 
There is a point where you will be logged off every time you hit the wrong object. 

Thus I needed to increase the accuracy of the algorithm. But this was impossible by using the
corner detector, because I found no way to increase the quality of feature points on a
representable set of different captchas. It worked only for a few of them, while the results on 
the remaining worsened.
The solution was already part of my thoughts, but until now I was to lazy to implement this idea:
I had to analyse the lines in the image. I read some papers and found a simple and fast line
finding algorithm. It is implemented in a separate library (https://github.com/highkite/lineFinding),
because I am going to use it in several projects.
The line finding algorithm was the answer to everything. Now the algorithm achieves a nearly perfect
hit rate. And at last I am able to finish the chapter **Alpha Wars**.

Consider the following as my share in fighting the **Pay2Win** philosophy ;).

# Installation

To install the **alphaBot** software you need to install the following packages first:

1. matplotlib
2. autopy
3. skimage
4. numpy
5. scipy

You can install them separately or by using pip and the **requirement.txt** file:

```
pip install -r requirements.txt
```

**alphaBot** is based on the **lineFinding** algorithm from here: https://github.com/highkite/lineFinding. 
Clone the repository and make sure that it is in the same directory as the **alphaBot** directory.
That means you should have a folder with at least two directories in it: **lineFinding** and **alphaBot**.

## A reasonable remark

I used an **ubuntu** linux system. I never tested it on **Windows**. I am not sure if it works correctly on windows.
Especially the mouse positioning and the screenshot library might cause problems.

# Usage

The usage of **alphaBot** is very simple. Almost everything you need to do is displayed in the console. However, in the
following I provide a stepwise instruction:

1. Open a console and type ```python alphaBot.py```.
2. Log in to the browser game and make sure that your whole base is visible in the window.
3. Press **Enter** in the command line and move the mouse pointer in the browser window. Wait until the Spinner disappears.
4. **alphaBot** is initialized now.
5. Press enter and move the mouse pointer in the browser window again.
6. **alphaBot** will farm fuel for you.
7. You can stop **alphaBot** by pressing **ctrl + c**.

