[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

# Better highlighting


### Usage:
This tool is designed for beautiful text formatting in the terminal. It is highly specialized, prints in terminal highlighted text 
in more readable form. 
It also can render 'pretty' table and python's iterators syntax.

### Example:
<img src="https://user-images.githubusercontent.com/21011049/160372378-32acc15e-1cfa-4987-bce7-6dfd34ec3ab2.png"></img> 

### Text styles
<table>
<th>Styles</th>
<tr><td>ansiblack</td></tr>
<tr><td>bold</td></tr>
<tr><td>italic</td></tr>
<tr><td>underline</td></tr>
</table>


### Colors
Colors specified using ansi* are converted to a default set of RGB colors when used with formatters other than the terminal-256 formatter.

By definition of ANSI, the following colors are considered “light” colors, and will be rendered by most terminals as bold:

* “brightblack” (darkgrey), “brightred”, “brightgreen”, “brightyellow”, “brightblue”, “brightmagenta”, “brightcyan”, “white”

The following are considered “dark” colors and will be rendered as non-bold:

* “black”, “red”, “green”, “yellow”, “blue”, “magenta”, “cyan”, “gray”

<table>
<th>Color names</th>
<tr><td>ansiblack</td></tr>
<tr><td>ansired</td></tr>
<tr><td>ansigreen</td></tr>
<tr><td>ansiyellow</td></tr>
<tr><td>ansiblue</td></tr>
<tr><td>ansimagenta</td></tr>
<tr><td>ansibrightblack</td></tr>
<tr><td>ansibrightred</td></tr>
<tr><td>ansibrightgreen</td></tr>
<tr><td>ansibrightyellow</td></tr>
<tr><td>ansibrightblue</td></tr>
<tr><td>ansibrightmagenta</td></tr>
<tr><td>ansibrightcyan</td></tr>
<tr><td>ansiwhite</td></tr>
</table>
