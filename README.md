# What’s this?
A quickly put together little Python script that enables you to postpone the due date of **review notes** and **review cards** created by the [obsidian-spaced-repetition](https://www.stephenmwangi.com/obsidian-spaced-repetition/) plugin written by Stephen Mwangi ([st3v3nmw](https://github.com/st3v3nmw/obsidian-spaced-repetition)) for the [Obsidian](https://obsidian.md/) note taking/knowledge management app.

# Why?
The *postponing feature* was [requested](https://github.com/st3v3nmw/obsidian-spaced-repetition/issues/798) in November 2023. Judging from the comments many dreaded they would not be able to keep up with their review queues during the winter festive period, and the request appeared to be supported by at least some users of the plugin. 

As of 14th Febuary 2024 this feature has not yet been implemented. Although I managed to get through the winter without too much of a backlog, sometimes I’d really like to have a weekend not “oriented around” my review queues or the fear that Monday’s review session will be brutal.

Since I don’t speak TypeScript, but desperately wanted a way to postpone review due dates, I thought I’d bridge the gap with this little Python script until the feature makes its way into the official [obsidian-spaced-repetition](https://www.stephenmwangi.com/obsidian-spaced-repetition/) plugin – which I’m sure will happen at some point.

# Okay, how do I use it?
Usage is simple but since the script was put together in the little free time I had you should **first be aware of the requirements** for use:
## Requirements
### Software
You must have Python (>3.8) installed on your system, although I think it should work with any Python3 version.
### Folder hierarchy and script placement
A picture is worth a thousand words. So I’ll start with that:
```
MyEmptyFolder/
├── MyVault/
└── obsidian_postponer.py
```
This means that:
1. you **MUST put** your Obsidian **Vault** (the directory of your Vault) **inside an empty folder** (e.g. `MyEmptyFolder/MyVault`)
2. then you **MUST put the script** `obsidian_postponer.py` in `MyEmptyFolder` just **at the same level as your `MyVault` folder** is.

### Backup
Create a backup of your vault before processing it with the script!
> [!WARNING]
> **Windows users:** 
> - If you simply copy-paste your Obsidian vault from one place to another your files’ creation dates will not be retained, but overwritten by the date at and time you are copying them. This is not a problem at all, unless **you care about watching the animated version of your graphs:** that will no longer represent the true chronological order of how you created your notes. To copy your files and preserve creation date timestamps, you can use the built-in [*Robocopy* function of Windows](https://superuser.com/a/1748913/763152).
> - if you **move** your Vault to a new location, timestamps are, indeed, preserved!
# Sure can I use it already?
## Overview
Yes you can. Follow the steps below:

> [!WARNING] 
> Make sure you didn’t skip the requirements!

1. Closing Obsidian is not necessary.
2. Open a command line inside your `MyEmptyFolder` where your Vault is. Then ask Python to run the script: for example, to postpone **both your card AND note review dates** by **10 days:**
```
python obsidian_postponer.py 10
```
3. Now go back to Obsidian.
4. Hit `CTRL + P` to fire up Obsidian’s command bar and start typing `reload`. You should now see a matching command appear: *Reload app without saving*. Select the command and hit ENTER.
5. Obsidian *might* do some re-indexing, let it finish.
6. Obsidian and the spaced repetition plugin are now fully aware of the new due dates and will adjust your note and card review queues accordingly.
## Further usage options
If you want the script to tell you all the options it has:
```
python obsidian_postponer.py --help
```

- You can postpone **cards only**:
```
python obsidian_postponer.py 10 -c
```
- Or **notes only** too:
```
python obsidian_postponer.py 10 -n
```

> [!IMPORTANT] 
> **If you make a mistake…**
> Example: you postponed everything by `100` days but you only wanted to postpone by `10`. Simply do another postpone of `-90` days. 

 - You can have all files listed that had at least one item already due at the time of running the script (verbose mode):
```
python obsidian_postponer.py 10 -v
```
## A nice trick
- to list all items with at least one item already due:
```
python obsidian_postponer.py 0 -v
```
# Why the rigid hierarchy, though?
The script expects your Vault directory to be at the same level as the script itself. It will then traverse ALL directories further down relative to its own location and work with any and all `.md` files it finds. 

- **This can be cool:** if you have multiple Vault directories next to the script, it will postpone note/card review dates across all of those Vaults.
- **This can be dangerous:** the script has no knowledge of Vaults. It simply looks for markdown (`.md`) files and processes them. If you run it in a folder that contains multiple Vaults and those Vaults also contain note/card review information they will also all be changed by the script.

# Disclaimer
So far I have not encountered any hiccups or damage arising from the use of this script. However, you are running it at your own risk, I make no guarantees. So please make sure you **create a backup of your Vault before using the script** on a Vault that is important to you.
